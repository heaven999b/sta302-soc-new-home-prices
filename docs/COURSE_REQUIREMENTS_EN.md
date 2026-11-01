# Course Requirements and Submission Record

## Verified course materials

The live Quercus assignment and rubric were checked on 2 November 2026, together with the locally saved official Part 0 and Part 1 instructions and the first embedded-ethics slides. The project information page identifies a proposal and signed teamwork agreement, followed by a poster/video presentation and an individual group-work reflection.

- [Part 0 and Part 1 assignment and rubric](https://q.utoronto.ca/courses/462653/assignments/1779637)
- [Project information and dates](https://q.utoronto.ca/courses/462653/pages/final-project-information)
- [Part 0 and Part 1 details](https://q.utoronto.ca/courses/462653/pages/final-project-parts-0-and-1)

Part 0/1 is due 5 November at 11:59 p.m. Toronto time, equivalent to 6 November at 12:59 p.m. Shanghai time. The separate NQA deadline is 8 November at 11:59 p.m. Toronto time, equivalent to 9 November at 12:59 p.m. Shanghai time. Part 2/3 is due 3 December at 11:59 p.m. Toronto time; the listed NQA date is 6 December. The schedule in each proposal targets the ordinary deadline.

The live assignment says no additional late submissions after the NQA deadline, while the general project page describes an hourly late penalty. Plan to the explicit assignment deadline rather than relying on that inconsistency. Detailed Part 2 and Part 3 instructions were not linked from the project-information table at this check; the later analyses are therefore preparation for those components, not certification against an unpublished rubric.

## Requirements matrix

| Requirement | Where addressed | Status |
|---|---|---|
| Open original data and collection purpose | Data description and bibliography | Three official-source datasets |
| At least 1,000 observations | Full cleaned datasets | SOC 6,185; NTD 2,135; IPEDS 1,070 |
| At least nine predictors, numerical and categorical | Variable summary tables | 17; 11; 13 predictor concepts |
| Justified categorical interaction | Introduction and Data description | Division, service type or sector |
| Three relevant peer-reviewed papers | Each Introduction and Bibliography | Three research articles per proposal; additional context identified |
| Numerical summary of all model variables | Table 1 | One concise summary table per proposal; expanded tables in portfolio |
| Trustworthiness and ethical collection/use | Ethics discussion | Source, metadata, privacy, consent and ownership addressed |
| Complete residual analysis | Preliminary results and figure grids | Conditions 1–2; linearity, variance, normality and dependence |
| Preliminary estimates with uncertainty | Table 2; housing coefficient appendix | Conventional SEs/intervals; violations disclosed |
| No repairs in Part 1 results | Main proposal versus supplement | Later repairs are separated |
| Analysis plan and diagnostics after changes | Plan | Selection, transformations, influence and reassessment |
| Dates for analysis, poster and recording | Team schedule | Dates filled; member assignments intentionally blank |
| Contributions | Opening table | Intentionally blank pending group completion |
| Word limits | Word-count record | Main-section headings, prose, captions and table cells checked |
| APA citations; no R console output in proposal | Bibliographies and formatted tables | Tables are edited displays, not console dumps |
| Reproducible Rmd | Matching repositories and local package | Part 1 and Part 2 knitted successfully for all three |
| Signed teamwork agreement | Separate Part 0 submission | Must be agreed and signed by the group |
| Original and cleaned CSVs on UofT OneDrive | Data folders | Local files available; institution-only link still required |

The dataset minimum refers to each full cleaned dataset; the salary proposal transparently states that its preliminary model uses 749 training institutions. The course instructions do not explicitly require a 1,000-row training partition. No high R², small p-value or unique ID is treated as proof that the regression assumptions hold.

## Submission package for the selected project

One group member submits the signed teamwork-agreement PDF, the selected proposal PDF and its matching Rmd. Original and cleaned CSVs go to UofT OneDrive with access set to anyone in UofT with the link; the link belongs in the Quercus submission comment. Include split_ids.csv with the data because the Rmd reads the fixed assignment. For IPEDS, identify the removal of unused chief-administrator name/title fields from repository directory copies.

The three-project portfolio, Google Docs and GitHub are supporting collaboration resources. They do not replace those required components. Contributions, task owners, signatures and the OneDrive permission check remain explicit completion steps. No course submission has been made as part of preparing this portfolio.

## Reproducibility and version scope

Fresh copies of all four public GitHub repositories were downloaded. Each Part1_Code.Rmd was knitted using R 4.4.3 from the original CSVs and fixed split files. Each Part2_Analysis.Rmd was then knitted on training data. All six renders completed successfully. Test-set evaluation blocks were left disabled. Runtime logs and cleaned-data comparisons are retained with the local delivery.

The older R-versus-Python verification reports describe 281 housing checks, 818 transit checks and 321 salary checks. Those historical cross-language audits are preserved as provenance; this preparation reran the R workflows and did not repeat every independent Python comparison. Deterministic OLS on the fixed split does not require averaging artificial repeated seeds. The exploratory selection and prior holdout exposure described in the supplements must still be disclosed.
