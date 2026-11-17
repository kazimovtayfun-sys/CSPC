"""PW3, Tasks 6 and 7: association, confounding, and the chemical mystery.

Run: python chemicals_analysis.py
Input and output files are stored beside this script.
The task comments are retained as a guide to the completed analysis.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


CHEMICALS = ["benzene", "cadmium"]
CONTROLS = ["pollution_index", "age"]


def p_text(p):
    """Avoid printing p = 0 when numerical underflow occurs."""
    return "< 1e-300" if p < 1e-300 else f"= {p:.3g}"


def pearson_result(x, y):
    r, p = stats.pearsonr(x, y)
    return {"r": float(r), "p": float(p), "n": len(x)}


def residualize(values, design):
    """Remove the fitted linear relationship with the control variables."""
    coefficients = np.linalg.lstsq(design, values, rcond=None)[0]
    return np.asarray(values) - design @ coefficients


def partial_correlation(x, y, design):
    """Correlate residuals; account for estimated controls in the t test."""
    x_residual = residualize(x, design)
    y_residual = residualize(y, design)
    r = float(np.corrcoef(x_residual, y_residual)[0, 1])
    n_controls = design.shape[1] - 1  # Exclude the intercept.
    df = len(x) - n_controls - 2
    statistic = r * np.sqrt(df / (1 - r**2))
    p = float(2 * stats.t.sf(abs(statistic), df))
    return {"r": r, "p": p, "df": df, "n": len(x)}, x_residual, y_residual


def adjusted_regression(data):
    """Fit both chemicals and controls; use HC3 robust standard errors.

    HC3 allows the residual variance to change across observations. The t-based
    intervals are approximate; a regression still needs appropriate controls
    and a suitable mean model to support its interpretation.
    """
    names = ["intercept"] + CHEMICALS + CONTROLS
    design = np.column_stack([np.ones(len(data)), data[CHEMICALS + CONTROLS]])
    y = data["malignancy"].to_numpy()
    coefficients = np.linalg.lstsq(design, y, rcond=None)[0]
    residuals = y - design @ coefficients
    inverse = np.linalg.inv(design.T @ design)
    leverage = np.sum((design @ inverse) * design, axis=1)
    weights = (residuals / (1 - leverage)) ** 2
    covariance = inverse @ (design.T @ (design * weights[:, None])) @ inverse
    standard_errors = np.sqrt(np.diag(covariance))
    df = len(y) - design.shape[1]
    critical = stats.t.ppf(0.975, df)
    rows = {}
    for name, coefficient, se in zip(names, coefficients, standard_errors):
        rows[name] = {
            "coefficient": float(coefficient),
            "standard_error_HC3": float(se),
            "ci95": [float(coefficient - critical * se),
                     float(coefficient + critical * se)],
            "p": float(2 * stats.t.sf(abs(coefficient / se), df)),
        }
    return {
        "coefficients": rows,
        "df": df,
        "r_squared": float(1 - np.sum(residuals**2) / np.sum((y - y.mean())**2)),
        "uncertainty_method": "HC3 robust standard errors; approximate t intervals",
    }


def scatter_with_line(ax, x, y, color):
    ax.scatter(x, y, s=16, alpha=0.35, color=color, edgecolors="none")
    slope, intercept = np.polyfit(x, y, 1)
    line_x = np.array([np.min(x), np.max(x)])
    ax.plot(line_x, intercept + slope * line_x, color="#222222", linewidth=1.7)
    ax.grid(alpha=0.16)


def main():
    folder = Path(__file__).resolve().parent
    # Task 6: Load the chemical data and quantify each chemical's naive
    # association with malignancy. Which looks more strongly associated?
    data = pd.read_csv(folder / "chemicals_cancer.csv")
    columns = CHEMICALS + CONTROLS + ["malignancy"]
    if data[columns].isna().any().any():
        raise ValueError("Missing values require an explicit handling decision.")
    y = data["malignancy"].to_numpy()
    naive = {name: pearson_result(data[name], y) for name in CHEMICALS}

    # Task 7: Account for pollution and age, then compare the chemical
    # associations again and explain the difference between association and cause.
    controls = np.column_stack([np.ones(len(data)), data[CONTROLS]])
    adjusted = {}
    residuals = {}
    for name in CHEMICALS:
        adjusted[name], x_residual, y_residual = partial_correlation(
            data[name].to_numpy(), y, controls
        )
        residuals[name] = (x_residual, y_residual)

    pollution_links = {
        name: pearson_result(data["pollution_index"], data[name])
        for name in CHEMICALS + ["malignancy", "age"]
    }
    # A narrow band illustrates the idea but does not remove all confounding.
    band = data[(data["pollution_index"] > 40) & (data["pollution_index"] < 60)]
    band_correlations = {
        name: pearson_result(band[name], band["malignancy"]) for name in CHEMICALS
    }
    regression = adjusted_regression(data)

    results = {
        "shape": list(data.shape),
        "missing_values": {name: int(data[name].isna().sum()) for name in columns},
        "duplicate_rows": int(data.duplicated().sum()),
        "naive_pearson": naive,
        "pollution_pearson": pollution_links,
        "partial_correlations_controls_pollution_and_age": adjusted,
        "pollution_band_40_to_60": band_correlations,
        "adjusted_OLS": regression,
        "p_value_note": "A p value of 0 in JSON means floating-point underflow, not exactly zero.",
        "interpretation": (
            "Benzene is the chemical supported as the intended driver in this synthetic "
            "exercise. Cadmium's strong naive association is explained by pollution. "
            "These observational analyses support that interpretation but cannot prove "
            "causation without the generating mechanism or causal assumptions."
        ),
    }

    lines = ["PW3 chemical-exposure analysis", f"Data shape: {data.shape}",
             f"Missing values: {data[columns].isna().sum().sum()}",
             f"Duplicate rows: {data.duplicated().sum()}", "", "Task 6: naive Pearson correlations"]
    for name, row in naive.items():
        lines.append(f"{name}: r = {row['r']:.6f}, p {p_text(row['p'])}")
    lines += ["", "Pollution links (Pearson correlations)"]
    for name, row in pollution_links.items():
        lines.append(f"pollution vs {name}: r = {row['r']:.6f}, p {p_text(row['p'])}")
    lines += ["", "Task 7: partial correlations controlling pollution_index and age"]
    for name, row in adjusted.items():
        lines.append(f"{name}: partial r = {row['r']:.6f}, p {p_text(row['p'])}, df = {row['df']}")
    lines += ["", f"Restricted pollution band: 40 < pollution_index < 60 (n = {len(band)})"]
    for name, row in band_correlations.items():
        lines.append(f"{name}: r = {row['r']:.6f}, p {p_text(row['p'])}")
    lines.append("Cadmium remains correlated inside this band: restriction alone leaves residual confounding.")
    lines += ["", "OLS: malignancy ~ benzene + cadmium + pollution_index + age",
              "95% confidence intervals use HC3 robust standard errors."]
    for name, row in regression["coefficients"].items():
        low, high = row["ci95"]
        lines.append(f"{name}: coefficient = {row['coefficient']:.6f}, CI [{low:.6f}, {high:.6f}], p {p_text(row['p'])}")
    lines += [f"R squared = {regression['r_squared']:.6f}", "", results["interpretation"]]
    report = "\n".join(lines) + "\n"
    print(report)
    (folder / "chemical_results.txt").write_text(report)
    (folder / "chemical_results.json").write_text(json.dumps(results, indent=2) + "\n")

    # Each column tracks the same chemical before and after adjustment.
    fig, axes = plt.subplots(2, 2, figsize=(11, 8.5), constrained_layout=True)
    colors = {"benzene": "#2a728e", "cadmium": "#c76a32"}
    for col, name in enumerate(CHEMICALS):
        scatter_with_line(axes[0, col], data[name], y, colors[name])
        axes[0, col].set(
            title=f"{name.capitalize()}: naive r = {naive[name]['r']:.3f}",
            xlabel=f"{name.capitalize()} level (data units)", ylabel="Malignancy score",
        )
        x_residual, y_residual = residuals[name]
        scatter_with_line(axes[1, col], x_residual, y_residual, colors[name])
        axes[1, col].set(
            title=f"{name.capitalize()}: adjusted r = {adjusted[name]['r']:.3f}",
            xlabel=f"{name.capitalize()} residual (data units)",
            ylabel="Malignancy residual (score units)",
        )
    fig.suptitle("Chemical associations before and after adjusting for pollution and age", fontsize=14)
    fig.savefig(folder / "chemical_associations.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for ax, name, label in zip(axes, ["cadmium", "malignancy"],
                               ["Cadmium level (data units)", "Malignancy score"]):
        scatter_with_line(ax, data["pollution_index"], data[name], "#55687b")
        ax.set(xlabel="Pollution index", ylabel=label,
               title=f"Pollution vs {name}: r = {pollution_links[name]['r']:.3f}")
    fig.suptitle("Pollution can explain the apparent cadmium association", fontsize=14)
    fig.savefig(folder / "chemical_confounding.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
