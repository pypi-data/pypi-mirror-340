import argparse
import json
import time
from pathlib import Path

import datasets
import torch
import torch.nn.functional as F
from datasets import DatasetDict, load_dataset
from qwen_vl_utils import process_vision_info
from tqdm import tqdm
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

from utils import translate_action_to_tool_call

SYSTEM_PROMPT = """You are a helpful assistant to a computer-use agent.

Your task is to write down the reasoning that justifies whether an action is directionally correct or not.

You will be given a task description, an action, and images showing the state of the computer before and after the action, along with the true label (rejected or approved).

IMPORTANT: This is only **one** action within a sequence of actions.

NOTE: Do not explicitly mention if the action is approved or directionally correct or not. Just write the reasoning.
"""
USER_PROMPT = """TASK: "{task}"
ACTION: "{action}"
TRUE LABEL: "{true_label}"
The images show the state of the computer before and after the action.
"""
BATCH_SIZE = 16


def load_model(model_name):
    return Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",
        device_map="auto",
    )


def prepare_inputs(
    tasks, actions, state_images, end_state_images, approved_labels, processor
):
    messages = []
    for task, action, state_image, end_state_image, approved_label in zip(
        tasks, actions, state_images, end_state_images, approved_labels
    ):
        message = [
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
                            true_label="approved" if approved_label else "rejected",
                        ),
                    },
                ],
            },
        ]
        messages.append(message)
    texts = [
        processor.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        for msg in messages
    ]
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=texts,
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")
    return inputs


def generate_answer(model, inputs):
    return model.generate(**inputs, max_new_tokens=256, output_logits=True, return_dict_in_generate=True, temperature=0.6)


def process_batch(batch, model=None, processor=None):
    inputs = prepare_inputs(
        batch["task_description"],
        batch["action"],
        batch["state_image_0"],
        batch["end_state_image_1"],
        batch["approved"],
        processor,
    )
    outputs = generate_answer(model, inputs)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :]
        for in_ids, out_ids in zip(inputs.input_ids, outputs.sequences)
    ]
    return processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    args = parser.parse_args()
    assert args.model_name in [
        "Qwen/Qwen2.5-VL-7B-Instruct",
        "Qwen/Qwen2.5-VL-72B-Instruct",
    ]
    model = load_model(args.model_name)
    processor = AutoProcessor.from_pretrained(args.model_name)
    processor.tokenizer.padding_side = "left" # flash attn needs this
    ds = load_dataset("agentsea/gflights-annotated-split-filtered")
    processed_ds = {}

    for split in ds.keys():
        all_reasoning = []
        for i in tqdm(
            range(0, len(ds[split]), BATCH_SIZE), desc=f"Processing {split} split"
        ):
            batch = ds[split].select(range(i, min(i + BATCH_SIZE, len(ds[split]))))
            reasoning = process_batch(batch, model, processor)
            all_reasoning.extend(reasoning)
        processed_split = ds[split].add_column("reasoning", all_reasoning)
        processed_ds[split] = processed_split

    processed_ds = DatasetDict(processed_ds)
    processed_ds.push_to_hub("agentsea/gflights-training2", private=True)


if __name__ == "__main__":
    main()
