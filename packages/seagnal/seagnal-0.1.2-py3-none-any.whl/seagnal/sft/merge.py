import argparse
import logging
import os

import torch
from peft import PeftModel
from transformers import (
    AutoProcessor,
    Qwen2_5_VLForConditionalGeneration,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


def merge_adapter(base_model_name, adapter_path, output_dir):
    """
    Merge LoRA adapter weights into the base model.

    Args:
        base_model_name: Name of the base model
        adapter_path: Path to the LoRA adapter weights
        output_dir: Directory to save the merged model
    """
    logger.info(f"Loading base model: {base_model_name}")
    base_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(base_model_name, torch_dtype=torch.bfloat16, device_map="auto")
    logger.info(f"Loading adapter from: {adapter_path}")
    model = PeftModel.from_pretrained(base_model, adapter_path)
    logger.info("Merging adapter weights into base model")
    merged_model = model.merge_and_unload()
    logger.info(f"Saving merged model to: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    merged_model.save_pretrained(output_dir)
    logger.info("Saving processor")
    processor = AutoProcessor.from_pretrained(base_model_name)
    processor.save_pretrained(output_dir)
    logger.info("Merge completed successfully!")
    return merged_model


def main():
    parser = argparse.ArgumentParser(description="Merge LoRA adapter into base model")
    parser.add_argument("--base_model_name", type=str, required=True, help="Name or path of the base model")
    parser.add_argument("--adapter_path", type=str, required=True, help="Path to the LoRA adapter weights")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the merged model")
    parser.add_argument("--push_to_hub", action="store_true", help="Push merged model to Hugging Face Hub")
    parser.add_argument("--hub_model_id", type=str, help="Model ID for Hugging Face Hub (required if push_to_hub=True)")
    parser.add_argument("--private", action="store_true", help="Make the uploaded model private")
    args = parser.parse_args()
    if args.push_to_hub and not args.hub_model_id:
        parser.error("--hub_model_id is required when using --push_to_hub")
    merged_model = merge_adapter(args.base_model_name, args.adapter_path, args.output_dir)
    if args.push_to_hub:
        logger.info(f"Pushing merged model to Hugging Face Hub: {args.hub_model_id}")
        merged_model.push_to_hub(args.hub_model_id, private=args.private)
        processor = AutoProcessor.from_pretrained(args.output_dir)
        processor.push_to_hub(args.hub_model_id, private=args.private)
        logger.info("Model pushed to hub successfully!")


if __name__ == "__main__":
    main()
