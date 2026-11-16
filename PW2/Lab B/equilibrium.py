"""PW2 Lab B Part 4: solve H2 + I2 <=> 2 HI at equilibrium.

Run with: python equilibrium.py
The plot is saved beside this script.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize


K = 15.6
a = b = 1.0  # Initial amounts of H2 and I2, in mol.


def k_imbalance(x):
    """Return zero when the reaction quotient equals K."""
    return (2 * x) ** 2 / ((a - x) * (b - x)) - K


def squared_imbalance(x):
    """SLSQP receives an array, even when there is only one variable."""
    return k_imbalance(x[0]) ** 2


def main():
    # Method 1: find a zero of the equilibrium equation.
    # Without fprime, scipy's newton function uses the secant method.
    x_newton = newton(k_imbalance, x0=0.5, tol=1e-12, maxiter=100)

    # Method 2: minimize the squared imbalance within the physical interval.
    # The upper bound avoids division by zero at x = 1.
    result = minimize(
        squared_imbalance,
        x0=[0.5],
        method="SLSQP",
        bounds=[(0, 0.999)],
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    if not result.success:
        raise RuntimeError(f"SLSQP did not converge: {result.message}")
    x_slsqp = float(result.x[0])

    if not (0 <= x_newton < min(a, b)):
        raise RuntimeError("The root is outside the physical extent interval.")
    agree = np.isclose(x_newton, x_slsqp, rtol=0, atol=1e-6)
    if not agree:
        raise RuntimeError("The two equilibrium methods disagree.")

    print(f"K = {K}")
    print(f"Newton (secant): x = {x_newton:.9f} mol")
    print(f"  Imbalance = {k_imbalance(x_newton):.3e}")
    print(f"SLSQP:          x = {x_slsqp:.9f} mol")
    print(f"  Imbalance = {k_imbalance(x_slsqp):.3e}")
    print(f"Methods agree within 1e-6 mol: {bool(agree)}")

    # Both methods agree; use the root to report and mark the composition.
    x_eq = x_newton
    n_h2 = a - x_eq
    n_i2 = b - x_eq
    n_hi = 2 * x_eq
    print("Equilibrium composition:")
    print(f"  H2 = {n_h2:.6f} mol")
    print(f"  I2 = {n_i2:.6f} mol")
    print(f"  HI = {n_hi:.6f} mol")

    x = np.linspace(0, min(a, b), 300)
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    # H2 and I2 coincide because their initial amounts are equal.
    ax.plot(x, a - x, color="#225a7c", linewidth=3.5, label=r"H$_2$")
    ax.plot(x, b - x, color="#e5a436", linewidth=2, linestyle="--", label=r"I$_2$")
    ax.plot(x, 2 * x, color="#ba4a43", linewidth=2.5, label="HI")
    ax.axvline(x_eq, color="#444444", linestyle=":", label="Equilibrium")
    ax.scatter([x_eq, x_eq], [n_h2, n_hi], color="#333333", zorder=5)
    ax.annotate(
        f"HI = {n_hi:.3f} mol",
        xy=(x_eq, n_hi),
        xytext=(0.38, 1.65),
        arrowprops={"arrowstyle": "->", "color": "#555555"},
    )
    ax.annotate(
        f"H$_2$ = I$_2$ = {n_h2:.3f} mol",
        xy=(x_eq, n_h2),
        xytext=(0.56, 0.75),
        arrowprops={"arrowstyle": "->", "color": "#555555"},
    )
    ax.set(
        xlabel="Reaction extent, x (mol)",
        ylabel="Amount (mol)",
        title=f"Chemical equilibrium: K = {K}, x = {x_eq:.4f} mol",
        xlim=(0, 1),
        ylim=(0, 2.1),
    )
    ax.grid(alpha=0.2)
    ax.legend(loc="upper left")
    output_path = Path(__file__).resolve().with_name("equilibrium.png")
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    print(f"Saved {output_path.name}")


if __name__ == "__main__":
    main()
