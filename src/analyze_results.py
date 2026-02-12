"""
Analyze experimental results: injection success rate vs document length.

Computes statistics, runs hypothesis tests, and generates visualizations.
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

RESULTS_DIR = Path("results")
PLOTS_DIR = RESULTS_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# Plotting style
sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 150


def load_results() -> pd.DataFrame:
    """Load all result files and combine into a single DataFrame."""
    all_results = []
    for f in RESULTS_DIR.glob("results_*.json"):
        with open(f) as fh:
            data = json.load(fh)
            all_results.extend(data)
    df = pd.DataFrame(all_results)
    # Filter out errors
    df = df[df["error"].isna() | (df["error"] == "None") | (df["error"].isnull())]
    print(f"Loaded {len(df)} valid results from {df['model'].nunique()} models")
    return df


def compute_isr_by_condition(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Injection Success Rate by length, position, context_type, model."""
    groups = df.groupby(["model", "length", "position", "context_type"])
    summary = groups.agg(
        total=("injection_success", "count"),
        successes=("injection_success", "sum"),
    ).reset_index()
    summary["isr"] = summary["successes"] / summary["total"]

    # Wilson score 95% CI
    z = 1.96
    n = summary["total"].values.astype(float)
    p = summary["isr"].values.astype(float)
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    summary["ci_lower"] = np.maximum(0, center - spread)
    summary["ci_upper"] = np.minimum(1, center + spread)

    return summary


def compute_isr_by_length(df: pd.DataFrame) -> pd.DataFrame:
    """Compute ISR aggregated by length and model only."""
    groups = df.groupby(["model", "length"])
    summary = groups.agg(
        total=("injection_success", "count"),
        successes=("injection_success", "sum"),
    ).reset_index()
    summary["isr"] = summary["successes"] / summary["total"]

    z = 1.96
    n = summary["total"].values.astype(float)
    p = summary["isr"].values.astype(float)
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    summary["ci_lower"] = np.maximum(0, center - spread)
    summary["ci_upper"] = np.minimum(1, center + spread)

    return summary


def plot_isr_vs_length(df: pd.DataFrame, summary: pd.DataFrame):
    """Main figure: ISR vs document length by model."""
    fig, ax = plt.subplots(figsize=(12, 7))

    models = sorted(summary["model"].unique())
    colors = sns.color_palette("Set2", len(models))
    markers = ["o", "s", "D", "^", "v"]

    for i, model in enumerate(models):
        mdata = summary[summary["model"] == model].sort_values("length")
        yerr_lower = np.maximum(0, (mdata["isr"].values - mdata["ci_lower"].values) * 100)
        yerr_upper = np.maximum(0, (mdata["ci_upper"].values - mdata["isr"].values) * 100)
        ax.errorbar(
            mdata["length"],
            mdata["isr"] * 100,
            yerr=[yerr_lower, yerr_upper],
            label=model,
            marker=markers[i % len(markers)],
            color=colors[i],
            linewidth=2,
            markersize=8,
            capsize=5,
        )

    ax.set_xlabel("Document Length (words)", fontsize=14)
    ax.set_ylabel("Injection Success Rate (%)", fontsize=14)
    ax.set_title("Injection Success Rate vs. Document Length", fontsize=16)
    ax.legend(fontsize=12)
    ax.set_ylim(-5, 105)
    ax.set_xscale("symlog", linthresh=50)
    ax.set_xticks([0, 100, 500, 1000, 2000, 5000, 10000])
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x):,}"))
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "isr_vs_length.png", bbox_inches="tight")
    plt.close()
    print("Saved: isr_vs_length.png")


def plot_isr_by_position(df: pd.DataFrame):
    """ISR by position within document, faceted by length."""
    # Exclude length=0 (no position)
    df_pos = df[df["length"] > 0].copy()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    models = sorted(df_pos["model"].unique())

    for i, model in enumerate(models):
        ax = axes[i]
        mdata = df_pos[df_pos["model"] == model]
        pivot = mdata.groupby(["length", "position"])["injection_success"].mean().reset_index()
        pivot_wide = pivot.pivot(index="length", columns="position", values="injection_success")
        pivot_wide = pivot_wide * 100

        pivot_wide.plot(kind="bar", ax=ax, width=0.8)
        ax.set_title(model, fontsize=14)
        ax.set_xlabel("Document Length (words)", fontsize=12)
        if i == 0:
            ax.set_ylabel("Injection Success Rate (%)", fontsize=12)
        ax.set_ylim(0, 105)
        ax.legend(title="Position", fontsize=10)
        ax.tick_params(axis="x", rotation=45)

    plt.suptitle("Injection Success Rate by Position and Length", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "isr_by_position.png", bbox_inches="tight")
    plt.close()
    print("Saved: isr_by_position.png")


