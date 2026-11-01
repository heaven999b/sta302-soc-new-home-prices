# Floor area × Census division: sale prices of new U.S. homes (SOC 2025)

## Start here — Group 62 materials

| Material | Link |
|---|---|
| Part 0 teamwork agreement — collaborative Google Doc | [Open Part 0](https://docs.google.com/document/d/1jENKQ83oF1fpZYHq7wk_R3dypHRt6pBYv2vRfdR1l7Q/edit) |
| Part 1 proposal — collaborative Google Doc | [Open Part 1](https://docs.google.com/document/d/1rDqK7jcE0h9sf8BB9BrexBxCRF1ibI0mxvHbqdOyR-w/edit) |
| Proposal snapshot — updated 2 November 2026 | [PDF](proposal/Proposal_Part1_EN.pdf) · [Word](proposal/Proposal_Part1_EN.docx) · [Markdown](proposal/Proposal_Part1_EN.md) |
| Shared submission materials | [Google Drive folder](https://drive.google.com/drive/folders/14TQrSwZvfd9tc5uYxqN5S1h_wcm8roYY) |
| Course data package — UofT sign-in required | [OneDrive folder](https://utoronto-my.sharepoint.com/:f:/g/personal/heaven_yi_mail_utoronto_ca/IgAFTwJSFUDmQobtA7uqUvTmAcypZCzwoALVw3rPRipUDVI?e=uGPNcc) |
| Executable analysis | [Part 1 Rmd](Part1_Code.Rmd) · [Part 2 Rmd](Part2_Analysis.Rmd) |
| Original data / cleaned data / fixed split | [Original](data/original/) · [Cleaned](data/cleaned/) · [Split IDs](data/split_ids.csv) |
| Figures and analysis output | [Figures](figures/) · [Part 1 output](Part1_Code.html) · [Part 2 output](Part2_Analysis.html) |
| Research documentation and checks | [Documents](docs/) · [Rerun verification](verification/2026-11-02/) |
| What to submit and what remains | [First-submission guide](submission/FIRST_SUBMISSION.txt) · [Submission comment](submission/QUERCUS_COMMENT.txt) |

Google Docs are the live editing copies; repository PDF/Word files are dated snapshots. GitHub may offer a download instead of previewing large HTML or data files. To obtain the whole project, use **Code → Download ZIP** or clone this repository.

## Latest English revision — 2 November 2026

Use the revised [proposal PDF](proposal/Proposal_Part1_EN.pdf), [editable Word document](proposal/Proposal_Part1_EN.docx), [Markdown](proposal/Proposal_Part1_EN.md) or [HTML](proposal/Proposal_Part1_EN.html). These supersede the September English proposal. The Chinese translation remains a dated historical draft.

Read the [English analysis supplement](docs/ANALYSIS_SUPPLEMENT_EN.md), [expanded data summaries](docs/DATA_SUMMARIES_EN.md), [course checklist](docs/COURSE_REQUIREMENTS_EN.md), and [rerun verification](verification/2026-11-02/README.md). The [complete three-project portfolio](https://github.com/heaven999b/sta302-research-project/tree/main/reports/english-2026-11-02) and [online reading copy](https://chatgpt.com/space/page_2de0a2753be081919dd0918aba49e029) provide the comparison.

**Selected project:** SOC, Group 62. Haiwen Yi's contribution and the first three analysis-task assignments are filled in. Other members' contributions and the four poster/presentation/submission task owners remain blank. Part 0 contains the agreed English teamwork text and Haiwen's information; other members must complete their entries. The UofT OneDrive data package has been uploaded and its school-link access checked. No Quercus submission has been made. See the [first-submission guide](submission/FIRST_SUBMISSION.txt).

**Version policy:** keep future data, code, figures and outputs in this repository. `Part1_Code.Rmd` and `Part2_Analysis.Rmd` are the executable sources; their HTML files contain analysis outputs. `probe/` is historical exploration. No retrospective weekly reports have been invented. Part 2 working notes and the historical design remain partly Chinese.


STA302H1 (Methods of Data Analysis I), University of Toronto, Fall 2026 — final project, candidate 1 of 3.

> 中文版见 [README_zh.md](README_zh.md)。完整的中文研究设计见 [design/research_design.md](design/research_design.md)。

## Research question

Among newly built, detached single-family homes sold in the United States in 2025, how much does an extra 100 square feet of finished floor area add to the sale price, and does this marginal price of floor area differ across the nine Census divisions, after holding constant lot size, bedrooms, full and half bathrooms, stories, garage, foundation, fireplaces, exterior wall material, heating fuel, sewer type, homeowners' association and age-restricted status, construction stage at sale, and month of sale?

The question is answered by the eight floor area × division interaction coefficients (and the partial F / HC3 Wald test that they are all zero) and by each division's floor-area slope with its 95% confidence interval.

## Data

- **Source:** U.S. Census Bureau, *Survey of Construction (SOC) microdata*, annual files for 2025 (main analysis) and 2024 (independent replication), <https://www.census.gov/construction/chars/microdata.html>. Free, no registration. Variable documentation: [`data/original/socmicro_info.pdf`](data/original/socmicro_info.pdf).
- **Collection:** a national probability sample of new houses (about 1 in 50) drawn from building permits and from canvassing areas that do not require permits; builders or owners are interviewed about start, sale and completion dates and more than 40 characteristics. HUD funds the collection of the characteristics.
- **Unit:** one newly built, detached single-family house built for sale with a 2025 sales contract. 25,246 raw records → **6,185** after cleaning → 4,330 training / 1,855 test.
- **Response:** sale price in $1000s (includes the improved lot; top- and bottom-coded by the Census Bureau within each division).
- **Predictors (17):** 3 numerical (floor area, lot size, month of sale) and 14 categorical (division and 13 structural or market features). 52 coefficients in the Part 1 model.

## Main results (training set, n = 4,330)

| | Part 1 (raw price, uncorrected) | Part 2 final (log price ~ log floor area, BIC-selected) |
|---|---:|---:|
| Coefficients | 52 | 46 |
| R² / adjusted R² | 0.713 / 0.710 | 0.756 / 0.753 |
| Residual skewness / excess kurtosis | 2.04 / 18.0 | 0.48 / 2.52 |
| Interaction partial F p-value | 1.2e-57 | 2.4e-9 |
| Interaction HC3 Wald p-value | 7.5e-24 | 1.6e-10 |
| ΔR² of floor area + interaction | 0.074 | 0.076 |
| Largest Cook's distance | 0.18 | 0.022 |

Floor-area effect by division:

| Division | n | Part 1 slope ($1000s per 100 sq ft), 95% CI | Part 2 elasticity, 95% CI | Price change for +10% floor area |
|---|---:|---|---|---:|
| South Atlantic (reference) | 1,308 | 11.83 (10.60, 13.07) | 0.679 (0.630, 0.727) | +6.7% |
| New England | 39 | 19.26 (15.05, 23.47) | 0.632 (0.448, 0.815) | +6.2% |
| Middle Atlantic | 119 | 24.56 (22.32, 26.79) | 0.735 (0.633, 0.837) | +7.3% |
| East North Central | 510 | 6.85 (5.19, 8.51) | 0.525 (0.462, 0.589) | +5.1% |
| West North Central | 313 | 10.57 (8.32, 12.82) | 0.535 (0.462, 0.608) | +5.2% |
| East South Central | 344 | 13.78 (11.88, 15.68) | 0.702 (0.628, 0.775) | +6.9% |
| West South Central | 850 | 9.27 (7.71, 10.82) | 0.734 (0.677, 0.791) | +7.2% |
| Mountain | 473 | 14.60 (13.03, 16.17) | 0.584 (0.523, 0.645) | +5.7% |
| Pacific | 374 | 21.70 (19.47, 23.92) | 0.727 (0.650, 0.804) | +7.2% |

- **Midwest contrast (1 df):** the floor-area elasticity is 0.152 lower in the Midwest (East and West North Central) than in the other seven divisions; HC3 p = 3.2e-10; clustered by division with a t(8) reference, p = 5.9e-4.
- **Robustness:** the interaction stays significant after adding each of seven alternative interactions, all of them at once (HC3 p = 1.3e-7), dropping top-coded prices, using the survey weights, and choosing the model by AIC. Individual division contrasts are less stable (see [`design/research_design.md`](design/research_design.md), section 8).
- **Independent replication:** the same final specification on 6,118 different homes sold in 2024 gives R² = 0.752 and interaction HC3 p = 1.2e-17, with the same pattern (lowest elasticities in East North Central, West North Central and Mountain).
- **Numerical check:** every R result was checked against the original Python probe (281 items; 261 identical to within 3.3e-10, the rest explained) — see [`verification/R_vs_Python.md`](verification/R_vs_Python.md).

## Repository layout

```
.
├── Part1_Code.Rmd / .html     Part 1 submission code (English): clean original data, summaries, interaction plot,
│                              preliminary model, full residual analysis. No corrections.
├── Part2_Analysis.Rmd / .html Part 2 working analysis (Chinese narrative), training set only: Box-Cox, log vs log-log,
│                              VIF/GVIF, influence, partial F, AIC/BIC step(), final model, HC3 and clustered SEs,
│                              confounding, sensitivity, Midwest contrast, 2024 replication, sealed test-set block
├── data/
│   ├── original/              soc25.csv, soc24.csv (Census files saved as CSV), socmicro_info.pdf
│   ├── cleaned/               soc_clean.csv (written by Part 1, with split column), soc2024_clean.csv (written by Part 2)
│   └── split_ids.csv          fixed 70/30 train/test split (id, split)
├── figures/                   PNGs written by the Rmd files (fig1–fig4 are used in the proposal)
├── proposal/                  Proposal_Part1_EN.md/.html/.pdf (+ proposal.css), Proposal_Part1_中文对照.md
├── design/research_design.md  full research design (Chinese)
├── verification/R_vs_Python.md
├── probe/                     original exploratory Python probe (provenance only; superseded by the R version)
└── docs/                      TODO.md, DECISIONS.md, CHANGELOG.md
```

## Reproducing the results

Requirements: R ≥ 4.3 with `MASS` (ships with R), `car`, `sandwich`, `lmtest`, `rmarkdown` and `knitr`. Part 1 uses only base R and `car`.

```r
install.packages(c("car", "sandwich", "lmtest", "rmarkdown", "knitr"))
```

1. Open `Part1_Code.Rmd` in RStudio and click **Knit**. It reads `data/original/soc25.csv`, prints the row count after each cleaning step (25,246 → … → 6,185), writes `data/cleaned/soc_clean.csv`, and draws the proposal figures into `figures/`.
2. Then knit `Part2_Analysis.Rmd`. It reads `data/cleaned/soc_clean.csv`, so Part 1 must be knitted first.

From a shell (use a UTF-8 locale, otherwise the Chinese table captions in Part 2 are garbled):

```bash
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
Rscript -e 'rmarkdown::render("Part1_Code.Rmd")'
Rscript -e 'rmarkdown::render("Part2_Analysis.Rmd")'
```

To rebuild the proposal after editing `proposal/Proposal_Part1_EN.md`:

```bash
cd proposal
pandoc Proposal_Part1_EN.md -s --css proposal.css -o Proposal_Part1_EN.html
# then print Proposal_Part1_EN.html to PDF (e.g. headless Chrome with --no-pdf-header-footer) and check every page
```

## Test-set policy

- The 70/30 split was fixed **once, at the start of the project**, with `numpy.random.default_rng(302).permutation(6185)` in the Python probe (first 4,330 permuted rows = training set) and archived as `data/split_ids.csv`. The R code reads this file instead of re-drawing the split (`set.seed(302)` in R would give a different split). The 1,855 test IDs match the probe's archived test IDs exactly.
- Every table, figure and model in both Rmd files uses the training rows only; Part 2 discards the test rows immediately after reading the cleaned file.
- The last chunk of `Part2_Analysis.Rmd` ("test-set final validation") is `eval = FALSE`. It must be run **once**, only after the Part 2 model is final.
- Disclosure: before the split was fixed, the probe looked at division-level median prices and floor areas on the full 2025 sample (descriptive only, no model fitting), so the test set is not 100% blind.

## Status and to-do

- [x] Group 62 selected; Part 1 code, figures, data, English proposal and analysis supplements prepared.
- [x] Haiwen Yi's contribution and first three task assignments recorded; Part 0 text and Haiwen's entry completed.
- [x] Original/cleaned data, fixed split and metadata uploaded to UofT OneDrive; school-link access checked.
- [ ] Other members complete Part 0 details and Part 1 contributions.
- [ ] Assign the four remaining plan tasks: poster draft, poster review, presentation recording/review, and final checks/submission.
- [ ] Group reviews both documents; export fresh final PDFs after all edits.
- [ ] One member submits Part 0 PDF, Part 1 PDF and Rmd on Quercus, adds the OneDrive link, and uploads Part 0 to the group page.


## References

- Glaeser, E. L., Gyourko, J., & Saks, R. (2005). Why is Manhattan so expensive? Regulation and the rise in housing prices. *The Journal of Law and Economics, 48*(2), 331–369. https://doi.org/10.1086/429979
- Gyourko, J., & Saiz, A. (2006). Construction costs and the supply of housing structure. *Journal of Regional Science, 46*(4), 661–680. https://doi.org/10.1111/j.1467-9787.2006.00472.x
- Rosen, S. (1974). Hedonic prices and implicit markets: Product differentiation in pure competition. *Journal of Political Economy, 82*(1), 34–55. https://doi.org/10.1086/260169
- U.S. Census Bureau. (2026). *Survey of Construction (SOC) microdata: 2025 annual file* [Data set]. https://www.census.gov/construction/chars/microdata.html
- U.S. Census Bureau. (n.d.). *Survey of Construction microdata files: General information and variable descriptions*. https://www.census.gov/construction/chars/pdf/socmicro_info.pdf

The SOC microdata are public-domain U.S. government data.
