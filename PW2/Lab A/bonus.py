"""
PW2 Lab A -- Bonus: 2D Tracked Trajectory
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Read trajectory.csv (columns: time, x, y)
data = np.loadtxt("trajectory.csv", delimiter=",", skiprows=1)
t = data[:, 0]
x = data[:, 1]
y = data[:, 2]

# 2. Compute velocity components and scalar speed
vx = np.gradient(x, t)
vy = np.gradient(y, t)
speed = np.sqrt(vx**2 + vy**2)

# 3. Create plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: 2D Path (x vs y)
ax1.plot(x, y, color="tab:blue", label="Tracked path")
ax1.set_xlabel("x (m)")
ax1.set_ylabel("y (m)")
ax1.set_title("2D Path (x vs y)")
ax1.grid(True)
ax1.axis("equal")
ax1.legend()

# Right panel: Speed over time
ax2.plot(t, speed, color="tab:purple", label=r"Speed $\sqrt{v_x^2 + v_y^2}$")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Speed (m/s)")
ax2.set_title("Speed vs Time")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig("trajectory.png", dpi=300)
print("Saved trajectory.png successfully.")