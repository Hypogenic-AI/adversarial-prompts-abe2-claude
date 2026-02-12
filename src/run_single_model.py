"""Run experiment for a single model. Usage: python src/run_single_model.py <model_name>"""

import sys
import json
from pathlib import Path

# Import from run_experiment
sys.path.insert(0, "src")
from run_experiment import MODELS, RESULTS_DIR, run_experiment

def main():
    model_name = sys.argv[1]
    if model_name not in MODELS:
        print(f"Unknown model: {model_name}. Available: {list(MODELS.keys())}")
        sys.exit(1)

    model_config = MODELS[model_name]

    with open("results/test_cases.json") as f:
        test_cases = json.load(f)
    with open("results/control_cases.json") as f:
        controls = json.load(f)

    print(f"Running {len(test_cases)} test cases for {model_name}")
    checkpoint = RESULTS_DIR / f"results_{model_name.replace('.', '_').replace('-', '_')}.json"
    results = run_experiment(test_cases, model_name, model_config, checkpoint)

    # Summary
    valid = [r for r in results if r.get("error") is None]
    successes = [r for r in valid if r.get("injection_success") is True]
    print(f"\n{model_name}: {len(successes)}/{len(valid)} injection successes ({len(successes)/len(valid)*100:.1f}%)")

    # By length
    from collections import defaultdict
    by_length = defaultdict(lambda: {"total": 0, "success": 0})
    for r in valid:
        by_length[r["length"]]["total"] += 1
        if r.get("injection_success"):
            by_length[r["length"]]["success"] += 1

    print(f"\nISR by length:")
    for length in sorted(by_length.keys()):
        d = by_length[length]
        isr = d["success"] / d["total"] * 100 if d["total"] > 0 else 0
        print(f"  {length:>6} words: {d['success']:>3}/{d['total']:>3} = {isr:>5.1f}%")

    # Also run controls
    print(f"\nRunning {len(controls)} control cases...")
    ctrl_checkpoint = RESULTS_DIR / f"controls_{model_name.replace('.', '_').replace('-', '_')}.json"
    ctrl_results = run_experiment(controls, model_name, model_config, ctrl_checkpoint)
    ctrl_valid = [r for r in ctrl_results if r.get("error") is None]
    ctrl_successes = [r for r in ctrl_valid if r.get("injection_success") is True]
    print(f"Controls: {len(ctrl_successes)}/{len(ctrl_valid)} false positives")

if __name__ == "__main__":
    main()
