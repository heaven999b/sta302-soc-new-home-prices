# Rerun verification — 2 November 2026

Both Rmd files rendered successfully with R 4.4.3, using original data and the existing split. Part 1 ran before Part 2. Both cleaned datasets match the downloaded GitHub snapshot byte for byte. The logs retain the observed locale/font/pandoc warnings; warnings were not removed.

The final test-evaluation chunks remained disabled. Earlier full-sample inspection or probe overlap is disclosed in the English analysis supplement; these reruns do not restore a fully blind test set. Historical R-versus-Python checks were not rerun in this revision.

The revised Word/PDF proposal was visually checked. The proposal and checklist describe remaining team and submission steps. No signatures, OneDrive access or course submission have been completed by this sync.

Reproduce from the repository root:

```sh
Rscript -e 'rmarkdown::render("Part1_Code.Rmd")'
Rscript -e 'rmarkdown::render("Part2_Analysis.Rmd")'
```

Dependencies and data provenance are documented in the repository README. `sha256.json` fingerprints the delivered code, reports, split and cleaned data.
