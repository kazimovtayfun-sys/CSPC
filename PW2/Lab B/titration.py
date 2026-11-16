"""PW2 Lab B, Part 5 (bonus): find a titration's equivalence point.

Run: python titration.py
The CSV is read from this script's folder; titration.png is saved there too.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    folder = Path(__file__).resolve().parent
    # TODO 1: read titration.csv (columns volume_base, pH) into arrays V, pH.
    data = np.genfromtxt(folder / "titration.csv", delimiter=",", names=True)
    V = data["volume_base"]
    pH = data["pH"]

    # TODO 2: compute the slope of the pH curve with np.gradient(pH, V), and find
    #         the volume where that slope is largest (np.argmax). That is the
    #         equivalence point. Print it.
    # np.gradient uses central differences at interior points.
    slope = np.gradient(pH, V)
    equivalence_index = np.argmax(slope)
    V_eq = V[equivalence_index]
    pH_eq = pH[equivalence_index]

    print(f"Equivalence volume = {V_eq:.2f} mL")
    print(f"pH at equivalence = {pH_eq:.3f}")
    print(f"Maximum numerical slope = {slope[equivalence_index]:.3f} pH/mL")

    # TODO 3: make two plots side by side: (left) pH vs volume with a line at the
    #         equivalence point; (right) the slope vs volume, showing it peaks
    #         at the equivalence point. Save as titration.png.
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    axes[0].plot(V, pH, color="#174a6e", linewidth=2, label="Titration curve")
    axes[0].scatter([V_eq], [pH_eq], color="#d56727", s=45, zorder=3)
    axes[0].set(xlabel="Base volume added (mL)", ylabel="pH", title="Titration curve")

    axes[1].plot(V, slope, color="#174a6e", linewidth=2, label="Numerical slope")
    axes[1].scatter(
        [V_eq], [slope[equivalence_index]], color="#d56727", s=45, zorder=3
    )
    axes[1].set(
        xlabel="Base volume added (mL)",
        ylabel="dpH/dV (pH/mL)",
        title="Largest slope identifies equivalence",
    )

    for ax in axes:
        ax.axvline(
            V_eq,
            color="#d56727",
            linestyle="--",
            linewidth=1.5,
            label=f"Equivalence: {V_eq:.0f} mL",
        )
        ax.grid(alpha=0.2)
        ax.legend(frameon=False)

    plot_path = folder / "titration.png"
    fig.savefig(plot_path, dpi=180)
    plt.close(fig)
    print(f"Saved {plot_path.name}")


if __name__ == "__main__":
    main()
