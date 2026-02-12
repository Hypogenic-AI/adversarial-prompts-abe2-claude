# Is It Easier or Harder to Hide Adversarial Prompts in Longer Documents?

An empirical study testing whether document length affects the effectiveness of adversarial prompt injection across frontier LLMs.

## Key Findings

- **The answer is model-dependent.** There is no universal relationship between document length and injection success.
- **Gemini 2.5 Flash**: Longer documents *help* attackers (ISR rises from 87.5% at 100 words to 98.1% at 10K words, p=0.032)
- **GPT-4.1-mini**: Longer documents *hinder* attackers (ISR falls from 86.7% to 80.8%, p=0.026)
- **Claude Sonnet 4**: Complete immunity -- 0% injection success rate across all 142 trials at all document lengths
- **Model choice matters most**: The difference between models (0%-94.5%) dwarfs the effect of document length (max ~19pp within a model)
- **Position matters for GPT**: Injections at the beginning of documents are most effective (93.1% vs 79.4% in middle)

## Quick Reproduction

```bash
# Set up environment
uv venv && source .venv/bin/activate
uv pip install openai httpx numpy pandas matplotlib seaborn scipy tqdm

# Generate test cases
python src/generate_documents.py

# Run experiments (requires API keys as environment variables)
export OPENAI_API_KEY=your_key
export OPENROUTER_KEY=your_key
python src/run_single_model.py gpt-4.1-mini
python src/run_single_model.py gemini-2.5-flash
python src/run_single_model.py claude-sonnet-4

# Analyze results
python src/analyze_results.py
```

## File Structure

```
.
├── REPORT.md                      # Full research report with results
├── README.md                      # This file
├── planning.md                    # Research plan and methodology
├── literature_review.md           # Literature synthesis
├── resources.md                   # Resource catalog
├── src/
│   ├── generate_documents.py      # Test case generation
│   ├── run_experiment.py          # Main experiment runner
│   ├── run_single_model.py        # Single-model runner
│   └── analyze_results.py         # Statistical analysis and plotting
├── results/
│   ├── test_cases.json            # Generated test cases
│   ├── results_gpt_4_1_mini.json  # GPT-4.1-mini raw results
│   ├── results_gemini_2_5_flash.json  # Gemini raw results
│   ├── results_claude_sonnet_4.json   # Claude raw results
│   ├── analysis.json              # Statistical analysis output
│   ├── config.json                # Experiment configuration
│   └── plots/
│       ├── isr_vs_length.png      # Main result: ISR vs document length
│       ├── isr_heatmap.png        # ISR heatmap by model x length
│       ├── isr_by_position.png    # Position effects
│       └── isr_by_context_type.png # Context type effects
├── papers/                        # 17 research papers (PDFs)
├── datasets/                      # HarmBench, AdvBench, SEP, etc.
└── code/                          # NINJA, HarmBench, and other repos
```

## Method

We embedded 20 distinct benign instruction injections (each with a unique codeword) within documents of 7 different lengths (0-10,000 words). The system prompt asked models to summarize the document; if the model output the codeword instead, the injection was counted as successful. This measures the same instruction-data confusion mechanism that underlies all prompt injection attacks, without generating harmful content.

See [REPORT.md](REPORT.md) for full details.
