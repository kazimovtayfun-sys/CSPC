# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under `PW<n>/Lab <X>/`.

## Setup
Create the environment for a given lab:
```bash
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc
```
## PW1 - Lab A: Reproducible Foundations
What I built:
Coursework repository structure, Conda environment, Git branching, unit tests, and performance benchmark.

Speed comparison (loop vs NumPy):

loop: 5.9297 s

numpy: 0.0003 s

speed-up: 17334.6 x faster

Tests: all passing? Yes

Conclusion:
In this lab, I set up a reproducible environment using Conda and Git. The vectorised NumPy implementation demonstrated significant performance improvements over pure Python loops. All unit tests passed successfully.

## PW1 - Lab B: Data, Plotting, and Automation

- **Data Findings & Model Fit**: The observed radioactive decay data decreases exponentially over time. When plotted alongside the theoretical curve ($N_0 e^{-\lambda t}$ with $\lambda = 0.3$), the measured data closely follows the analytical decay law.
- **Snakemake Automation**: The Snakemake pipeline automates figure generation, re-running `plot.py` to produce `figure.png` only when the input files (`decay_observed.csv`, `plot.py`) are modified or when the target figure is missing.
## PW2 - Lab A: Motion from Tracking Data

- **Mean Acceleration:** -8.58 m/s²
- **Standard Deviation of Acceleration:** 28.72 m/s²
- **Max Difference (Original vs Recovered Position):** 0.78 m

### Observations:
- **Noise in Acceleration:** Numerical differentiation magnifies high-frequency measurement noise because finite differences divide small position fluctuations by the small time step ($\Delta t = 0.1\text{ s}$). Differentiating twice amplifies this effect exponentially, leading to large oscillations in acceleration even though the position data appears smooth.
- **Integration Effect:** Integration performs cumulative summation, which acts as a low-pass filter and allows zero-mean random noise to cancel out. Consequently, integrating the noisy acceleration back recovers the original position trajectory within less than a metre of error.
