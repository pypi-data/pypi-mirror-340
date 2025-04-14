import argparse
import json
import logging
import os
import re
from typing import List, Tuple

import torch
import wandb
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from prompts import SYSTEM_PROMPT, USER_PROMPT
from qwen_vl_utils import process_vision_info
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from transformers import (
    AutoProcessor,
    BitsAndBytesConfig,
    Qwen2_5_VLForConditionalGeneration,
    get_cosine_schedule_with_warmup,
)
from utils import translate_action_to_tool_call

# general
USE_WANDB = True
BEST_CHECKPOINT_DIR = "../assets/checkpoints/best"
# model
USE_LORA = True
USE_QLORA = False
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.bfloat16
ATTN_IMPLEMENTATION = "flash_attention_2"
# training
LEARNING_RATE = 1e-4
EPOCHS = 1
BATCH_SIZE = 1
GRAD_ACCUM_STEPS = 1
TRAIN_SAMPLE_RATIO = 1.0
# evaluation
EVAL_STEPS = 100
EVAL_BATCH_SIZE = 4
EVAL_SAMPLE_RATIO = 0.25
# optimizer
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.05
MAX_GRAD_NORM = 1.0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class AgentTutorDataset(Dataset):
    def __init__(self, split: str):
        self.data = load_dataset("agentsea/gflights-training2")[split]
        num_samples = int(
            len(self.data)
            * (TRAIN_SAMPLE_RATIO if split == "train" else EVAL_SAMPLE_RATIO)
        )
        self.data = self.data.shuffle(seed=42).select(range(num_samples))
        logger.info(
            f"Loaded {(TRAIN_SAMPLE_RATIO if split == "train" else EVAL_SAMPLE_RATIO)*100}% ({num_samples} samples) of {split} split"
        )

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> dict:
        sample: dict = self.data[idx]
        return {
            "task": sample["task_description"],
            "action": sample["action"],
            "state_image": sample["state_image_0"],
            "end_state_image": sample["end_state_image_1"],
            "reasoning": sample["reasoning"],
            "approved_label": sample["approved"],
        }


def load_model(
    model_name: str,
    use_lora: bool = USE_LORA,
    use_q_lora: bool = USE_QLORA,
    lora_alpha: int = 64,
    lora_dropout: float = 0.05,
    r: int = 32,
) -> Tuple[Qwen2_5_VLForConditionalGeneration, AutoProcessor]:
    # model
    if use_lora:
        lora_config = LoraConfig(
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            r=r,
            bias="none",
            target_modules=["q_proj", "v_proj"],
            task_type="CAUSAL_LM",
        )
    if use_q_lora:
        assert use_lora, "use_lora must be True if use_q_lora is True"
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4"
        )
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16 if use_q_lora else TORCH_DTYPE,
        attn_implementation=ATTN_IMPLEMENTATION,
        device_map="auto",
        quantization_config=bnb_config if use_q_lora else None,
    )
    if use_lora:
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
    # processor
    processor = AutoProcessor.from_pretrained(model_name)
    if ATTN_IMPLEMENTATION == "flash_attention_2":
        processor.tokenizer.padding_side = "left"  # flash attn needs this
    return model, processor


def prepare_inputs(batch: List[dict], processor, split: str) -> dict:
    assert split in ["train", "validation"]
    messages = []
    for example in batch:
        message = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": example["state_image"]},
                    {"type": "image", "image": example["end_state_image"]},
                    {
                        "type": "text",
                        "text": USER_PROMPT.format(
                            task=example["task"],
                            action=translate_action_to_tool_call(
                                json.loads(example["action"])
                            ),
                            true_label=(
                                "approved" if example["approved_label"] else "rejected"
                            ),
                        ),
                    },
                ],
            },
        ]
        if split == "train":
            message.append(
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": f"<think>{example['reasoning']}</think>\n<answer>{'yes' if example['approved_label'] else 'no'}</answer>",
                        }
                    ],
                }
            )
        messages.append(message)
    texts = [
        processor.apply_chat_template(
            msg,
            tokenize=False,
            add_generation_prompt=True if split == "validation" else False,
        )
        for msg in messages
    ]
    image_inputs, _ = process_vision_info(messages)
    return processor(text=texts, images=image_inputs, padding=True, return_tensors="pt")


