# Resources Catalog: Adversarial Prompt Hiding in Long Documents

A comprehensive catalog of all papers, datasets, and code repositories gathered for this research project.

---

## Papers

All papers are stored in `papers/`. Total: 17 PDFs.

### Tier 1: Directly Address the Research Question

| File | Title | Authors | Year | arXiv |
|------|-------|---------|------|-------|
| `2511.04707_jailbreaking_in_the_haystack.pdf` | Jailbreaking in the Haystack: Compute-Optimal Long-Context Attacks on LLMs (NINJA) | Shah, Wu, Zhong, Robey, Raghunathan | 2025 | [2511.04707](https://arxiv.org/abs/2511.04707) |
| `2502.04204_short_length_adversarial_training.pdf` | Short-length Adversarial Training Helps LLMs Defend Long-length Jailbreak Attacks | Fu, Ding, Zhang, Wang | 2025 | [2502.04204](https://arxiv.org/abs/2502.04204) |
| `2307.03172_lost_in_the_middle.pdf` | Lost in the Middle: How Language Models Use Long Contexts | Liu, Lin, Hewitt, Paranjape, Bevilacqua, Petroni, Liang | 2024 | [2307.03172](https://arxiv.org/abs/2307.03172) |
| `2404.02151_many_shot_jailbreaking.pdf` | Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks | Andriushchenko, Croce, Flammarion | 2024 | [2404.02151](https://arxiv.org/abs/2404.02151) |

### Tier 2: Defenses and Instruction-Data Separation

| File | Title | Authors | Year | arXiv |
|------|-------|---------|------|-------|
| `2403.14720_spotlighting_defense.pdf` | Spotlighting: Defending LLMs Against Prompt Injection | Hines, Kramer, Grady, Berger, Celikyilmaz | 2024 | [2403.14720](https://arxiv.org/abs/2403.14720) |
| `2403.06833_can_llms_separate_instructions_data.pdf` | Can LLMs Separate Instructions From Data? And What Do We Even Mean By That? | Gozverev et al. | 2025 | [2403.06833](https://arxiv.org/abs/2403.06833) |
| `2410.05451_secalign.pdf` | SecAlign: Defending Against Prompt Injection with Preference Optimization | — | 2024 | [2410.05451](https://arxiv.org/abs/2410.05451) |
| `2503.10566_aside.pdf` | ASIDE: Architectural Separation of Instructions and Data in Language Models | — | 2025 | [2503.10566](https://arxiv.org/abs/2503.10566) |
| `2410.09102_instructional_segment_embedding.pdf` | Instructional Segment Embedding | — | 2024 | [2410.09102](https://arxiv.org/abs/2410.09102) |

### Tier 3: Attack Methods and Threat Models

| File | Title | Authors | Year | arXiv |
|------|-------|---------|------|-------|
| `2302.12173_indirect_prompt_injection.pdf` | Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz | 2023 | [2302.12173](https://arxiv.org/abs/2302.12173) |
| `2305.14950_adversarial_demonstration_attacks.pdf` | Adversarial Demonstration Attacks on Large Language Models | — | 2023 | [2305.14950](https://arxiv.org/abs/2305.14950) |
| `2512.03001_invasive_context_engineering.pdf` | Invasive Context Engineering | — | 2025 | [2512.03001](https://arxiv.org/abs/2512.03001) |
| `2312.02780_scaling_laws_adversarial_activations.pdf` | Scaling Laws for Adversarial Activations | — | 2023 | [2312.02780](https://arxiv.org/abs/2312.02780) |
| `2502.15609_robustness_context_hijacking.pdf` | Robustness to Context Hijacking | — | 2025 | [2502.15609](https://arxiv.org/abs/2502.15609) |

### Tier 4: Specialized Attack Vectors

| File | Title | Authors | Year | arXiv |
|------|-------|---------|------|-------|
| `2505.16957_invisible_prompts_font_injection.pdf` | Invisible Prompts: Hidden Adversarial Instructions via Font-Based Injection | — | 2025 | [2505.16957](https://arxiv.org/abs/2505.16957) |
| `2507.05093_hidden_threat_rag.pdf` | Hidden Threat in RAG Data Loaders | — | 2025 | [2507.05093](https://arxiv.org/abs/2507.05093) |
| `2508.20863_publish_to_perish.pdf` | Publish to Perish: Adversarial Prompt Injection in Peer Review | — | 2025 | [2508.20863](https://arxiv.org/abs/2508.20863) |

---

## Datasets

All datasets are stored in `datasets/`. Total size: ~266 MB.

| Dataset | Directory | Size | Examples | Source Paper | Primary Use |
|---------|-----------|------|----------|--------------|-------------|
| HarmBench | `datasets/harmbench/` | 238 KB | 400 behaviors (320 test / 80 val) | Mazeika et al., 2024 | Standard red teaming evaluation; 80-behavior test set used by NINJA |
| AdvBench | `datasets/advbench/` | 46 KB | 520 behaviors + 574 strings | Zou et al., 2023 | Universal attack benchmark; foundational harmful behaviors dataset |
| JailbreakBench | `datasets/jailbreakbench/` | 186 KB | 100 harmful + 100 benign | Chao et al., 2024 | Curated jailbreak benchmark with overrefusal measurement |
| NaturalQuestions / Lost in the Middle | `datasets/naturalquestions/` | 262 MB | 2,655 QA pairs × multiple configs | Liu et al., 2024 | Position bias experiments; multi-document QA at varying lengths |
| SEP | `datasets/sep/` | 4 MB | 9,160 paired examples | Gozverev et al., 2025 | Instruction-data separation measurement |

### Dataset Details

- **HarmBench:** 3 CSV files (`harmbench_behaviors_text_{all,test,val}.csv`). Schema: Behavior, FunctionalCategory, SemanticCategory, Tags, ContextString, BehaviorID.
- **AdvBench:** 2 CSV files (`harmful_behaviors.csv`, `harmful_strings.csv`). Schema: goal, target.
- **JailbreakBench:** 3 CSV files (`harmful-behaviors.csv`, `benign-behaviors.csv`, `judge-comparison.csv`). Sourced from AdvBench + HarmBench + TDC.
- **NaturalQuestions:** Parquet files (NQ-Open), JSONL files (multi-doc QA at 10/20/30 docs with varied gold positions), key-value retrieval data. Includes download scripts for full Contriever documents (~1.3 GB).
- **SEP:** Single JSON file with 9,160 paired clean/instructed examples across task types.

See `datasets/README.md` for full documentation including schemas, download instructions, and verification script.

---

## Code Repositories

All repositories are cloned in `code/`. Total: 5 repos.

| Repository | Directory | Paper | URL |
|------------|-----------|-------|-----|
| NINJA_Attack | `code/NINJA_Attack/` | Jailbreaking in the Haystack (2511.04707) | [github.com/AR-FORUM/NINJA_Attack](https://github.com/AR-FORUM/NINJA_Attack) |
| adv-icl | `code/adv-icl/` | Short-length Adversarial Training (2502.04204) | [github.com/fshp971/adv-icl](https://github.com/fshp971/adv-icl) |
| llm-adaptive-attacks | `code/llm-adaptive-attacks/` | Adaptive Attacks on Safety-Aligned LLMs (2404.02151) | [github.com/tml-epfl/llm-adaptive-attacks](https://github.com/tml-epfl/llm-adaptive-attacks) |
| HarmBench | `code/HarmBench/` | HarmBench Framework (2402.04249) | [github.com/centerforaisafety/HarmBench](https://github.com/centerforaisafety/HarmBench) |
| jailbreakbench | `code/jailbreakbench/` | JailbreakBench (2404.01318) | [github.com/JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench) |

### Repository Highlights

- **NINJA_Attack:** Most directly relevant. Implements `LongContext` attack method on HarmBench framework. Key files: `baselines/longcontext/`, configs for 1K-15K word contexts, pre-computed results.
- **adv-icl:** Implements adversarial ICL training with √M scaling law. Key files: `src/adv_trainers/`, `src/attacks/` (GCG, AutoDAN, BEAST).
- **llm-adaptive-attacks:** Simple adaptive attack achieving ~100% ASR. Key files: `main.py` (random search), `prompts.py` (model-specific templates), `jailbreak_artifacts/` (pre-computed jailbreaks for 15+ models).
- **HarmBench:** Standard evaluation framework. Key files: `data/behavior_datasets/`, `baselines/` (18+ attack implementations), pipeline scripts.
- **jailbreakbench:** Benchmark with defense implementations. Key files: `src/jailbreakbench/defenses/` (SmoothLLM, perplexity filter, etc.), `src/jailbreakbench/classifier.py`.

See `code/README.md` for detailed file-level documentation and cross-repository connections.

---

## Quick Start Guide

### Reproducing NINJA Attack (Most Relevant Experiment)

```bash
cd code/NINJA_Attack

# Install dependencies
pip install -r requirements.txt

# Generate long-context test cases at different lengths
python generate_test_cases.py \
    --method_name LongContext \
    --experiment_name my_experiment \
    --method_config configs/method_configs/LongContext_config.yaml

# Generate model completions
python generate_completions.py \
    --model_name llama3.1_8b \
    --experiment_name my_experiment

# Evaluate attack success rates
python evaluate_completions.py \
    --cls_path cais/HarmBench-Llama-2-13b-cls \
    --experiment_name my_experiment
```

### Using HarmBench Behaviors

```python
import pandas as pd

# Load the standard 80-behavior test set
behaviors = pd.read_csv("datasets/harmbench/harmbench_behaviors_text_test.csv")
print(f"Test behaviors: {len(behaviors)}")

# Load AdvBench for broader coverage
advbench = pd.read_csv("datasets/advbench/harmful_behaviors.csv")
print(f"AdvBench behaviors: {len(advbench)}")
```

### Exploring Position Effects (Lost in the Middle)

```python
import json, gzip

# Load 20-document setting with gold at position 0 (beginning)
with gzip.open("datasets/naturalquestions/20_total_documents/nq-open-20_total_documents_gold_at_0.jsonl.gz") as f:
    examples = [json.loads(line) for line in f]
print(f"Examples: {len(examples)}")
print(f"Question: {examples[0]['question']}")
print(f"Documents: {len(examples[0]['ctxs'])}")
```

---

## File Tree Summary

```
adversarial-prompts-abe2-claude/
├── literature_review.md          # Synthesis of findings
├── resources.md                  # This file
├── papers/                       # 17 downloaded PDFs
│   ├── 2511.04707_jailbreaking_in_the_haystack.pdf
│   ├── 2502.04204_short_length_adversarial_training.pdf
│   ├── 2307.03172_lost_in_the_middle.pdf
│   ├── 2404.02151_many_shot_jailbreaking.pdf
│   ├── 2403.14720_spotlighting_defense.pdf
│   ├── ... (12 more)
│   └── pages/                    # PDF chunks for deep reading
├── datasets/                     # 5 datasets (~266 MB)
│   ├── README.md
│   ├── .gitignore
│   ├── verify_datasets.py
│   ├── harmbench/
│   ├── advbench/
│   ├── jailbreakbench/
│   ├── naturalquestions/
│   └── sep/
├── code/                         # 5 cloned repositories
│   ├── README.md
│   ├── NINJA_Attack/
│   ├── adv-icl/
│   ├── llm-adaptive-attacks/
│   ├── HarmBench/
│   └── jailbreakbench/
└── .venv/                        # Virtual environment
```
