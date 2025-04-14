import argparse
import json
import subprocess
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import torch
import torch.nn.functional as F
from datasets import load_dataset
from qwen_vl_utils import process_vision_info
from tqdm import tqdm
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from utils import translate_action_to_tool_call

SYSTEM_PROMPT = """You are a helpful assistant to a computer-use agent.

Your task is to evaluate whether an action is directionally correct.

IMPORTANT: This is only **one** action within a sequence of actions. You should not evaluate whether the action finished the task, but whether it is directionally correct.

Use the following format to answer the question:

*Reasoning*: <reasoning>
*Correct*: <correct>

Note: The value of the `correct` field should be either `yes` or `no` (lowercase only).
"""
USER_PROMPT = """TASK: "{task}"
ACTION: "{action}"
The images show the state of the computer before and after the action.
"""
TOKENS = [1004, 1024, 2048, 4096, 8192, 16384]
PIXELS = [x * 28 * 28 for x in TOKENS]


def load_model(model_name):
    return Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",
        device_map="auto",
    )


def prepare_inputs(task, action, state_image, end_state_image, processor):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": [
                {"type": "image", "image": state_image},
                {"type": "image", "image": end_state_image},
                {
                    "type": "text",
                    "text": USER_PROMPT.format(
                        task=task,
                        action=translate_action_to_tool_call(json.loads(action)),
                    ),
                },
            ],
        },
    ]
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")
    return inputs


def generate_answer(model, inputs):
    start_time = time.time()
    memory_samples = []

    def memory_callback(step, token_id, outputs):
        memory_samples.append(get_gpu_memory_usage())
        return False

    memory_samples.append(get_gpu_memory_usage())

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        output_logits=True,
        return_dict_in_generate=True,
        streamer=memory_callback if hasattr(model, "streamer") else None,
    )

    memory_samples.append(get_gpu_memory_usage())

    generation_time = time.time() - start_time
    avg_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
    peak_memory = max(memory_samples) if memory_samples else 0
    return outputs, generation_time, avg_memory, peak_memory


def get_gpu_memory_usage():
    """Get GPU memory usage in MB using nvidia-smi"""
    result = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,nounits,noheader"],
        encoding="utf-8",
    )
    return float(result.strip())


def get_gpu_total_memory():
    """Get total GPU memory capacity in MB"""
    result = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,nounits,noheader"],
        encoding="utf-8",
    )
    return float(result.strip())


