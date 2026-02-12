#!/usr/bin/env python3
"""
Verify all downloaded datasets for the adversarial prompts research project.

Checks that each dataset file exists, is non-empty, and has the expected structure.

Usage:
    python verify_datasets.py
"""

import csv
import gzip
import json
import os
import sys

DATASETS_DIR = os.path.dirname(os.path.abspath(__file__))

def check_csv(filepath, expected_min_rows=None, expected_columns=None):
    """Check a CSV file exists and has expected structure."""
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if expected_min_rows and len(rows) < expected_min_rows:
            return False, f"Expected >= {expected_min_rows} rows, got {len(rows)}"
        if expected_columns:
            for col in expected_columns:
                if col not in rows[0]:
                    return False, f"Missing column: {col}"
        return True, f"{len(rows)} rows, columns: {list(rows[0].keys())}"


def check_jsonl_gz(filepath, expected_min_rows=None):
    """Check a gzipped JSONL file."""
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    try:
        count = 0
        with gzip.open(filepath, "rt") as f:
            first = json.loads(f.readline())
            count = 1
            for line in f:
                count += 1
        if expected_min_rows and count < expected_min_rows:
            return False, f"Expected >= {expected_min_rows} rows, got {count}"
        return True, f"{count} examples, keys: {list(first.keys())}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def check_json(filepath, expected_min_items=None):
    """Check a JSON file."""
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    try:
        with open(filepath) as f:
            data = json.load(f)
        if isinstance(data, list):
            if expected_min_items and len(data) < expected_min_items:
                return False, f"Expected >= {expected_min_items} items, got {len(data)}"
            return True, f"{len(data)} items, sample keys: {list(data[0].keys()) if data else 'empty'}"
        elif isinstance(data, dict):
            return True, f"dict with {len(data)} keys: {list(data.keys())[:5]}"
        return True, f"type: {type(data).__name__}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def check_parquet(filepath):
    """Check a Parquet file exists and has reasonable size."""
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    size = os.path.getsize(filepath)
    if size < 1000:
        return False, f"File suspiciously small: {size} bytes"
    return True, f"Size: {size / (1024*1024):.1f} MB"


def main():
    all_ok = True
    results = []

    print("=" * 70)
    print("DATASET VERIFICATION REPORT")
    print("=" * 70)

    # --- HarmBench ---
    print("\n[HarmBench]")
    checks = [
        ("harmbench/harmbench_behaviors_text_all.csv", lambda p: check_csv(p, 300, ["Behavior", "BehaviorID"])),
        ("harmbench/harmbench_behaviors_text_test.csv", lambda p: check_csv(p, 200, ["Behavior"])),
        ("harmbench/harmbench_behaviors_text_val.csv", lambda p: check_csv(p, 50, ["Behavior"])),
    ]
    for relpath, checker in checks:
        fullpath = os.path.join(DATASETS_DIR, relpath)
        ok, msg = checker(fullpath)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {relpath}: {msg}")
        if not ok:
            all_ok = False

    # --- AdvBench ---
    print("\n[AdvBench]")
    checks = [
        ("advbench/harmful_behaviors.csv", lambda p: check_csv(p, 500, ["goal", "target"])),
        ("advbench/harmful_strings.csv", lambda p: check_csv(p, 500)),
    ]
    for relpath, checker in checks:
        fullpath = os.path.join(DATASETS_DIR, relpath)
        ok, msg = checker(fullpath)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {relpath}: {msg}")
        if not ok:
            all_ok = False

    # --- JailbreakBench ---
    print("\n[JailbreakBench]")
    checks = [
        ("jailbreakbench/harmful-behaviors.csv", lambda p: check_csv(p, 100, ["Goal", "Target", "Category"])),
        ("jailbreakbench/benign-behaviors.csv", lambda p: check_csv(p, 100)),
        ("jailbreakbench/judge-comparison.csv", lambda p: check_csv(p, 100)),
    ]
    for relpath, checker in checks:
        fullpath = os.path.join(DATASETS_DIR, relpath)
        ok, msg = checker(fullpath)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {relpath}: {msg}")
        if not ok:
            all_ok = False

    # --- NaturalQuestions / Lost in the Middle ---
    print("\n[NaturalQuestions / Lost in the Middle]")
    checks = [
        ("naturalquestions/nq-open-oracle.jsonl.gz", lambda p: check_jsonl_gz(p, 2000)),
        ("naturalquestions/nq_open_train.parquet", lambda p: check_parquet(p)),
        ("naturalquestions/nq_open_validation.parquet", lambda p: check_parquet(p)),
    ]
    for n_docs, positions in [(10, [0, 4, 9]), (20, [0, 4, 9, 14, 19]), (30, [0, 4, 9, 14, 19, 24, 29])]:
        for pos in positions:
            relpath = f"naturalquestions/{n_docs}_total_documents/nq-open-{n_docs}_total_documents_gold_at_{pos}.jsonl.gz"
            checks.append((relpath, lambda p: check_jsonl_gz(p, 2000)))
    for relpath, checker in checks:
        fullpath = os.path.join(DATASETS_DIR, relpath)
        ok, msg = checker(fullpath)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {relpath}: {msg}")
        if not ok:
            all_ok = False

    # KV retrieval
    for keys in [75, 140, 300]:
        relpath = f"naturalquestions/kv_retrieval_data/kv-retrieval-{keys}_keys.jsonl.gz"
        fullpath = os.path.join(DATASETS_DIR, relpath)
        ok, msg = check_jsonl_gz(fullpath, 100)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {relpath}: {msg}")
        if not ok:
            all_ok = False

    # --- SEP ---
    print("\n[SEP Dataset]")
    fullpath = os.path.join(DATASETS_DIR, "sep/SEP_dataset.json")
    ok, msg = check_json(fullpath, 9000)
    status = "OK" if ok else "FAIL"
    print(f"  [{status}] sep/SEP_dataset.json: {msg}")
    if not ok:
        all_ok = False

    # --- Summary ---
    print("\n" + "=" * 70)
    if all_ok:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED - see above for details")
    print("=" * 70)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