def train_collate_fn(
    batch: List[dict], processor
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    inputs = prepare_inputs(batch, processor, split="train")
    labels = inputs["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    for image_token_id in [
        151652,
        151653,
        151655,
    ]:  # see tokenizer config https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct/blob/main/tokenizer_config.json
        labels[labels == image_token_id] = -100
    return (
        inputs["input_ids"],
        inputs["attention_mask"],
        inputs["pixel_values"],
        inputs["image_grid_thw"],
        labels,
    )


def val_collate_fn(
    batch: List[dict], processor
) -> Tuple[
    torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, List[str]
]:
    suffixes = [
        f"<think>{example['reasoning']}</think>\n<answer>{'yes' if example['approved_label'] else 'no'}</answer>"
        for example in batch
    ]
    inputs = prepare_inputs(batch, processor, split="validation")
    labels = inputs["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    for image_token_id in [151652, 151653, 151655]:
        labels[labels == image_token_id] = -100
    return (
        inputs["input_ids"],
        inputs["attention_mask"],
        inputs["pixel_values"],
        inputs["image_grid_thw"],
        labels,
        suffixes,
    )


def init_dataloader(split: str, processor) -> DataLoader:
    assert split in ["train", "validation"]
    return DataLoader(
        dataset=AgentTutorDataset(split),
        batch_size=BATCH_SIZE if split == "train" else EVAL_BATCH_SIZE,
        shuffle=True if split == "train" else False,
        collate_fn=lambda batch: train_collate_fn(batch, processor)
        if split == "train"
        else val_collate_fn(batch, processor),
    )


def setup_wandb(project_name: str, run_name: str) -> None:
    os.environ["WANDB_PROJECT"] = project_name
    wandb.init(
        project=project_name,
        name=run_name,
        config={
            "EPOCHS": EPOCHS,
            "LEARNING_RATE": LEARNING_RATE,
            "BATCH_SIZE": BATCH_SIZE,
        },
    )


def init_optimizer(model: Qwen2_5_VLForConditionalGeneration) -> torch.optim.Optimizer:
    return AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=WEIGHT_DECAY,
    )


def compute_loss(
    batch: Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
    model: Qwen2_5_VLForConditionalGeneration,
) -> torch.Tensor:
    input_ids, attention_mask, pixel_values, image_grid_thw, labels = batch
    inputs = {
        "input_ids": input_ids.to(model.device),
        "attention_mask": attention_mask.to(model.device),
        "pixel_values": pixel_values.to(model.device),
        "image_grid_thw": image_grid_thw.to(model.device),
        "labels": labels.to(model.device),
    }
    outputs = model(**inputs)
    return outputs.loss


def calculate_metrics(predicted_labels: List[str], true_labels: List[str]) -> dict:
    true_positive_count = sum(
        1
        for true, pred in zip(true_labels, predicted_labels)
        if true == "yes" and pred == "yes"
    )
    false_positive_count = sum(
        1
        for true, pred in zip(true_labels, predicted_labels)
        if true == "no" and pred == "yes"
    )
    true_negative_count = sum(
        1
        for true, pred in zip(true_labels, predicted_labels)
        if true == "no" and pred == "no"
    )
    false_negative_count = sum(
        1
        for true, pred in zip(true_labels, predicted_labels)
        if true == "yes" and pred == "no"
    )
    accuracy = (
        (true_positive_count + true_negative_count)
        / (
            true_positive_count
            + true_negative_count
            + false_positive_count
            + false_negative_count
        )
        if true_positive_count
        + true_negative_count
        + false_positive_count
        + false_negative_count
        > 0
        else 0
    )
    precision = (
        true_positive_count / (true_positive_count + false_positive_count)
        if true_positive_count + false_positive_count > 0
        else 0
    )
    recall = (
        true_positive_count / (true_positive_count + false_negative_count)
        if true_positive_count + false_negative_count > 0
        else 0
    )
    f1 = (
        2
        * true_positive_count
        / (2 * true_positive_count + false_positive_count + false_negative_count)
        if 2 * true_positive_count + false_positive_count + false_negative_count > 0
        else 0
    )
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positive": true_positive_count,
        "false_positive": false_positive_count,
        "true_negative": true_negative_count,
        "false_negative": false_negative_count,
    }


