# Proposal writing sync — 2 November 2026

The approved writing revision was applied to the existing Group 62 Google Doc and synchronized to Markdown, HTML, Word and PDF. It follows three review rounds: an initial Astra review, an independent second review, and a final recheck of the revised text.

The introduction connects Rosen (1974), Gyourko and Saiz (2006), and Sirmans et al. (2006) to the question, controls and regional-slope comparison. The preliminary results now explain dollar slopes, the Middle Atlantic–South Atlantic contrast, the interaction's increase in training R², diagnostic evidence, provisional inference, and the conditional bedroom/lot-size estimates. Table 2 and Figures 2–4 captions and the bibliography were synchronized.

## Validation

- All approved paragraphs and captions match the live Word export verbatim; the PDF and HTML match after whitespace normalization. PDF page footers are excluded from text comparisons.
- The five tables match the live pre-edit backup, including the latest team names and plan assignments. All four embedded figure files have unchanged hashes.
- All 10 pages of the Word rendering were visually inspected. The final sanitized live Word export renders to 10 byte-identical page PNGs. All 10 pages of the Google Docs PDF export were also visually inspected.
- Introduction: **342 words**. Preliminary results: **313 words**, plus **49 words** in its captions, totaling **362 words**. Counts use whitespace splitting.
- The local submission-preparation ZIP was rebuilt and every packaged file checked against its SHA-256 manifest.

`reviewed_text.json` contains the approved text; `validation.json` records the checks; `sha256.json` fingerprints the proposal files and unchanged analysis inputs/outputs. Dollar-delimited math was disabled when generating HTML so currency amounts remain literal text.

The Word export's hidden title-border residue was removed before rendering. The PDF is a fresh Google Docs export. The live document remains the editing source; these files are snapshots. Missing team names/contributions remain blank. Historical Chinese drafts and the three-project comparison archive were not rewritten.

This was a writing and document synchronization. Analysis code, data, split IDs and model output did not change, and the R analyses were not rerun for this text-only revision. No Quercus submission was made.
