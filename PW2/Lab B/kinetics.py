"""PW2 Lab B, Part 3: fit a first-order rate constant to measured data.

Run: python kinetics.py
The CSV is read from this script's folder; kinetics.png is saved there too.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


def main():
    folder = Path(__file__).resolve().parent
    data = np.genfromtxt(folder / "kinetics.csv", delimiter=",", names=True)
    t = data["time"]
    C = data["concentration"]
    C0 = C[0]

    def total_error(k):
        """Sum of squared residuals for C(t) = C0 * exp(-k*t)."""
        predicted = C0 * np.exp(-k * t)
        return np.sum((C - predicted) ** 2)

    result = minimize(
        total_error,
        x0=[0.5],
        method="SLSQP",
        bounds=[(0, 5)],
        options={"ftol": 1e-10, "maxiter": 1000},
    )
    if not result.success:
        raise RuntimeError(f"Rate fit failed: {result.message}")

    k_fit = float(result.x[0])
    sse = float(total_error(k_fit))
    rmse = np.sqrt(sse / len(t))
    print(f"Initial concentration C0 = {C0:.3f}")
    print(f"Fitted rate constant k = {k_fit:.8f} (inverse time units)")
    print(f"Sum of squared errors = {sse:.6f}")
    print(f"Root-mean-square error = {rmse:.6f}")

    t_curve = np.linspace(t.min(), t.max(), 400)
    C_curve = C0 * np.exp(-k_fit * t_curve)
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.scatter(t, C, color="#174a6e", s=32, label="Measured data", zorder=3)
    ax.plot(
        t_curve,
        C_curve,
        color="#d56727",
        linewidth=2.3,
        label=f"First-order fit: k = {k_fit:.5f}",
    )
    ax.axhline(0, color="0.65", linewidth=0.8)
    ax.set(
        xlabel="Time (data units)",
        ylabel="Concentration (data units)",
        title="First-order reaction: measured data and fitted decay",
    )
    ax.grid(alpha=0.2)
    ax.legend(frameon=False)
    plot_path = folder / "kinetics.png"
    fig.savefig(plot_path, dpi=180)
    plt.close(fig)
    print(f"Saved {plot_path.name}")


if __name__ == "__main__":
    main()
