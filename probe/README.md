# Python probe (provenance only)

This folder keeps the **exploratory Python probe** that was used on 2026-09-30 to decide whether this topic qualifies. It has been **superseded by the R version** (`Part1_Code.Rmd`, `Part2_Analysis.Rmd`) and is kept only so that the numbers in `verification/R_vs_Python.md` can be traced to their source.

探索阶段的 Python 探针，已被 R 版取代，只作溯源用。

| Path | What it is |
|---|---|
| `scripts/probe_soc.py` | First probe: cleaning, Part 1 raw-price model, log preview, raw-scale robustness checks |
| `scripts/soc_extra.py` | log and Box-Cox(−0.5) versions, survey weights, 2024 replication of the raw specification |
| `scripts/soc_fullflow.py` | Full workflow: variable table, Part 1 course-style diagnostics, Part 2 transformations, BIC/AIC backward selection, final model, confounding checks, 2024 replication of the final specification |
| `scripts/soc_iid.py` | Cluster-robust SEs by division, 1-df Midwest contrast, weighted final model |
| `scripts/utils.py`, `scripts/course_diag.py` | Shared helpers (split, HC3, partial F, GVIF, Box-Cox, ICC, backward selection) and course-style diagnostic plots |
| `scripts/verify_citations.py` | Crossref DOI check for the references |
| `results/soc.json`, `soc_extra.json`, `soc_fullflow.json`, `soc_iid.json` | Numerical results of the scripts above |
| `results/tables/soc_*.csv` | Variable table and coefficient tables (Part 1 and final model) |
| `results/crossref_verification.json` | Crossref metadata for all references checked by the search groups (includes DOIs used by other candidate projects) |

Notes:

- The scripts expect the original probe folder layout (`data/soc/…`, `figures/`, `results/`) and will **not** run inside this repository as-is. They are not needed to reproduce any result here; use the Rmd files instead.
- All fitting in the probe used the 70% training split only (`numpy.random.default_rng(302)`); the test IDs it saved are identical to the `test` rows of `data/split_ids.csv`.
- Known issues found during the R check (see `verification/R_vs_Python.md`, section 3): the cluster-robust SE of the Midwest contrast counts one redundant column in the small-sample factor; "ICC ≈ 0 after adding division fixed effects" is mechanical and is not evidence of independence; the "all alternative interactions" check omitted division × full bathrooms.
