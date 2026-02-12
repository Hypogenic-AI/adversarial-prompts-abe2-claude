# Code Repositories for Adversarial Prompt Hiding Research

This directory contains cloned repositories relevant to studying how adversarial prompts
can be hidden in long documents targeting LLMs. All repos were shallow-cloned (`--depth 1`)
to save disk space.

---

## 1. NINJA_Attack

- **URL:** https://github.com/AR-FORUM/NINJA_Attack
- **Paper:** "Jailbreaking in the Haystack: Compute-Optimal Long-Context Attacks on LLMs" (arXiv:2511.04707), ICML 2025 LCFM Workshop
- **Authors:** Rishi Rajesh Shah, Chen Henry Wu, Ziqian Zhong, Alexander Robey, Aditi Raghunathan

### Description
The most directly relevant repository for our research. Implements the NINJA Attack, which
studies how increasing context length affects jailbreak success rates. Built on top of the
HarmBench framework, it adds a `LongContext` attack method that extends adversarial prompts
with surrounding benign context to hide the malicious payload. Supports configurable context
lengths (1K, 2K, 5K, 10K, 15K words) and includes pre-computed results across multiple models.

### Key Files and Directories
- `baselines/longcontext/` -- Core attack implementation (longcontext.py, longcontext_keywords.py, longcontext_ref.py)
- `baselines/manyshot/` -- Many-shot jailbreaking baseline for comparison
- `configs/method_configs/LongContext_config.yaml` -- Configuration for context length, generation model, caching
- `data/behavior_datasets/` -- HarmBench behavior datasets used for evaluation
- `context_cache*/` -- Pre-generated context extensions at various lengths
- `results*/` -- Pre-computed attack results at different context lengths (1000, 10000, 15000 words)
- `compare_context_length.py` -- Scripts for analyzing ASR vs context length
- `gen_and_eval_all.sh` -- Batch evaluation across all configurations
- `generate_test_cases.py`, `generate_completions.py`, `evaluate_completions.py` -- HarmBench pipeline scripts

---

## 2. adv-icl

- **URL:** https://github.com/fshp971/adv-icl
- **Paper:** "Short-length Adversarial Training Helps LLMs Defend Long-length Jailbreak Attacks: Theoretical and Empirical Evidence" (arXiv:2502.04204)
- **Authors:** Shaopeng Fu, Liang Ding, Jingfeng Zhang, Di Wang

### Description
Studies the relationship between adversarial training length and defense effectiveness against
longer attacks. Establishes a sqrt scaling law: adversarial training on short attacks (length k)
provides defense against attacks up to length O(sqrt(k)). Implements adversarial in-context
learning (adv-ICL) training and evaluates against GCG, AutoDAN, and BEAST attacks at various
lengths. Directly relevant to understanding whether short defenses can protect against long
adversarial prompts.

### Key Files and Directories
- `src/adv_trainers/` -- Adversarial training implementation (trainer.py, data.py, evaluator.py)
- `src/attacks/` -- Attack implementations: gcg.py, autodan_zhu.py, beast.py, conti_embed.py
- `src/train.py` -- Main training script
- `src/evaluate.py` -- Evaluation script for measuring defense effectiveness
- `configs/train/` -- Training configurations for different adversarial training setups
- `configs/eval/` -- Evaluation configs per attack type (gcg/, beast/, autodan-zhu/)
- `data/advbench/harmful_behaviors.csv` -- AdvBench harmful behaviors dataset
- `data/harmbench/behavior_datasets/` -- HarmBench test behaviors and adversarial training behaviors
- `scripts/` -- Shell scripts for running training and evaluation experiments

---

## 3. llm-adaptive-attacks

- **URL:** https://github.com/tml-epfl/llm-adaptive-attacks
- **Paper:** "Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks" (arXiv:2404.02151), ICLR 2025
- **Authors:** Maksym Andriushchenko, Francesco Croce, Nicolas Flammarion (EPFL)

### Description
Demonstrates that even state-of-the-art safety-aligned LLMs are vulnerable to simple adaptive
attacks. Achieves nearly 100% attack success rate on GPT-3.5/4, Llama-2 (7B/13B/70B), Gemma-7B,
and adversarially-trained R2D2 using adversarial prompt templates combined with random search on
suffixes. Also demonstrates transfer attacks and prefilling attacks against Claude models. The key
insight is that adaptivity (tailoring attack strategy to each model) is crucial for success.

### Key Files and Directories
- `main.py` -- Main attack script using random search on logprobs (HuggingFace and GPT models)
- `main_claude_prefilling.py` -- Prefilling attack implementation for Claude models
- `main_claude_transfer.py` -- Transfer attack on Claude using GPT-4-derived adversarial suffixes
- `conversers.py` -- Model conversation handling utilities
- `judges.py` -- GPT-4 judge for evaluating attack success
- `prompts.py` -- Adversarial prompt templates (model-specific)
- `harmful_behaviors/harmful_behaviors_pair.csv` -- 50 harmful behaviors from AdvBench used in evaluation
- `jailbreak_artifacts/` -- Pre-computed jailbreak strings for 15+ models (JSON format, JailbreakBench compatible)
- `experiments/` -- Shell scripts for reproducing experiments on each model (exps_llama2_7b.sh, exps_gpt4_turbo.sh, etc.)
- `attack_logs/` -- Full attack logs with intermediate adversarial suffixes

---

## 4. HarmBench

- **URL:** https://github.com/centerforaisafety/HarmBench
- **Paper:** "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal" (arXiv:2402.04249)
- **Authors:** Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, et al.

