import copy
import json
import os
import re
from typing import List

import torch
from datasets import load_dataset
from peft import LoraConfig
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from trl import GRPOConfig, GRPOTrainer

# logging
os.environ["WANDB_PROJECT"] = "verifiers-rlvr"

# model
model_id = "agentsea/Qwen2.5-VL-7B-SFT"
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
    use_cache=False,
)
lora_config = LoraConfig(
    lora_alpha=64,
    lora_dropout=0.05,
    r=32,
    bias="none",
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM",
)
processor = AutoProcessor.from_pretrained(model_id, padding_side="left")


# data
def preprocess_data(examples):
    batch_size = len(examples["prompt"])
    processed_prompts = []
    processed_images = []
    for i in range(batch_size):
        prompt_data = json.loads(examples["prompt"][i])
        image_data = examples["images"][i]
        processed_prompts.append(copy.deepcopy(prompt_data))
        image_index = 0
        for message in prompt_data:
            for content in message["content"]:
                if isinstance(content, dict) and content.get("type") == "image":
                    content["image"] = image_data[image_index]
                    image_index += 1
        processed_images_data, _ = process_vision_info(prompt_data)
        processed_images.append(processed_images_data)
    examples["images"] = processed_images
    examples["prompt"] = processed_prompts
    return examples


train_dataset = load_dataset("agentsea/gflights-trl-resampled", split="train")
train_dataset = train_dataset.shuffle(seed=42)
train_dataset = train_dataset.with_transform(preprocess_data)

eval_dataset = load_dataset("agentsea/gflights-trl-resampled", split="validation")
eval_dataset = eval_dataset.shuffle(seed=42).select(
    range(int(len(eval_dataset) * 0.1))
)  # only use 10% of eval dataset for evaluation
eval_dataset = eval_dataset.with_transform(preprocess_data)


# rewards
def reward_format(completions, **kwargs) -> List[float]:
    pattern = r"^<think>([^<]*(?:<(?!/?think>)[^<]*)*)<\/think>\n<answer>([\s\S]*?)<\/answer>$"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [
        re.search(pattern, content, re.DOTALL) for content in completion_contents
    ]
    return [
        1.0 if (match is not None and len(match.groups()) == 2) else 0.0
        for match in matches
    ]


def reward_correctness(completions, approved, **kwargs) -> List[float]:
    pattern = r"<answer>([\s\S]*?)<\/answer>"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [
        re.search(pattern, content, re.DOTALL) for content in completion_contents
    ]
    answers = [match.group(1) if match else None for match in matches]
    answer_bools = [
        (answer == "yes") if answer in ["yes", "no"] else None for answer in answers
    ]
    return [
        1.0 if (i < len(approved) and ans is not None and ans == approved[i]) else 0.0
        for i, ans in enumerate(answer_bools)
    ]


# grpo
training_args = GRPOConfig(
    output_dir="Qwen2.5-VL-7B-GRPO",
    logging_steps=1,
    use_vllm=True,
    vllm_device="cuda:1",  # TODO: remove this once vllm server is decoupled
    bf16=True,
    gradient_checkpointing=True,
    per_device_train_batch_size=10,
    num_generations=10,
    num_train_epochs=1,
    max_prompt_length=None,
    log_completions=True,
    do_eval=True,
    eval_steps=100,
    eval_strategy="steps",
    per_device_eval_batch_size=10,
    push_to_hub=True,
    push_to_hub_model_id="Qwen2.5-VL-7B-GRPO-SFTd-base-resampled",
    push_to_hub_organization="agentsea",
    hub_private_repo=True,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=1,
    adam_beta2=0.98,
    lr_scheduler_type="cosine",
    beta=0.001,
    temperature=1.0,
    sync_ref_model=True,
    ref_model_sync_steps=64,
    vllm_gpu_memory_utilization=0.9,
    run_name="Qwen2.5-VL-7B-GRPO-SFTd-base-resampled"
)

trainer = GRPOTrainer(
    model=model,
    processing_class=processor,
    reward_funcs=[reward_format, reward_correctness],
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    peft_config=lora_config,
)

trainer.train()
