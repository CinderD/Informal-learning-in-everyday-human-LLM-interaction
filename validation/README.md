# Validation Artifacts

This directory contains de-identified validation outputs used to support the manuscript's annotation-validity claims.

## Files

- `user_framing_450_human_verified_metrics.csv`: aggregate agreement metrics for the Zixin human-verified, positive-oversampled user-framing audit.
- `user_framing_450_human_verified_cases_deidentified.csv`: case-level user-framing audit labels without raw text, original conversation identifiers, URLs or timestamps.
- `writing210_final_human_human_agreement_metrics.csv`: final writing-domain human--human agreement metrics for labels used in the manuscript and supplementary analyses.

## User-Framing Audit

The user-framing audit sampled 450 first user turns, with 75 cases from each corpus-by-task setting: WildChat coding, WildChat writing, LMSYS Chat coding, LMSYS Chat writing, ShareChat coding and ShareChat writing. The design deliberately oversampled production-positive intentional-framing cases, with 50 production-positive cases and 25 production-negative cases per setting. This validates the label boundary for explicit learning-oriented framing, but it must not be used to estimate population prevalence.

Overall agreement with the production user-framing label was F1 = 0.857, MCC = 0.677 and Gwet's AC1 = 0.671. Task-stratified F1 was 0.924 for coding and 0.779 for writing.

## Writing Human--Human Agreement

The writing agreement file reports final Zixin--Haotian agreement for the writing-210 validation set. The non-scaffolded reference label is not included because it is not reported in the current manuscript tables. The public label name `Scaffolding` corresponds to the production scaffolded-support indicator.

## Privacy Boundary

These files intentionally exclude raw message text, original conversation identifiers, source URLs, timestamps and user identifiers. Case hashes are generated for this release only and are not intended for linkage to raw public corpora.