### Description
The standard benchmark framework for evaluating LLM attacks and defenses. Provides a unified
evaluation pipeline (generate test cases -> generate completions -> evaluate completions) with
support for 18 red teaming methods and 33 target LLMs. Contains the 80 harmful behaviors used
by the NINJA Attack and multiple other papers. Also includes adversarial training code and
classifier models for automated evaluation of attack success.

### Key Files and Directories
- `data/behavior_datasets/` -- Core behavior datasets:
  - `harmbench_behaviors_text_test.csv` -- 80 text-based test behaviors (widely used across papers)
  - `harmbench_behaviors_text_val.csv` -- Validation behaviors
  - `harmbench_behaviors_text_all.csv` -- All behaviors combined
  - `harmbench_behaviors_multimodal_all.csv` -- Multimodal behaviors
- `baselines/` -- 18+ attack implementations:
  - `gcg/`, `autodan/`, `pair/`, `tap/` -- Core optimization-based attacks
  - `direct_request/`, `zeroshot/`, `fewshot/` -- Baseline prompting methods
  - `artprompt/`, `gptfuzz/`, `pap/` -- Advanced attack methods
- `baselines/baseline.py` -- Base class for red teaming methods
- `baselines/model_utils.py` -- Model loading and inference utilities
- `configs/method_configs/` -- YAML configs for each attack method
- `configs/model_configs/models.yaml` -- Model definitions (HuggingFace paths, chat templates)
- `eval_utils.py` -- Evaluation utilities and classifier integration
- `generate_test_cases.py`, `generate_completions.py`, `evaluate_completions.py` -- Pipeline scripts
- `adversarial_training/` -- Code for adversarial training of robust models
- `notebooks/` -- Jupyter notebooks for running classifiers

---

## 5. jailbreakbench

- **URL:** https://github.com/JailbreakBench/jailbreakbench
- **Paper:** "JailbreakBench: An Open Robustness Benchmark for Jailbreaking Language Models" (arXiv:2404.01318), NeurIPS 2024 Datasets and Benchmarks Track
- **Authors:** Patrick Chao, Edoardo Debenedetti, Alexander Robey, Maksym Andriushchenko, et al.

### Description
A standardized, open-source benchmark for evaluating jailbreaking attacks and defenses. Provides
the JBB-Behaviors dataset with 100 harmful and 100 benign behaviors sourced from AdvBench,
HarmBench, and the Trojan Detection Challenge. Includes a leaderboard, artifact repository for
submitted jailbreak strings, and implementations of defense algorithms (SmoothLLM, perplexity
filtering, synonym substitution). Also provides Llama3-based judges for automated evaluation.

### Key Files and Directories
- `src/jailbreakbench/dataset.py` -- Dataset loading (100 harmful + 100 benign behaviors)
- `src/jailbreakbench/artifact.py` -- Loading/submitting jailbreak artifacts
- `src/jailbreakbench/classifier.py` -- Llama3 70B jailbreak judge and Llama3 8B refusal judge
- `src/jailbreakbench/config.py` -- Model and benchmark configuration
- `src/jailbreakbench/defenses/` -- Defense implementations:
  - `smooth_llm.py` -- SmoothLLM defense (Robey et al., 2023)
  - `perplexity_filter.py` -- Perplexity-based filtering (Jain et al., 2023)
  - `synonym_substitution.py` -- Synonym substitution defense
  - `erase_and_check.py` -- Erase-and-check defense
  - `remove_non_dictionary.py` -- Non-dictionary word removal
  - `defenselib/perturbations.py` -- Perturbation primitives for defenses
- `src/jailbreakbench/llm/` -- LLM wrappers (vLLM, LiteLLM) for querying models
- `src/jailbreakbench/submission.py` -- Submission formatting for leaderboard
- `examples/prompts/` -- Example jailbreak prompts (llama2.json, vicuna.json)
- `pyproject.toml` -- Package configuration (installable via pip)

---

## Cross-Repository Connections

These repositories are deeply interconnected:

1. **NINJA_Attack** is built directly on top of **HarmBench**, sharing the same evaluation
   pipeline and behavior datasets. It adds the `LongContext` method as a new baseline.

2. **adv-icl** evaluates against attacks from the **HarmBench** ecosystem (GCG, AutoDAN, BEAST)
   and uses both AdvBench and HarmBench behavior datasets.

3. **llm-adaptive-attacks** exports jailbreak artifacts in **JailbreakBench** format and uses
   the same 50-behavior subset from AdvBench that is also part of **HarmBench**.

4. **JailbreakBench** sources its 100 behaviors from AdvBench, **HarmBench**, and the Trojan
   Detection Challenge, providing a unified evaluation layer.

5. The `harmful_behaviors.csv` from AdvBench appears (in full or subset) across all five repos,
   providing a common evaluation basis.

## Relevance to Our Research Question

> "Is it easier or harder to hide adversarial prompts in longer documents?"

| Repository | Relevance |
|---|---|
| **NINJA_Attack** | Directly answers this -- measures ASR at 1K-15K word context lengths |
| **adv-icl** | Provides theoretical framework (sqrt scaling law) for short-vs-long attack/defense tradeoffs |
| **llm-adaptive-attacks** | Establishes ASR baselines with adaptive attacks (model-specific prompt templates + suffix optimization) |
| **HarmBench** | Standard evaluation framework and behavior datasets used across all experiments |
| **JailbreakBench** | Complementary benchmark with defense implementations for measuring robustness |
