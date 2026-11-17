# PW3 data sources and reproducibility

## Heart data

- Requested dataset: [Ritwik_B3, Heart Disease Cleveland on Kaggle](https://www.kaggle.com/datasets/ritwikb3/heart-disease-cleveland).
- Downloaded on 2026-11-16 using the [public Kaggle download endpoint](https://www.kaggle.com/api/v1/datasets/download/ritwikb3/heart-disease-cleveland).
- Archive member: `Heart_disease_cleveland_new.csv`. Saved as `heart.csv` with identical bytes, including its UTF-8 byte-order mark. No rows or values were changed.
- Shape: 303 rows and 14 columns. `target = 0` means disease absent (164 patients); `target = 1` means disease present (139 patients).
- The four analyzed continuous columns and every binary target were checked row by row against [UCI's original processed Cleveland data](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data). They agree exactly when the UCI diagnosis is converted with `target = (num > 0)`.
- Other categorical columns in the Kaggle version have been recoded upstream. This analysis does not assume they retain UCI's original encodings.

Original dataset citation: Janosi, A., Steinbrunn, W., Pfisterer, M., and Detrano, R.
(1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository.
[DOI: 10.24432/C52P4X](https://doi.org/10.24432/C52P4X).
The [UCI dataset page](https://archive.ics.uci.edu/dataset/45/heart+disease)
documents the variables and licenses the source dataset under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

SHA-256 of `heart.csv`:

```text
336e9962f76b6be8dc4517335b5bf2ffff4fa7eb88953d837d2f137a85f32252
```

## Synthetic chemical data

`chemicals_cancer.csv` is the supplied PW3 teaching dataset: 1,000 rows with
benzene, cadmium, pollution index, age, and malignancy score. The supplied file is
included unchanged. Its generating code was not supplied, so the causal
interpretation is discussed as the intended explanation supported by the
adjusted associations, rather than as experimentally established causation.
Chemical concentration units were not specified and are labelled as data units.

## Methods references

- [SciPy Shapiro-Wilk normality test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html).
- [SciPy independent-sample t-test, including Welch's test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html).
- [SciPy Mann-Whitney U test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html).

Run both scripts from the repository root:

```bash
conda activate cspc
python -m pip install -r PW3/requirements.txt
python PW3/heart_analysis.py
python PW3/chemicals_analysis.py
```

Each script reads its local CSV and regenerates its plots and result files in
the same directory. No network connection is needed to run the analysis after
the files and dependencies are installed.