def plot_isr_by_context_type(df: pd.DataFrame):
    """ISR by context type (random vs relevant), faceted by model."""
    df_ctx = df[df["length"] > 0].copy()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    models = sorted(df_ctx["model"].unique())

    for i, model in enumerate(models):
        ax = axes[i]
        mdata = df_ctx[df_ctx["model"] == model]
        pivot = mdata.groupby(["length", "context_type"])["injection_success"].mean().reset_index()
        pivot_wide = pivot.pivot(index="length", columns="context_type", values="injection_success")
        pivot_wide = pivot_wide * 100

        pivot_wide.plot(kind="bar", ax=ax, width=0.8)
        ax.set_title(model, fontsize=14)
        ax.set_xlabel("Document Length (words)", fontsize=12)
        if i == 0:
            ax.set_ylabel("Injection Success Rate (%)", fontsize=12)
        ax.set_ylim(0, 105)
        ax.legend(title="Context Type", fontsize=10)
        ax.tick_params(axis="x", rotation=45)

    plt.suptitle("Injection Success Rate by Context Type and Length", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "isr_by_context_type.png", bbox_inches="tight")
    plt.close()
    print("Saved: isr_by_context_type.png")


def plot_heatmap(df: pd.DataFrame):
    """Heatmap of ISR by model × length."""
    pivot = df.groupby(["model", "length"])["injection_success"].mean().reset_index()
    pivot["injection_success"] = pivot["injection_success"].astype(float)
    heatmap_data = pivot.pivot(index="model", columns="length", values="injection_success") * 100
    heatmap_data = heatmap_data.astype(float)

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn_r",
        vmin=0,
        vmax=100,
        ax=ax,
        cbar_kws={"label": "ISR (%)"},
    )
    ax.set_title("Injection Success Rate (%) by Model and Document Length", fontsize=14)
    ax.set_xlabel("Document Length (words)", fontsize=12)
    ax.set_ylabel("Model", fontsize=12)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "isr_heatmap.png", bbox_inches="tight")
    plt.close()
    print("Saved: isr_heatmap.png")


def run_statistical_tests(df: pd.DataFrame) -> dict:
    """Run statistical tests for hypotheses."""
    results = {}

    # H1: Is there a monotonic relationship between length and ISR?
    for model in df["model"].unique():
        mdata = df[df["model"] == model]
        # Cochran-Armitage trend test approximation via point-biserial correlation
        corr, p_val = stats.pointbiserialr(
            mdata["injection_success"].astype(int),
            mdata["length"],
        )
        results[f"H1_trend_{model}"] = {
            "test": "Point-biserial correlation (length vs. injection_success)",
            "correlation": round(corr, 4),
            "p_value": round(p_val, 6),
            "significant": p_val < 0.05,
        }

    # H2: Position effect (beginning vs middle vs end) for long docs
    for model in df["model"].unique():
        mdata = df[(df["model"] == model) & (df["length"] >= 1000)]
        if mdata["position"].nunique() >= 3:
            groups = [
                mdata[mdata["position"] == pos]["injection_success"].astype(int).values
                for pos in ["beginning", "middle", "end"]
            ]
            # Only run if we have data in all groups
            if all(len(g) > 0 for g in groups):
                stat, p_val = stats.kruskal(*groups)
                results[f"H2_position_{model}"] = {
                    "test": "Kruskal-Wallis (position effect on ISR)",
                    "statistic": round(stat, 4),
                    "p_value": round(p_val, 6),
                    "significant": p_val < 0.05,
                    "group_means": {
                        pos: round(mdata[mdata["position"] == pos]["injection_success"].mean(), 4)
                        for pos in ["beginning", "middle", "end"]
                    },
                }

    # H3: Context type effect (random vs relevant)
    for model in df["model"].unique():
        mdata = df[(df["model"] == model) & (df["length"] > 0)]
        random_data = mdata[mdata["context_type"] == "random"]["injection_success"].astype(int)
        relevant_data = mdata[mdata["context_type"] == "relevant"]["injection_success"].astype(int)
        if len(random_data) > 0 and len(relevant_data) > 0:
            stat, p_val = stats.mannwhitneyu(random_data, relevant_data, alternative="two-sided")
            results[f"H3_context_{model}"] = {
                "test": "Mann-Whitney U (random vs relevant context)",
                "statistic": round(stat, 4),
                "p_value": round(p_val, 6),
                "significant": p_val < 0.05,
                "random_isr": round(random_data.mean(), 4),
                "relevant_isr": round(relevant_data.mean(), 4),
            }

    # H4: Model comparison — chi-squared test for overall ISR differences
    contingency = pd.crosstab(df["model"], df["injection_success"])
    if contingency.shape[1] == 2:
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency)
        results["H4_model_comparison"] = {
            "test": "Chi-squared test (model × injection success)",
            "chi2": round(chi2, 4),
            "p_value": round(p_val, 6),
            "dof": dof,
            "significant": p_val < 0.05,
            "model_isrs": {
                model: round(df[df["model"] == model]["injection_success"].mean(), 4)
                for model in df["model"].unique()
            },
        }

    # Logistic regression (simplified: length as predictor)
    for model in df["model"].unique():
        mdata = df[df["model"] == model]
        if mdata["injection_success"].nunique() > 1:
            X = mdata["length"].values
            y = mdata["injection_success"].astype(int).values
            # Simple logistic regression via statsmodels-free approach
            # Using scipy minimize
            from scipy.optimize import minimize

            def neg_log_likelihood(params):
                b0, b1 = params
                z = b0 + b1 * X / 10000  # Scale length
                p = 1 / (1 + np.exp(-z))
                p = np.clip(p, 1e-10, 1 - 1e-10)
                return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))

            result = minimize(neg_log_likelihood, [0, 0], method="Nelder-Mead")
            b0, b1 = result.x
            results[f"logistic_regression_{model}"] = {
                "test": "Logistic regression: ISR ~ length",
                "intercept": round(b0, 4),
                "length_coefficient": round(b1, 4),
                "interpretation": (
                    f"For every 10,000 word increase, log-odds of injection success "
                    f"{'increase' if b1 > 0 else 'decrease'} by {abs(b1):.4f}"
                ),
            }

    return results


