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