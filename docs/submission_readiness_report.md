# Release Readiness Audit

Date: 2026-07-16

## Scope

This audit checks the current manuscript release repository against Nature Portfolio-style expectations for data availability, code availability, ethics disclosure, figure source data and reproducibility materials.

## Current Package

- `source_data/` contains numeric source data used to render the main numeric figures and Appendix C visual summaries.
- `derived_label_tables/` contains compressed, label-only conversation-level and adjacent-turn analytic tables for WildChat, LMSYS Chat and ShareChat.
- `statistical_outputs/integrated_regression/` contains regression, bootstrap, confidence-interval, p-value and sensitivity outputs used in the manuscript and appendix.
- `statistical_outputs/support_intent/` contains support-intent prevalence and contrast summaries.
- `tables/` contains the LaTeX source for manuscript and appendix tables.
- `scripts/` contains the custom source-data, statistical-output, derived-label export, release-verification and figure-generation scripts.
- `docs/numeric_consistency_checks.csv` records automated row-level checks comparing figure source data with the corresponding statistical output files.
- `MANIFEST.csv` records SHA-256 checksums for released files.

The package excludes raw message text, user identifiers, linked user histories, API keys and archived `previous/` folders. Raw public corpora should be obtained from their original providers under their own licences and terms.

## Automated Checks

- Active LaTeX dependency check: all active `\input`, `\include` and `\includegraphics` targets were present.
- Active citation check: all 53 active citation keys were present in `sn-bibliography.bib`.
- Active reference metadata check: active article, conference, book and chapter references had a DOI, URL or ISBN after cleanup.
- Numeric source-data check: row-level checks in `numeric_consistency_checks.csv` pass for the manuscript source-data values covered by that file.
- Derived label-table check: conversation counts, user-turn counts and assistant-turn counts matched Table 1 for all six main task settings.
- Derived label-table leakage scan found no raw message-text fields, original conversation identifiers, URLs, timestamps, API-key strings, internal absolute paths or archived non-current labels.
- Derived label-table support coding check verified that blank support-type rows remain blank on the scaffolded indicator and are not encoded as non-scaffolded reference rows.
- Derived label-table identifier check verified that public `*_hash` columns now contain release-local random pseudonymous IDs rather than deterministic SHA-256 hashes of raw corpus identifiers.
- Figure 3 panel b source data matched `statistical_outputs/integrated_regression/fig3_adjusted_model_significance.csv`.
- Figure 3 panel c source data matched `statistical_outputs/integrated_regression/fig3_user_framing_stratified_poisson_significance.csv`.
- Figure 5 panel a source data matched `statistical_outputs/integrated_regression/key_percentage_lifts_significance.csv`.
- Active-source wording scan found no remaining active occurrences of obsolete comparison-corpus terms, obsolete response terminology, matched-setting terminology, strictness wording or measured-user-status wording.
- LaTeX compilation completed successfully with `latexmk -pdf -interaction=nonstopmode -halt-on-error sn-article.tex`.

## Table 1 Verification

The Table 1 total counts were rechecked from the displayed setting rows: 128,569 conversations, 491,685 user turns and 489,785 assistant turns. Weighted pooled values recomputed from rounded row displays matched the table to rounding precision for user intent, scaffolded support, cognitive engagement and constructive engagement. The emotional-engagement pooled value recomputed from rounded displayed rows is 0.75%, whereas the table reports 0.74%; this is consistent with using unrounded underlying row values rather than the rounded table display.

## Nature-Facing Materials Present

- Data availability statement: present in the paper repository at `sections/06-declarations.tex`.
- Code availability statement: present in the paper repository at `sections/06-declarations.tex`.
- Ethics statement: present in `sections/06-declarations.tex`.
- Competing interests: present in `sections/06-declarations.tex`.
- Author contributions: present, but final author initials and role allocation remain a team-level item.
- Acknowledgements and funding: present, but final funder names and grant numbers remain a team-level item.
- LLM use statement: present in `sections/06-declarations.tex`.
- Figure source data statement: present in `sections/06-declarations.tex`.

## Remaining Manual Items Before Submission

- Publish the updated `v0.1.3` GitHub release so that Zenodo can archive the current submission package, then verify that the displayed Zenodo metadata matches `.zenodo.json` and `CITATION.cff`.
- Confirm final author contributions, acknowledgements, funding and ethics wording against the submission system metadata.
- Decide whether the final journal upload should use the modular Overleaf source or a flattened single `.tex` file with embedded bibliography, depending on the journal production instructions.
- Confirm whether the final journal upload should also include rendered figure PDFs/SVGs in addition to numeric source-data CSVs.

## Notes

The current submission package is a derived-data and source-data package, not a raw-data redistribution. This is intentional because the project uses public conversation corpora released by third parties and the manuscript should avoid redistributing raw message text or user-level traces. The camera-ready figure scripts and `source_data/` files reproduce the reported figure values; full re-annotation from raw conversations requires access to the original public corpora and user-provided API credentials.