def create_summary(all_metrics):
    """Create and save summary table and graph"""
    total_gpu_memory = get_gpu_total_memory()

    # Prepare data for the table
    data = {
        "Pixel Size": [],
        "Accuracy (%)": [],
        "Precision (%)": [],
        "Recall (%)": [],
        "F1 Score (%)": [],
        "Generation Time (s)": [],
        "GPU Utilization (%)": [],
    }

    for metrics in all_metrics:
        data["Pixel Size"].append(metrics["pixel_size"])
        data["Accuracy (%)"].append(metrics["accuracy"] * 100)
        data["Precision (%)"].append(metrics["precision"] * 100)
        data["Recall (%)"].append(metrics["recall"] * 100)
        data["F1 Score (%)"].append(metrics["f1_score"] * 100)
        data["Generation Time (s)"].append(metrics["avg_generation_time"])
        data["GPU Utilization (%)"].append(
            (metrics["avg_generation_memory_mb"] / total_gpu_memory) * 100
        )

    # Create DataFrame and save table
    df = pd.DataFrame(data)
    table_str = "# Performance metrics across different pixel sizes\n\n"
    table_str += df.to_markdown(index=False, floatfmt=".2f")

    output_dir = Path("../assets/eval_results/reward_model/size_ablation")

    with open(output_dir / "summary_table.md", "w") as f:
        f.write(table_str)

    # Create performance metrics graph
    plt.figure(figsize=(12, 6))
    metrics_to_plot = [
        "Accuracy (%)",
        "Precision (%)",
        "Recall (%)",
        "F1 Score (%)",
        "GPU Utilization (%)",
    ]

    for metric in metrics_to_plot:
        plt.plot(data["Pixel Size"], data[metric], marker="o", label=metric)

    plt.xlabel("Pixel Size")
    plt.ylabel("Percentage")
    plt.title("Performance Metrics vs Pixel Size")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_dir / "performance_metrics.png", dpi=300, bbox_inches="tight")
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    args = parser.parse_args()
    assert args.model_name in [
        "Qwen/Qwen2.5-VL-7B-Instruct",
        "Qwen/Qwen2.5-VL-72B-Instruct",
    ]
    model = load_model(args.model_name)

    ds_val = load_dataset("agentsea/gflights-annotated-split-filtered", split="validation")

    all_metrics = []

    for pixel_size in PIXELS:
        print(f"\nEvaluating with pixel_size={pixel_size}")
        processor = AutoProcessor.from_pretrained(
            args.model_name, min_pixels=pixel_size, max_pixels=pixel_size
        )

        results = []
        num_correct = 0
        total_examples = 0
        sum_final_answer_prob = 0.0
        total_generation_time = 0.0
        sum_avg_memory = 0.0
        sum_peak_memory = 0.0
        confusion_matrix = {
            "true_positive": 0,
            "false_positive": 0,
            "true_negative": 0,
            "false_negative": 0,
        }

        for example in tqdm(ds_val, desc="Evaluating test examples"):
            task = example["task_description"]
            action = example["action"]
            state_image = example["state_image_0"]
            end_state_image = example["end_state_image_1"]
            inputs = prepare_inputs(
                task, action, state_image, end_state_image, processor
            )
            outputs, generation_time, avg_memory, peak_memory = generate_answer(
                model, inputs
            )
            sum_avg_memory += avg_memory
            sum_peak_memory += peak_memory
            total_generation_time += generation_time
            decoded = processor.decode(
                outputs.sequences[0][inputs.input_ids.shape[1] :],
                skip_special_tokens=True,
            )
            final_answer_token_id = int(outputs.sequences[0][-2])
            final_answer = processor.tokenizer.decode([final_answer_token_id]).strip()
            logits = outputs.logits[-2]
            probs = F.softmax(logits, dim=1)
            final_answer_prob = float(probs[0, final_answer_token_id])
            true_label = "yes" if example["approved"] else "no"
            correct = final_answer.lower() == true_label
            if correct:
                num_correct += 1
            total_examples += 1
            sum_final_answer_prob += final_answer_prob
            predicted_yes = final_answer.lower() == "yes"
            actual_yes = true_label == "yes"
            if predicted_yes and actual_yes:
                confusion_matrix["true_positive"] += 1
            elif predicted_yes and not actual_yes:
                confusion_matrix["false_positive"] += 1
            elif not predicted_yes and actual_yes:
                confusion_matrix["false_negative"] += 1
            else:
                confusion_matrix["true_negative"] += 1
            results.append(
                {
                    "task_id": example["task_id"],
                    "true_label": true_label,
                    "full_answer": decoded,
                    "final_answer": final_answer,
                    "final_answer_prob": final_answer_prob,
                    "generation_time": generation_time,
                }
            )

        accuracy = num_correct / total_examples if total_examples > 0 else 0.0
        avg_final_answer_prob = (
            sum_final_answer_prob / total_examples if total_examples > 0 else 0.0
        )
        avg_generation_time = (
            total_generation_time / total_examples if total_examples > 0 else 0.0
        )
        precision = (
            confusion_matrix["true_positive"]
            / (confusion_matrix["true_positive"] + confusion_matrix["false_positive"])
            if (confusion_matrix["true_positive"] + confusion_matrix["false_positive"])
            > 0
            else 0.0
        )
        recall = (
            confusion_matrix["true_positive"]
            / (confusion_matrix["true_positive"] + confusion_matrix["false_negative"])
            if (confusion_matrix["true_positive"] + confusion_matrix["false_negative"])
            > 0
            else 0.0
        )
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        avg_memory_usage = (
            sum_avg_memory / total_examples if total_examples > 0 else 0.0
        )
        avg_peak_memory = (
            sum_peak_memory / total_examples if total_examples > 0 else 0.0
        )

        output_dir = Path("../assets/eval_results/reward_model/size_ablation")
        output_dir.mkdir(parents=True, exist_ok=True)

        size_suffix = f"_size{pixel_size}"
        output_file = output_dir / f"reward_results{size_suffix}.json"
        metrics_file = output_dir / f"reward_metrics{size_suffix}.json"

        metrics = {
            "pixel_size": pixel_size,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "avg_generation_time": avg_generation_time,
            "avg_final_answer_prob": avg_final_answer_prob,
            "avg_generation_memory_mb": avg_memory_usage,
            "avg_peak_generation_memory_mb": avg_peak_memory,
            "confusion_matrix": confusion_matrix,
        }

        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)

        print(f"\nResults for pixel_size={pixel_size}:")
        print(
            f"Classification Accuracy: {accuracy*100:.2f}% ({num_correct} / {total_examples})"
        )
        print(f"Average final answer probability: {avg_final_answer_prob*100:.2f}%")
        print(f"Average generation time: {avg_generation_time:.3f} seconds")
        print(f"Precision: {precision*100:.2f}%")
        print(f"Recall: {recall*100:.2f}%")
        print(f"F1 Score: {f1_score*100:.2f}%")
        print("\nConfusion Matrix:")
        print(f"True Positives: {confusion_matrix['true_positive']}")
        print(f"False Positives: {confusion_matrix['false_positive']}")
        print(f"True Negatives: {confusion_matrix['true_negative']}")
        print(f"False Negatives: {confusion_matrix['false_negative']}")
        print(f"Average Generation Memory Usage: {avg_memory_usage:.0f} MB")
        print(f"Average Peak Generation Memory Usage: {avg_peak_memory:.0f} MB")
        print(f"\nSaved results to {output_file}")
        print(f"Saved metrics to {metrics_file}")

        all_metrics.append(metrics)

    create_summary(all_metrics)
    print(
        "\nSummary table and graph have been saved to 'summary_table.md' and 'performance_metrics.png'"
    )


if __name__ == "__main__":
    main()
