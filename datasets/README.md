# Datasets for Adversarial Prompt Hiding in Long Documents

This directory contains datasets used for research on adversarial prompt hiding
in long documents for LLMs. These datasets support experiments on:

- Evaluating adversarial prompt attack success rates
- Testing how document length affects attack effectiveness
- Benchmarking defense mechanisms
- Measuring instruction-data separation in LLMs
- Analyzing position bias in long-context retrieval

## Dataset Summary

| Dataset | Size | Examples | Primary Use |
|---------|------|----------|-------------|
| HarmBench | 238 KB | 400 behaviors (320 test / 80 val) | Standardized red teaming evaluation |
| AdvBench | 46 KB | 520 harmful behaviors + 574 harmful strings | Universal adversarial attack benchmarking |
| JailbreakBench | 186 KB | 100 harmful + 100 benign behaviors | Jailbreak robustness evaluation |
| NaturalQuestions / Lost in the Middle | 262 MB | 2,655 QA pairs x multiple configs | Position bias in long contexts |
| SEP | 4 MB | 9,160 examples | Instruction-data separation |

**Total size on disk: ~266 MB**

---

## 1. HarmBench

**Directory:** `harmbench/`

A standardized evaluation framework for automated red teaming and robust refusal
of LLMs. Contains 400 harmful text behaviors categorized by functional and
semantic categories.

### Files

| File | Rows | Description |
|------|------|-------------|
| `harmbench_behaviors_text_all.csv` | 400 | All text-based harmful behaviors |
| `harmbench_behaviors_text_test.csv` | 320 | Test split (used for evaluation) |
| `harmbench_behaviors_text_val.csv` | 80 | Validation split |

### Schema

- `Behavior`: The harmful behavior description/instruction
- `FunctionalCategory`: Functional classification (e.g., standard, contextual)
- `SemanticCategory`: Semantic topic area
- `Tags`: Additional metadata tags
- `ContextString`: Optional context for contextual behaviors
- `BehaviorID`: Unique identifier

### Source

- **Paper:** Mazeika et al., "HarmBench: A Standardized Evaluation Framework for
  Automated Red Teaming and Robust Refusal" (arXiv:2402.04249, 2024)
- **GitHub:** https://github.com/centerforaisafety/HarmBench
- **Website:** https://www.harmbench.org
- **License:** MIT

### Relevance to Our Research

HarmBench provides the standard 80-behavior test set used by the NINJA attack
paper and the adaptive attacks paper for evaluating adversarial prompt success
rates when hidden in longer contexts.

---

## 2. AdvBench

**Directory:** `advbench/`

A dataset of 520 harmful behaviors formulated as instructions, from the
"Universal and Transferable Adversarial Attacks on Aligned Language Models"
(GCG attack) paper.

### Files

| File | Rows | Description |
|------|------|-------------|
| `harmful_behaviors.csv` | 520 | Harmful behavior instructions with target completions |
| `harmful_strings.csv` | 574 | Target harmful output strings |

### Schema (harmful_behaviors.csv)

- `goal`: The harmful instruction/request
- `target`: The target completion that constitutes a successful attack

### Source

- **Paper:** Zou et al., "Universal and Transferable Adversarial Attacks on
  Aligned Language Models" (arXiv:2307.15043, 2023)
- **GitHub:** https://github.com/llm-attacks/llm-attacks
- **HuggingFace:** https://huggingface.co/datasets/walledai/AdvBench
- **License:** MIT

### Relevance to Our Research

AdvBench is the foundational harmful behaviors dataset used by most adversarial
attack papers. The adaptive attacks paper and short-length adversarial training
papers both use AdvBench for evaluating attack transferability across document
lengths.

---

## 3. JailbreakBench (JBB-Behaviors)

**Directory:** `jailbreakbench/`

A curated benchmark of 100 distinct misuse behaviors for evaluating jailbreak
attacks and defenses, sourced from AdvBench and TDC/HarmBench with original
additions, organized by OpenAI usage policy categories.

### Files

| File | Rows | Description |
|------|------|-------------|
| `harmful-behaviors.csv` | 100 | Harmful misuse behaviors with categories and sources |
| `benign-behaviors.csv` | 100 | Benign behaviors for measuring overrefusal |
| `judge-comparison.csv` | 300 | Human and automated judge comparison data |

### Schema (harmful-behaviors.csv)

- `Index`: Behavior index
- `Goal`: The harmful goal/request
- `Target`: Target response prefix
- `Behavior`: Behavior description
- `Category`: OpenAI usage policy category (10 categories)
- `Source`: Original source (AdvBench, TDC/HarmBench, or original)

### Source

- **Paper:** Chao et al., "JailbreakBench: An Open Robustness Benchmark for
  Jailbreaking Language Models" (NeurIPS 2024, Datasets and Benchmarks Track)
- **GitHub:** https://github.com/JailbreakBench/jailbreakbench
- **HuggingFace:** https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors
- **License:** MIT

### Relevance to Our Research

JailbreakBench provides a carefully curated superset that combines the most
relevant behaviors from AdvBench and HarmBench with systematic category
coverage. The benign behaviors enable measuring overrefusal rates, which is
important for evaluating whether defenses against adversarial prompts in long
documents degrade normal functionality.

---

## 4. NaturalQuestions-Open / Lost in the Middle

**Directory:** `naturalquestions/`

