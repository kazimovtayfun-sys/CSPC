import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# TODO 1: read freefall.csv into arrays t and y
data = np.loadtxt("freefall.csv", delimiter=",", skiprows=1)
t = data[:, 0]
y = data[:, 1]

# TODO 2: compute velocity and acceleration
v = np.gradient(y, t)
a = np.gradient(v, t)

mean_a = np.mean(a)
std_a = np.std(a)

print(f"Mean acceleration: {mean_a:.4f} m/s^2")
print(f"Acceleration std dev: {std_a:.4f} m/s^2")

# TODO 3: integrate a back up to recover velocity and position
v_recovered = cumulative_trapezoid(a, t, initial=0) + v[0]
y_recovered = cumulative_trapezoid(v_recovered, t, initial=0) + y[0]

max_diff = np.max(np.abs(y - y_recovered))
print(f"Max difference between original and recovered position: {max_diff:.4f} m")

# TODO 4: make a figure with 3 stacked panels
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

# Top panel: Position
ax1.plot(t, y, label="Measured position y(t)", color="tab:blue")
ax1.set_ylabel("Position (m)")
ax1.grid(True)
ax1.legend(loc="upper right")

# Middle panel: Velocity
ax2.plot(t, v, label="Velocity v(t)", color="tab:orange")
ax2.set_ylabel("Velocity (m/s)")
ax2.grid(True)
ax2.legend(loc="lower left")

# Bottom panel: Acceleration
ax3.plot(t, a, label="Acceleration a(t)", color="tab:red", alpha=0.6)
ax3.axhline(-9.81, color="black", linestyle="--", linewidth=1.5, label="Target (-9.81 m/s²)")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Acceleration (m/s²)")
ax3.grid(True)
ax3.legend(loc="lower left")

plt.tight_layout()
plt.savefig("motion.png", dpi=300)
print("Saved motion.png successfully.")