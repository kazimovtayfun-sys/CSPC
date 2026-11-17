"""PW3, Tasks 1-5 and bonus: distributions and comparisons in heart data.

Run: python heart_analysis.py
Reads heart.csv and saves plots and results beside this script.
Source: https://www.kaggle.com/datasets/ritwikb3/heart-disease-cleveland
Target coding: 0 = no heart disease, 1 = heart disease.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


CONTINUOUS = ["age", "chol", "trestbps", "thalach"]
LABELS = {
    "age": "Age (years)",
    "chol": "Cholesterol (mg/dL)",
    "trestbps": "Resting blood pressure (mmHg)",
    "thalach": "Maximum heart rate (beats/min)",
}
COLORS = {0: "#246487", 1: "#c66a38"}
GROUP_LABELS = {0: "No disease", 1: "Disease"}


def normality_summary(values):
    """Summarize shape and test the hypothesis of a normal distribution."""
    test = stats.shapiro(values)
    return {
        "n": int(len(values)),
        "mean": float(np.mean(values)),
        "sd": float(np.std(values, ddof=1)),
        "median": float(np.median(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "skewness": float(stats.skew(values, bias=False)),
        "shapiro_W": float(test.statistic),
        "shapiro_p": float(test.pvalue),
    }


def mean_summary(values):
    """Student-t 95% interval for a group mean, with sample SD and SEM."""
    n = len(values)
    mean = np.mean(values)
    sd = np.std(values, ddof=1)
    sem = sd / np.sqrt(n)
    margin = stats.t.ppf(0.975, df=n - 1) * sem
    return {
        "n": int(n), "mean": float(mean), "sd": float(sd),
        "sem": float(sem), "ci95_low": float(mean - margin),
        "ci95_high": float(mean + margin),
    }


def main():
    folder = Path(__file__).resolve().parent
    report = []

    def log(message):
        print(message)
        report.append(str(message))

    # Task 1: Load heart.csv with pandas, print its shape and first rows,
    # and isolate age, chol, trestbps, and thalach.
    data = pd.read_csv(folder / "heart.csv", encoding="utf-8-sig")
    log(f"Data shape: {data.shape}")
    log("First five rows:\n" + data.head().to_string(index=False))
    log("Missing values per column:\n" + data.isna().sum().to_string())
    log(f"Exact duplicate rows: {data.duplicated().sum()}")
    required = CONTINUOUS + ["target"]
    clean = data.dropna(subset=required).copy()
    if set(clean["target"].unique()) != {0, 1}:
        raise ValueError("Expected target coding 0 = no disease and 1 = disease.")
    log(f"Rows omitted for missing analysis variables: {len(data) - len(clean)}")
    continuous = clean[CONTINUOUS]
    log("Continuous-variable summary:\n" + continuous.describe().to_string())
    results = {
        "shape": list(data.shape),
        "missing_values": {key: int(value) for key, value in data.isna().sum().items()},
        "duplicates": int(data.duplicated().sum()),
        "rows_used": int(len(clean)),
        "target_coding": {"0": "No disease", "1": "Disease"},
    }

    # Task 2: Visualize and describe the distribution of each continuous variable.
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    for ax, column in zip(axes.flat, CONTINUOUS):
        values = continuous[column].to_numpy()
        ax.hist(values, bins="fd", density=True, color="#246487", alpha=0.75,
                edgecolor="white", label="Observed distribution")
        grid = np.linspace(values.min(), values.max(), 300)
        ax.plot(grid, stats.norm.pdf(grid, values.mean(), values.std(ddof=1)),
                color="#c66a38", linewidth=2, label="Normal reference")
        ax.set(xlabel=LABELS[column], ylabel="Density")
        ax.grid(axis="y", alpha=0.2)
    axes[0, 0].legend(frameon=False, fontsize=9)
    fig.suptitle("Heart data: four continuous distributions", fontsize=15)
    fig.savefig(folder / "heart_distributions.png", dpi=180)
    plt.close(fig)

    # Task 3: Assess approximate normality with Q-Q plots and Shapiro-Wilk tests.
    # These are descriptive diagnostics; a small p-value is not an effect size.
    results["normality"] = {}
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    for ax, column in zip(axes.flat, CONTINUOUS):
        values = continuous[column].to_numpy()
        summary = normality_summary(values)
        results["normality"][column] = summary
        (theoretical, observed), (slope, intercept, _) = stats.probplot(values)
        ax.scatter(theoretical, observed, color="#246487", s=16, alpha=0.7)
        ax.plot(theoretical, intercept + slope * theoretical,
                color="#c66a38", linewidth=2)
        ax.set(xlabel="Theoretical normal quantile", ylabel=LABELS[column],
               title=f"{column}: Shapiro p = {summary['shapiro_p']:.3g}")
        ax.grid(alpha=0.2)
        log(f"{column}: W={summary['shapiro_W']:.6f}, "
            f"p={summary['shapiro_p']:.6g}, skew={summary['skewness']:.6f}")
    fig.suptitle("Normal Q-Q plots: departures from the line reveal non-normality", fontsize=14)
    fig.savefig(folder / "heart_qq.png", dpi=180)
    plt.close(fig)

    # Task 4: Compare maximum heart rate between target groups and report
    # group means with uncertainty. Check each group's distribution as well.
    groups = {value: clean.loc[clean["target"] == value, "thalach"].to_numpy()
              for value in (0, 1)}
    results["groups"] = {}
    for value, values in groups.items():
        summary = mean_summary(values)
        summary["normality"] = normality_summary(values)
        results["groups"][str(value)] = summary
        log(f"{GROUP_LABELS[value]}: n={summary['n']}, mean={summary['mean']:.6f}, "
            f"SD={summary['sd']:.6f}, SEM={summary['sem']:.6f}, "
            f"95% CI=[{summary['ci95_low']:.6f}, {summary['ci95_high']:.6f}], "
            f"Shapiro p={summary['normality']['shapiro_p']:.6g}")

    # Welch directly tests the difference in means without equal-variance
    # assumptions. Large independent groups make mean inference reasonably
    # robust to the observed non-normality. Mann-Whitney is a rank sensitivity
    # analysis; it is not generally a test of equal means or equal medians.
    healthy, disease = groups[0], groups[1]
    welch = stats.ttest_ind(disease, healthy, equal_var=False)
    difference = disease.mean() - healthy.mean()
    variance_terms = [np.var(values, ddof=1) / len(values)
                      for values in (disease, healthy)]
    standard_error = np.sqrt(sum(variance_terms))
    df = sum(variance_terms) ** 2 / sum(
        term ** 2 / (len(values) - 1)
        for term, values in zip(variance_terms, (disease, healthy))
    )
    margin = stats.t.ppf(0.975, df) * standard_error
    rank_test = stats.mannwhitneyu(disease, healthy, alternative="two-sided",
                                  method="asymptotic")
    results["comparison"] = {
        "difference_direction": "Disease minus no disease",
        "mean_difference": float(difference),
        "difference_sem": float(standard_error),
        "difference_ci95_low": float(difference - margin),
        "difference_ci95_high": float(difference + margin),
        "welch_t": float(welch.statistic), "welch_df": float(df),
        "welch_p": float(welch.pvalue),
        "mann_whitney_U": float(rank_test.statistic),
        "mann_whitney_p": float(rank_test.pvalue),
    }
    log(f"Welch t={welch.statistic:.6f}, df={df:.6f}, p={welch.pvalue:.6g}")
    log(f"Mean difference (disease - no disease)={difference:.6f} beats/min; "
        f"95% CI=[{difference-margin:.6f}, {difference+margin:.6f}]")
    log(f"Mann-Whitney sensitivity: U={rank_test.statistic:.6f}, "
        f"two-sided p={rank_test.pvalue:.6g}")

    fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
    for value in (0, 1):
        summary = results["groups"][str(value)]
        ax.errorbar(value, summary["mean"],
                    yerr=[[summary["mean"] - summary["ci95_low"]],
                          [summary["ci95_high"] - summary["mean"]]],
                    fmt="o", markersize=9, capsize=7, linewidth=2.3,
                    color=COLORS[value])
        ax.annotate(f"{summary['mean']:.2f}", (value, summary["ci95_high"]),
                    xytext=(0, 12), textcoords="offset points", ha="center")
    ax.set(xticks=[0, 1],
           xticklabels=[f"{GROUP_LABELS[value]}\n(n = {len(groups[value])})"
                        for value in (0, 1)],
           ylabel="Mean maximum heart rate (beats/min)",
           title="Mean maximum heart rate with 95% confidence intervals",
           xlim=(-0.6, 1.6))
    ax.margins(y=0.25)
    ax.grid(axis="y", alpha=0.2)
    fig.savefig(folder / "heart_group_means.png", dpi=180)
    plt.close(fig)

    # Task 5: Quantify and plot the relationship between age and maximum heart rate.
    # Spearman measures monotonic association and is less sensitive to outliers.
    spearman = stats.spearmanr(clean["age"], clean["thalach"])
    pearson = stats.pearsonr(clean["age"], clean["thalach"])
    results["age_thalach"] = {
        "n": int(len(clean)), "spearman_rho": float(spearman.statistic),
        "spearman_p": float(spearman.pvalue),
        "pearson_r": float(pearson.statistic), "pearson_p": float(pearson.pvalue),
    }
    log(f"Age vs thalach: Spearman rho={spearman.statistic:.6f}, "
        f"p={spearman.pvalue:.6g}; Pearson r={pearson.statistic:.6f}, "
        f"p={pearson.pvalue:.6g}")
    fig, ax = plt.subplots(figsize=(8, 5.5), constrained_layout=True)
    for value in (0, 1):
        group = clean[clean["target"] == value]
        ax.scatter(group["age"], group["thalach"], color=COLORS[value],
                   alpha=0.65, s=28, label=GROUP_LABELS[value])
    ax.set(xlabel=LABELS["age"], ylabel=LABELS["thalach"],
           title=f"Age and maximum heart rate: Spearman rho = {spearman.statistic:.3f}")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.savefig(folder / "age_thalach.png", dpi=180)
    plt.close(fig)

    # Bonus: Quantify category balance using Shannon entropy in bits.
    proportions = clean["target"].value_counts(normalize=True).sort_index()
    entropy = -np.sum(proportions * np.log2(proportions))
    results["target_entropy"] = {
        "counts": {str(key): int(value) for key, value in clean["target"].value_counts().items()},
        "proportions": {str(key): float(value) for key, value in proportions.items()},
        "entropy_bits": float(entropy), "maximum_binary_entropy_bits": 1.0,
    }
    log(f"Target proportions: {proportions.to_dict()}")
    log(f"Target Shannon entropy = {entropy:.6f} bits (binary maximum = 1 bit)")
    log("Interpretation assumes independent patients; these associations do not establish causation.")
    (folder / "heart_results.json").write_text(json.dumps(results, indent=2) + "\n")
    (folder / "heart_results.txt").write_text("\n\n".join(report) + "\n")


if __name__ == "__main__":
    main()
