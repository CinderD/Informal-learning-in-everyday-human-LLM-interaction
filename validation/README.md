# Validation Artifacts

This directory contains label-only validation outputs used to support the manuscript's annotation-validity claims.

## Files

- `user_framing_450_human_verified_metrics.csv`: aggregate agreement metrics for the human-verified, positive-oversampled user-framing audit.
- `user_framing_450_human_verified_cases_deidentified.csv`: case-level user-framing audit labels without raw text, original conversation identifiers, URLs or timestamps.
- `writing210_final_human_human_agreement_metrics.csv`: final writing-domain human--human agreement metrics for labels used in the manuscript and supplementary analyses.
- `constructive_production_validation_c_vs_non_c_final_metrics.csv`: aggregate human--LLM agreement metrics for the constructive-versus-non-constructive production-label audit.
- `constructive_production_validation_per_label_metrics.csv`: one-vs-rest human--LLM agreement metrics for user engagement production labels.
- `constructive_production_validation_mismatches_human_confirmed.csv`: label-only mismatch metadata from the human-confirmed user engagement production-label audit.
- `assistant_production_validation_per_label_metrics.csv`: one-vs-rest human--LLM agreement metrics for assistant scaffolding and support-form production labels.
- `assistant_production_validation_mismatches_human_confirmed.csv`: label-only mismatch metadata from the human-confirmed assistant production-label audit.
- `wildchat_post_labelling_review_summary.csv`: aggregate composition of WildChat post-labelling review samples, with 100 labelled turns per task and no raw text.

## User-Framing Audit

The user-framing audit sampled 450 first user turns, with 75 cases from each corpus-by-task setting: WildChat coding, WildChat writing, LMSYS Chat coding, LMSYS Chat writing, ShareChat coding and ShareChat writing. The design deliberately oversampled production-positive intentional-framing cases, with 50 production-positive cases and 25 production-negative cases per setting. This validates the label boundary for explicit learning-oriented framing, but it must not be used to estimate population prevalence.

Overall agreement with the production user-framing label was F1 = 0.857, MCC = 0.677 and Gwet's AC1 = 0.671. Task-stratified F1 was 0.924 for coding and 0.779 for writing.

## Writing Human--Human Agreement

The writing agreement file reports final two-reviewer human--human agreement for the writing-210 validation set. The non-scaffolded reference label is not included because it is not reported in the current manuscript tables. The public label name `Scaffolding` corresponds to the production scaffolded-support indicator.

## Production-Label Audits

The user engagement production-label audit sampled 600 user turns across the six corpus-by-task settings, with production constructive cases deliberately oversampled. The assistant production-label audit sampled 180 assistant turns across the same settings, with scaffolded-support and support-form positives deliberately oversampled. These audits validate label boundaries and production-label reliability; they should not be used as population-prevalence samples.

In assistant validation files, `S2` denotes scaffolded support and `S1` denotes the non-scaffolded reference label retained from the production annotation schema.

## WildChat Post-Labelling Review Summary

The WildChat post-labelling review summary records the production-label composition of coding and writing review samples drawn from completed WildChat labelled pools. Each task sample contained 50 user turns and 50 assistant turns. The file is included as aggregate validation provenance only and does not contain raw text or conversation identifiers.

## Privacy Boundary

These files intentionally exclude raw message text, original conversation identifiers, source URLs, timestamps and user identifiers. Case IDs are release-local and are not intended for linkage to raw public corpora.
