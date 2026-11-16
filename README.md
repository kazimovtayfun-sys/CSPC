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

### Bonus (2D Trajectory):
- Processed 2D position tracking data from `trajectory.csv`.
- Computed velocity components $v_x$ and $v_y$ using numerical differentiation, then calculated total speed $\sqrt{v_x^2 + v_y^2}$.
- Generated and saved `trajectory.png` showing the 2D path and speed evolution over time.

## PW2 - Lab B: Optimization in Chemistry

Completed scripts, input data, plots, and recorded console output are in
[`PW2/Lab B/`](PW2/Lab%20B/).

### Running the scripts

From the repository root, with NumPy, SciPy, and Matplotlib installed:

```bash
conda activate cspc
python "PW2/Lab B/warmup.py"
python "PW2/Lab B/kinetics.py"
python "PW2/Lab B/equilibrium.py"
python "PW2/Lab B/titration.py"
```

The chemistry scripts read their CSVs and save their PNGs in the script's own
folder, so they also work when launched from another directory. Recorded output
is available in [`results.txt`](PW2/Lab%20B/results.txt).

### Part 2: comparing three optimization methods

For the convex function `f(x) = (x - 3)^2 + 1`, gradient descent, Newton's method,
and SLSQP all converge from `x0 = 0` to `x = 3`, where `f(x) = 1`.
The curvature is positive (`f''(x) = 2`), confirming a minimum.

For `g(x) = x^4 - 3x^2 + x + 5`, the results are:

| Start x0 | Method | Final x | g(x) | Classification |
| ---: | --- | ---: | ---: | --- |
| 0 | Gradient descent | -1.300840 | 1.486095 | Global minimum |
| 0 | Newton | 0.169938 | 5.084135 | Local maximum |
| 0 | SLSQP | -1.300840 | 1.486095 | Global minimum |
| 2 | Gradient descent | 1.130901 | 3.929770 | Local minimum |
| 2 | Newton | 1.130901 | 3.929770 | Local minimum |
| 2 | SLSQP | -1.300840 | 1.486095 | Global minimum |

Newton is applied to `g'(x) = 0`, so it finds a stationary point rather than
necessarily a minimum. From zero it reaches a point with
`g''(0.169938) = -5.653451`, identifying a maximum. From two it reaches
`g''(1.130901) = 9.347248`, identifying a minimum.

The starting point changes the result for gradient descent and Newton. SLSQP
reaches the negative minimum from both starting points in this run; its line
search can take steps across to the other minimum. This is an observed result,
not a guarantee that SLSQP always finds a global minimum. Comparing the two
minima shows that the negative one has the lower value. Since the quartic tends
to positive infinity at both ends and has no other stationary points, it is the
global minimum.

Gradient descent uses a learning rate of `0.05` and stops when the change in x
is below `1e-10`, with a limit of 10,000 iterations. Newton uses a tolerance of
`1e-12`; SLSQP uses `ftol = 1e-12`. These settings and the chosen starting points
explain the reported numerical behavior.

### Part 3: first-order reaction kinetics

The model is `C(t) = C0 * exp(-k*t)`, with the initial concentration fixed to the
first measurement, `C0 = 104.082`. Minimizing the sum of squared concentration
residuals with SLSQP, starting at `k = 0.5` and using bounds `0 <= k <= 5`, gives:

- **Fitted rate constant:** `k = 0.26176039` per data time unit.
- **Sum of squared errors:** `266.129419`.
- **Root-mean-square error:** `2.579387` concentration data units, across 40 measurements.

This is close to the expected rate constant of 0.25. The fitted curve follows the
observed exponential decay; residual scatter reflects the noisy measurements.
The CSV does not specify physical time or concentration units, so the plot uses
data units. The negative late-time observations are retained when fitting.

![Measured concentrations and fitted first-order decay](PW2/Lab%20B/kinetics.png)

### Part 4: chemical equilibrium

For `H2 + I2 <=> 2 HI`, starting with 1 mol of each reactant and `K = 15.6`,
the equilibrium equation is `(2*x)^2 / (1-x)^2 - 15.6 = 0`.

| Method | Equilibrium extent x (mol) |
| --- | ---: |
| `scipy.optimize.newton` root finder | 0.663847667 |
| SLSQP, minimizing squared imbalance | 0.663847659 |

Both methods start from `x = 0.5`; SLSQP uses bounds `[0, 0.999]` to avoid
division by zero at `x = 1`. The extents agree within `8e-9` mol. The call to
`newton` does not supply a derivative, so SciPy uses its secant variant here.

Using the root-finder result, the equilibrium composition is:

| Species | Amount (mol) |
| --- | ---: |
| H2 | 0.336152 |
| I2 | 0.336152 |
| HI | 1.327695 |

The analytical solution `x = sqrt(K) / (2 + sqrt(K)) = 0.663847666961` independently
confirms the numerical result. Substitution gives the specified equilibrium
constant, and `2*n(H2) + n(HI) = 2` and `2*n(I2) + n(HI) = 2` preserve the
initial amounts of hydrogen and iodine atoms. The reactant curves coincide
because their initial amounts and stoichiometric coefficients are equal.

![Species amounts versus reaction extent, with equilibrium marked](PW2/Lab%20B/equilibrium.png)

### Part 5: titration equivalence point (bonus)

The numerical slope is computed with `np.gradient(pH, V)`. Its maximum occurs at
**50.00 mL**, where **pH = 7.000** and the numerical slope is **4.000 pH/mL**.
This identifies the equivalence point at the steepest part of the measured pH
curve. It is an estimate on the supplied 1 mL sampling grid.

![Titration curve and its numerical slope, with equivalence marked](PW2/Lab%20B/titration.png)

### Validation

All four scripts ran successfully using Python 3.11.9, NumPy 2.4.6,
SciPy 1.17.1, and Matplotlib 3.11.2. The warm-up solutions were checked against
the roots of the analytical derivative; the kinetic fit was checked with an
independent root solve of the error derivative; the equilibrium was checked
against the exact solution and atom conservation; and the titration result was
checked using central differences. All three saved plots were visually reviewed.
