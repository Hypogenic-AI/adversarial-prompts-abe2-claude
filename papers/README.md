# Downloaded Papers

17 papers downloaded from arXiv, organized by relevance to the research question: "Is it easier or harder to hide adversarial prompts in longer documents?"

## Papers

| # | File | Title | arXiv | Size |
|---|------|-------|-------|------|
| 1 | `2511.04707_jailbreaking_in_the_haystack.pdf` | Jailbreaking in the Haystack (NINJA Attack) | 2511.04707 | 3.4 MB |
| 2 | `2502.04204_short_length_adversarial_training.pdf` | Short-length Adversarial Training | 2502.04204 | 1.1 MB |
| 3 | `2307.03172_lost_in_the_middle.pdf` | Lost in the Middle | 2307.03172 | 748 KB |
| 4 | `2404.02151_many_shot_jailbreaking.pdf` | Adaptive Attacks on Safety-Aligned LLMs | 2404.02151 | 1.9 MB |
| 5 | `2403.14720_spotlighting_defense.pdf` | Spotlighting Defense | 2403.14720 | 383 KB |
| 6 | `2403.06833_can_llms_separate_instructions_data.pdf` | Can LLMs Separate Instructions from Data? (SEP) | 2403.06833 | 531 KB |
| 7 | `2302.12173_indirect_prompt_injection.pdf` | Indirect Prompt Injection (XPIA) | 2302.12173 | 7.3 MB |
| 8 | `2512.03001_invasive_context_engineering.pdf` | Invasive Context Engineering | 2512.03001 | 144 KB |
| 9 | `2312.02780_scaling_laws_adversarial_activations.pdf` | Scaling Laws for Adversarial Activations | 2312.02780 | 1.7 MB |
| 10 | `2305.14950_adversarial_demonstration_attacks.pdf` | Adversarial Demonstration Attacks | 2305.14950 | 1.5 MB |
| 11 | `2410.05451_secalign.pdf` | SecAlign | 2410.05451 | 907 KB |
| 12 | `2502.15609_robustness_context_hijacking.pdf` | Robustness to Context Hijacking | 2502.15609 | 2.4 MB |
| 13 | `2503.10566_aside.pdf` | ASIDE: Architectural Separation | 2503.10566 | 1.1 MB |
| 14 | `2505.16957_invisible_prompts_font_injection.pdf` | Invisible Prompts (Font Injection) | 2505.16957 | 1.8 MB |
| 15 | `2507.05093_hidden_threat_rag.pdf` | Hidden Threat in RAG | 2507.05093 | 862 KB |
| 16 | `2508.20863_publish_to_perish.pdf` | Publish to Perish (Peer Review Injection) | 2508.20863 | 1.1 MB |
| 17 | `2410.09102_instructional_segment_embedding.pdf` | Instructional Segment Embedding | 2410.09102 | 6.9 MB |

## Deep-Read Papers

The following 5 papers were read in depth with detailed notes extracted:

1. **NINJA Attack (2511.04707)** — ASR increases with context length (23.7% → 58.8%). Position at beginning most effective. Relevant context > random. Compute-optimal: longer context beats more trials.
2. **Lost in the Middle (2307.03172)** — U-shaped attention curve. Models struggle with info in middle of long contexts.
3. **Spotlighting (2403.14720)** — Delimiting/datamarking/encoding reduce ASR from >50% to <2%.
4. **Short-length AT (2502.04204)** — √M scaling law: defending against length-M attacks requires only √M training length.
5. **Adaptive Attacks (2404.02151)** — 100% ASR on 21 models. Optimal suffix length ~25 tokens (U-shaped).

## Subdirectory: pages/

Contains PDF chunks (3 pages each) created for deep reading with `pypdf`. Used during the literature review process.
