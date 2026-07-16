# Release Verification Report

Date: 2026-07-16

This report verifies the public release package after applying the v0.1.4 Fig. 2b source-data consistency update and prior release-audit fixes. The checks cover package integrity, manuscript source-data consistency and derived label-table encoding. They do not re-run raw-corpus annotation, which requires separate raw-data access and API credentials.

## Checks

- **PASS** `numeric_consistency`: 18/18 source-data checks passed
- **PASS** `figure2b_source_data`: 24 Fig. 2b rows match mean within-conversation ratios
- **PASS** `derived_label_tables`: Table 1 totals verified: conversations=128569, user_turns=491685, assistant_turns=489785
- **PASS** `manifest`: 118 files verified

## Privacy Boundary

The release contains label-only analytic tables and numeric source values. It excludes raw message text, original conversation identifiers, URLs, timestamps, user identifiers, linked user histories and API keys. The `*_hash` columns in derived label tables are legacy schema names; their current values are release-local random pseudonymous IDs rather than deterministic hashes of raw corpus identifiers.

## Support-Type Encoding

Assistant support type is encoded as `S1`, `S2` or blank. Blank support-type rows are outside the scaffolded-versus-reference contrast and have blank scaffolded indicators; they should not be interpreted as non-scaffolded reference rows.

## Reproduction Scope

`source_data/` contains the manuscript figure source values; `statistical_outputs/` contains model, bootstrap, confidence-interval, p-value and sensitivity outputs; `derived_label_tables/` supports label-level checks and secondary analyses under the privacy boundary above.