Multi-document QA data from the "Lost in the Middle" paper, which demonstrates
that LLM performance degrades when relevant information is placed in the middle
of long contexts (U-shaped performance curve). Also includes the raw NQ-Open
question-answer pairs and key-value retrieval data.

### Files

**NQ-Open raw data (HuggingFace parquet):**

| File | Size | Description |
|------|------|-------------|
| `nq_open_train.parquet` | 4.3 MB | 87,925 training QA pairs |
| `nq_open_validation.parquet` | 0.2 MB | 3,610 validation QA pairs |

**Lost in the Middle - Multi-document QA:**

| File | Examples | Description |
|------|----------|-------------|
| `nq-open-oracle.jsonl.gz` | 2,655 | Oracle setting (1 gold document) |
| `10_total_documents/nq-open-10_total_documents_gold_at_{0,4,9}.jsonl.gz` | 2,655 each | 10-doc setting, gold at positions 0/4/9 |
| `20_total_documents/nq-open-20_total_documents_gold_at_{0,4,9,14,19}.jsonl.gz` | 2,655 each | 20-doc setting, gold at 5 positions |
| `30_total_documents/nq-open-30_total_documents_gold_at_{0,4,9,14,19,24,29}.jsonl.gz` | 2,655 each | 30-doc setting, gold at 7 positions |

**Key-Value Retrieval:**

| File | Examples | Description |
|------|----------|-------------|
| `kv_retrieval_data/kv-retrieval-75_keys.jsonl.gz` | 500 | 75-key retrieval tasks |
| `kv_retrieval_data/kv-retrieval-140_keys.jsonl.gz` | 500 | 140-key retrieval tasks |
| `kv_retrieval_data/kv-retrieval-300_keys.jsonl.gz` | 500 | 300-key retrieval tasks |

### Schema (multi-document QA, JSONL)

- `question`: The natural language question
- `answers`: List of valid answer strings
- `ctxs`: List of document contexts (each with `title`, `text`, `hasanswer`, etc.)
- `nq_annotated_gold`: Whether this is an NQ-annotated gold passage

### Download Scripts

- `download_nq_open.py`: Downloads the full NQ-Open dataset via HuggingFace
  datasets library (requires `pip install datasets`)
- `download_retrieved_documents.sh`: Downloads the ~1.3 GB pre-retrieved
  Contriever-MSMARCO documents file for generating custom position experiments

### Source

- **Paper:** Liu et al., "Lost in the Middle: How Language Models Use Long
  Contexts" (TACL, 2024; arXiv:2307.03172)
- **GitHub:** https://github.com/nelson-liu/lost-in-the-middle
- **NQ-Open HuggingFace:** https://huggingface.co/datasets/google-research-datasets/nq_open
- **License:** CC BY-SA 3.0 (NQ-Open)

### Relevance to Our Research

This dataset directly supports experiments on how document length and position
affect LLM attention and performance. The multi-document QA setup with varying
gold document positions is the ideal testbed for studying whether adversarial
prompts are more effective when hidden at specific positions within long
documents. The U-shaped performance curve (better at beginning and end, worse in
the middle) suggests adversarial prompts may be harder to detect when placed in
the middle of long contexts.

---

## 5. SEP Dataset (Instruction-Data Separation)

**Directory:** `sep/`

A benchmark dataset for measuring whether LLMs can separate instructions from
data, from the paper "Can LLMs Separate Instructions From Data? And What Do We
Even Mean By That?"

### Files

| File | Examples | Description |
|------|----------|-------------|
| `SEP_dataset.json` | 9,160 | Full SEP benchmark dataset |

### Schema

Each example contains:
- `system_prompt_clean`: System prompt without injected instruction
- `system_prompt_instructed`: System prompt with injected instruction (probe)
- `prompt_clean`: User data prompt without injected instruction
- `prompt_instructed`: User data prompt with injected instruction (probe)
- `witness`: Expected output when the probe instruction is followed
- `info`: Metadata dictionary containing:
  - `type`: Task category (e.g., "Analytical and Evaluative Tasks")
  - `subtask`: Specific subtask name
  - `subtask_descr`: Subtask description
  - `appended_task_id`: Task identifier
  - `appended_type`: Type of appended task
  - `is_insistent`: Whether the probe uses insistent phrasing

### Source

- **Paper:** Gozverev et al., "Can LLMs Separate Instructions From Data? And What
  Do We Even Mean By That?" (ICLR 2025; arXiv:2403.06833)
- **GitHub:** https://github.com/egozverev/Should-It-Be-Executed-Or-Processed
- **License:** See repository

### Relevance to Our Research

The SEP dataset directly measures a model's ability to distinguish between
instructions it should execute and data it should process -- the fundamental
capability that adversarial prompt injection attacks exploit. By testing whether
models follow injected instructions in data fields, it quantifies the exact
vulnerability that makes adversarial prompt hiding in long documents possible.
The dataset includes both "clean" (no injection) and "instructed" (with
injection) variants, enabling controlled experiments on separation failure rates.

---

## Verification

Run the verification script to check all datasets are present and valid:

```bash
python verify_datasets.py
```

## .gitignore Policy

- CSV files are committed to git (small enough)
- Parquet files, JSONL files, and large JSON files are git-ignored
- Download scripts are committed for reproducibility
- The `download_retrieved_documents.sh` script can fetch the ~1.3 GB
  Contriever-MSMARCO file if needed for custom experiments
