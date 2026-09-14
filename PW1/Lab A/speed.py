import time
from decay import simulate, simulate_loop

n0 = 100_000
lam = 0.05
steps = 200

# Loop benchmark
t0 = time.perf_counter()
simulate_loop(n0, lam, steps=steps)
t_loop = time.perf_counter() - t0

# NumPy benchmark
t0 = time.perf_counter()
simulate(n0, lam, steps=steps)
t_numpy = time.perf_counter() - t0

speedup = t_loop / t_numpy

print(f"loop:    {t_loop:.4f} s")
print(f"numpy:   {t_numpy:.4f} s")
print(f"speedup: {speedup:.1f}x")
