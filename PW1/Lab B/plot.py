import numpy as np
import matplotlib.pyplot as plt

LAMBDA = 0.3  # decay constant, given

# TODO 1: read decay_observed.csv (columns: time, count; skip the header row)
# and split it into two arrays: t and observed.
data = np.loadtxt("decay_observed.csv", delimiter=",", skiprows=1)
t = data[:, 0]
observed = data[:, 1]

# TODO 2: set N0 to the first observed value, then build the analytical curve
# analytical = N0 * exp(-LAMBDA * t)
N0 = observed[0]
analytical = N0 * np.exp(-LAMBDA * t)

# TODO 3: make a 1x2 subplot with SHARED x and y axes.
# left panel: scatter of the observed data, titled "Observed data"
# right panel: line plot of the analytical curve, titled "Analytical"
# label the axes.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)

# Left panel: observed data points
ax1.scatter(t, observed, color="crimson", alpha=0.7, label="Observed data")
ax1.set_title("Observed data")
ax1.set_xlabel("Time")
ax1.set_ylabel("Count")
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend()

# Right panel: theoretical analytical line
ax2.plot(t, analytical, color="navy", linewidth=2, label="Analytical curve")
ax2.set_title("Analytical")
ax2.set_xlabel("Time")
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.legend()

plt.tight_layout()

# TODO 4: save the figure as figure.png
plt.savefig("figure.png", dpi=300)
print("Saved figure.png")