def compute_effect_sizes(df: pd.DataFrame) -> dict:
    """Compute effect sizes for key comparisons."""
    effects = {}

    for model in df["model"].unique():
        mdata = df[df["model"] == model]
        # Effect size: length=0 vs length=10000
        short = mdata[mdata["length"] == 0]["injection_success"].astype(float)
        long = mdata[mdata["length"] == 10000]["injection_success"].astype(float)

        if len(short) > 0 and len(long) > 0:
            mean_diff = long.mean() - short.mean()
            pooled_std = np.sqrt((short.var() + long.var()) / 2)
            cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0

            effects[f"{model}_short_vs_long"] = {
                "short_isr": round(short.mean(), 4),
                "long_isr": round(long.mean(), 4),
                "difference": round(mean_diff, 4),
                "cohens_d": round(cohens_d, 4),
                "interpretation": (
                    "large" if abs(cohens_d) > 0.8 else
                    "medium" if abs(cohens_d) > 0.5 else
                    "small" if abs(cohens_d) > 0.2 else "negligible"
                ),
            }

    return effects


def main():
    df = load_results()
    if len(df) == 0:
        print("No results found. Run experiments first.")
        return

    print(f"\nModels: {df['model'].unique()}")
    print(f"Length conditions: {sorted(df['length'].unique())}")
    print(f"Total valid results: {len(df)}")

    # Overall ISR by model
    print("\n" + "=" * 60)
    print("OVERALL INJECTION SUCCESS RATES")
    print("=" * 60)
    for model in sorted(df["model"].unique()):
        mdata = df[df["model"] == model]
        isr = mdata["injection_success"].mean()
        n = len(mdata)
        print(f"  {model}: {isr*100:.1f}% ({int(isr*n)}/{n})")

    # ISR by length and model
    summary = compute_isr_by_length(df)
    print("\n" + "=" * 60)
    print("ISR BY LENGTH AND MODEL")
    print("=" * 60)
    for model in sorted(summary["model"].unique()):
        print(f"\n  {model}:")
        mdata = summary[summary["model"] == model].sort_values("length")
        for _, row in mdata.iterrows():
            print(f"    {int(row['length']):>6} words: {row['isr']*100:>5.1f}% "
                  f"[{row['ci_lower']*100:.1f}%, {row['ci_upper']*100:.1f}%] "
                  f"(n={int(row['total'])})")

    # Generate plots
    print("\nGenerating plots...")
    plot_isr_vs_length(df, summary)
    plot_heatmap(df)
    plot_isr_by_position(df)
    plot_isr_by_context_type(df)

    # Statistical tests
    print("\n" + "=" * 60)
    print("STATISTICAL TESTS")
    print("=" * 60)
    stat_results = run_statistical_tests(df)
    for name, result in stat_results.items():
        print(f"\n  {name}:")
        for k, v in result.items():
            print(f"    {k}: {v}")

    # Effect sizes
    print("\n" + "=" * 60)
    print("EFFECT SIZES")
    print("=" * 60)
    effects = compute_effect_sizes(df)
    for name, effect in effects.items():
        print(f"\n  {name}:")
        for k, v in effect.items():
            print(f"    {k}: {v}")

    # Save all analysis results
    analysis = {
        "summary_by_length": summary.to_dict(orient="records"),
        "statistical_tests": stat_results,
        "effect_sizes": effects,
        "overall_isr": {
            model: round(df[df["model"] == model]["injection_success"].mean(), 4)
            for model in df["model"].unique()
        },
    }
    with open(RESULTS_DIR / "analysis.json", "w") as f:
        json.dump(analysis, f, indent=2, default=str)
    print(f"\nSaved analysis to {RESULTS_DIR / 'analysis.json'}")


if __name__ == "__main__":
    main()