def eval(model, val_dataloader, processor) -> dict:
    model.eval()
    total_loss = 0
    num_batches = 0
    predicted_labels = []
    true_labels = []
    error_count = 0
    example_count = 0
    answer_pattern = re.compile(r"<answer>([\s\S]*?)<\/answer>", re.DOTALL)
    with torch.no_grad():
        for batch in tqdm(val_dataloader, desc="Evaluating"):
            num_batches += 1
            (
                input_ids,
                attention_mask,
                pixel_values,
                image_grid_thw,
                labels,
                suffixes,
            ) = batch  # unpack batch
            loss = compute_loss(
                (input_ids, attention_mask, pixel_values, image_grid_thw, labels), model
            )  # compute loss
            total_loss += loss.item()
            outputs = model.generate(
                input_ids=input_ids.to(model.device),
                attention_mask=attention_mask.to(model.device),
                pixel_values=pixel_values.to(model.device),
                image_grid_thw=image_grid_thw.to(model.device),
                max_new_tokens=256,
                output_logits=True,
                return_dict_in_generate=True,
            )  # generate outputs for eval metrics
            trimmed_ids = [
                out_ids[len(in_ids) :]
                for in_ids, out_ids in zip(input_ids, outputs.sequences)
            ]
            decoded_outputs = processor.tokenizer.batch_decode(
                trimmed_ids, skip_special_tokens=True
            )
            for _, (decoded_output, suffix) in enumerate(
                zip(decoded_outputs, suffixes)
            ):
                example_count += 1
                try:
                    # true label
                    true_label_match = answer_pattern.search(suffix)
                    if not true_label_match:
                        error_count += 1
                        continue
                    true_label = true_label_match.group(1).strip()
                    # predicted label
                    predicted_label_match = answer_pattern.search(decoded_output)
                    if not predicted_label_match:
                        error_count += 1
                        continue
                    predicted_label = predicted_label_match.group(1).strip()
                    if predicted_label not in ["yes", "no"]:
                        error_count += 1
                        continue
                except Exception:
                    error_count += 1
                    continue
                predicted_labels.append(predicted_label)
                true_labels.append(true_label)
    avg_loss = total_loss / num_batches if num_batches > 0 else 0
    if len(true_labels) > 0:
        metrics = calculate_metrics(predicted_labels, true_labels)
        metrics["error_rate"] = error_count / example_count if example_count > 0 else 0
    else:
        metrics = {
            "error_rate": 1.0 if example_count > 0 else 0,
            "loss": avg_loss,
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        }
    logger.info(
        f"Evaluation completed. Average loss: {avg_loss:.4f}. Num batches: {num_batches}. Error rate: {metrics['error_rate']:.4f}"
    )
    model.train()
    return {"loss": avg_loss, **metrics}


