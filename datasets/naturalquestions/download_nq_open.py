#!/usr/bin/env python3
"""
Download the NQ-Open dataset from HuggingFace.

NQ-Open (Natural Questions Open) contains 87,925 training and 3,610 validation
question-answer pairs derived from Google's Natural Questions dataset.
This is the open-domain variant where only questions with short answers are kept
and the evidence document is discarded.

Used by the "Lost in the Middle" paper for multi-document QA experiments
on position bias in long contexts.

Source: https://huggingface.co/datasets/google-research-datasets/nq_open
License: CC BY-SA 3.0

Usage:
    python download_nq_open.py [--output-dir OUTPUT_DIR]
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Download NQ-Open dataset from HuggingFace")
    parser.add_argument(
        "--output-dir",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Directory to save the dataset (default: same directory as this script)",
    )
    args = parser.parse_args()

    try:
        from datasets import load_dataset
    except ImportError:
        print("Error: 'datasets' library not installed.")
        print("Install with: pip install datasets")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    print("Downloading NQ-Open dataset from HuggingFace...")
    dataset = load_dataset("google-research-datasets/nq_open")

    for split_name in dataset:
        output_path = os.path.join(args.output_dir, f"nq_open_{split_name}.jsonl")
        print(f"Saving {split_name} split ({len(dataset[split_name])} examples) to {output_path}")
        with open(output_path, "w") as f:
            for example in dataset[split_name]:
                f.write(json.dumps(example) + "\n")

    print("Done!")
    print(f"Files saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
