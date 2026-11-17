# Part 2 review — REFERENCE ONLY

Published 17 November 2026; analysis revision 2 dated 16 November 2026.

**For comparison and group discussion only. This is not an approved group version, a replacement for the existing project, or a Quercus submission.** The alternative transformation and all conclusions require group review. Earlier project files remain in their existing locations.

[Shared Google Doc reference tab](https://docs.google.com/document/d/1rDqK7jcE0h9sf8BB9BrexBxCRF1ibI0mxvHbqdOyR-w/edit?tab=t.rysncb3oknd2)

## Read / download

| Material | Purpose |
|---|---|
| [Anonymous A1 poster](Poster_Part2_review.pdf) | Revised figures, model comparison, diagnostics and interpretation |
| [Chinese review report](Review_Report_ZH.pdf) | Five-page explanation and rubric evidence |
| [32-item rubric audit](Rubric_point_by_point_ZH.txt) | Evidence and explicit unverified presentation items |
| [Executed analysis](Part2_Analysis_review.html) | Full code, numerical output and diagnostics; download and open locally |
| [R Markdown source](Part2_Analysis_review.Rmd) | Self-contained reproducible analysis |
| [English rehearsal outline](Presentation_rehearsal_EN.txt) | Four 110-second blocks; actual recording is still required |
| [Editable poster source](poster_source/) | Rebuild the PDF from the accompanying results and figures |
| [Numerical verification](results/final_verification.json) | Independent coefficient, SE, partial-F and inverse-transformation checks |

The dated report describes the local review at the time it was written. References inside that report to private `requirements/`, the original draft, or historical audit files refer to the local review archive, not this public directory. They are not required to run this analysis. Course handouts and browser/account dumps are not redistributed here.

## Findings and interpretation

- The original fixed split is unchanged: 4,330 training observations and 1,855 reserved observations. Test evaluation is disabled.
- The reference response is `z = 2 - 2/sqrt(price_k)`, with `log(area) * division`. The matched-design Box–Cox estimate is −0.504, with a profile 95% interval [−0.554, −0.455].
- Same-response BIC improves from −27426.06 (52 coefficients) to −27449.43 (46 coefficients). This comparison must not be made across response scales.
- The regional interaction gives F(8,4284) = 16.68, nominal p ≈ 1.40e−24. This is exploratory post-selection inference, not a confirmatory population claim.
- Figure 1 shows 4.3%–8.6% changes for 10% more area, at a **fixed hypothetical $500,000 model-index baseline**. This is an inverse transformation of the fitted transformed mean; it is not arithmetic mean price, a constant elasticity, or a causal renovation return.
- Residual spread improves, but tail behavior, collinearity, unknown dependence, survey design and coding limitations remain. New England has only 39 training observations.

The 13 poster subitems have material/render evidence. The presentation outline addresses the remaining content, but all 19 presentation subitems still require an actual video for acceptance. No score or full-mark guarantee is implied. Teacher feedback/latest group draft, actual timing and delivery, competition choice, link permissions and submission are not verified/completed by this reference package.

## Reproduce

Download the repository ZIP and extract it, or clone the repository. Keep this directory together; it contains public Census raw data and the fixed split.

In R/RStudio, set the working directory to this directory, then run:

```r
install.packages(c("MASS", "knitr", "rmarkdown", "jsonlite")) # only if missing
rmarkdown::render("Part2_Analysis_review.Rmd")
```

R and Pandoc are required; RStudio normally supplies Pandoc. On macOS/Linux, `bash run_review.command` is an alternative if `Rscript` is on PATH. The launcher also recognizes the existing local `sta302r` environment. Default `evaluate_test=false` preserves the reserved set. Do not use test outcomes to choose or revise the model.

The final source was rendered from raw CSV and split in a clean directory using R 4.4.3. Independent NumPy verification matched coefficients within 3.93e−14, standard errors within 1.30e−13, and the nested F statistic within 1.82e−12. The poster was rendered and visually checked. This publication copies those verified source/results; it does not claim a new video or assignment submission.

To rebuild the poster, install Python `numpy` and `reportlab`, then run `python3 poster_source/build_poster.py` from this directory. Inspect the resulting PDF after editing.

`SHA256_MANIFEST.json` records the published files. Public data source: [U.S. Census SOC microdata](https://www.census.gov/construction/chars/microdata.html).