def train(model: Qwen2_5_VLForConditionalGeneration, processor: AutoProcessor) -> None:
    logger.info("Initializing training...")
    train_dataloader = init_dataloader(split="train", processor=processor)
    val_dataloader = init_dataloader(split="validation", processor=processor)
    optimizer = init_optimizer(model)
    num_training_steps = EPOCHS * len(train_dataloader) // GRAD_ACCUM_STEPS
    num_warmup_steps = int(num_training_steps * WARMUP_RATIO)
    scheduler = get_cosine_schedule_with_warmup(
        optimizer=optimizer,
        num_warmup_steps=num_warmup_steps,
        num_training_steps=num_training_steps,
    )
    logger.info(f"Total training steps: {num_training_steps}")
    logger.info(f"Warmup steps: {num_warmup_steps}")
    processor.save_pretrained(BEST_CHECKPOINT_DIR)  # only save this once
    processor.push_to_hub("agentsea/Qwen2.5-VL-7B-SFT-adapter", private=True)
    best_val_accuracy = float("-inf")
    i = 0
    model.train()
    for epoch in range(EPOCHS):
        progress_bar = tqdm(
            total=len(train_dataloader),
            desc=f"Epoch {epoch + 1}/{EPOCHS}",
            position=0,
            leave=True,
        )
        for _, batch in enumerate(train_dataloader):
            i += 1
            loss = compute_loss(batch, model)
            loss = loss / GRAD_ACCUM_STEPS
            loss.backward()
            if i % GRAD_ACCUM_STEPS == 0:
                torch.nn.utils.clip_grad_norm_(
                    model.parameters(), max_norm=MAX_GRAD_NORM
                )
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                progress_bar.set_postfix(
                    {
                        "loss": f"{loss.item():.4f}",
                        "lr": f"{scheduler.get_last_lr()[0]:.2e}",
                    }
                )
                progress_bar.update()
                if USE_WANDB:
                    wandb.log(
                        {
                            "train/loss": loss.item(),
                            "train/learning_rate": scheduler.get_last_lr()[0],
                        }
                    )
            if i % EVAL_STEPS == 0:
                logger.info(f"Running evaluation at step {i}")
                eval_metrics = eval(model, val_dataloader, processor)
                if USE_WANDB:
                    wandb.log({f"eval/{k}": v for k, v in eval_metrics.items()})
                if (
                    eval_metrics["accuracy"] > best_val_accuracy
                    and eval_metrics["error_rate"] == 0
                ):
                    best_val_accuracy = eval_metrics["accuracy"]
                    logger.info(f"New best validation loss: {best_val_accuracy:.4f}")
                    os.makedirs(BEST_CHECKPOINT_DIR, exist_ok=True)
                    model.save_pretrained(BEST_CHECKPOINT_DIR)
                    model.push_to_hub(
                        "agentsea/Qwen2.5-VL-7B-SFT-adapter",
                        private=True,
                        commit_message=f"New best validation accuracy: {best_val_accuracy:.4f} at step {i}",
                    )
                metrics_str = " | ".join(
                    [f"{k}: {v:.4f}" for k, v in eval_metrics.items()]
                )
                logger.info(f"Evaluation metrics - {metrics_str}")
        progress_bar.close()
        logger.info(f"Epoch {epoch + 1}/{EPOCHS} completed")
    if USE_WANDB:
        wandb.finish()
    logger.info("Training completed!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--wandb_project_name", type=str)
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    model_name = args.model_name
    if USE_WANDB:
        wandb_project_name = args.wandb_project_name
        assert (
            wandb_project_name is not None
        ), "wandb_project_name is required for wandb usage"
        run_name = f"{model_name}-LR{LEARNING_RATE}-EPOCHS{EPOCHS}-BATCH{BATCH_SIZE}-WARMUP{WARMUP_RATIO}-EVALSTEPS{EVAL_STEPS}-EVALBATCH{EVAL_BATCH_SIZE}-EVALSAMPLE{EVAL_SAMPLE_RATIO}-TRAINSAMPLE{TRAIN_SAMPLE_RATIO}"
        setup_wandb(wandb_project_name, run_name)
    assert model_name in [
        "Qwen/Qwen2.5-VL-3B-Instruct",
        "Qwen/Qwen2.5-VL-7B-Instruct",
        "Qwen/Qwen2.5-VL-72B-Instruct",
    ]
    model, processor = load_model(model_name)
    train(model, processor)


if __name__ == "__main__":
    main()
