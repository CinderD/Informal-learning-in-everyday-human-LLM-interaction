# Informal learning in everyday human-LLM interaction

This repository contains the derived data and custom code needed to verify the aggregate figures, tables and statistical summaries for the manuscript "Informal learning in everyday human-LLM interaction".

## Repository Contents

- `source_data/`: numeric source data for the main manuscript figures and selected supplementary figures.
- `derived_label_tables/`: de-identified conversation-level and adjacent-turn analytic labels for the six main WildChat, LMSYS Chat and ShareChat task settings.
- `validation/`: de-identified validation and audit outputs for human agreement and user-framing checks.
- `statistical_outputs/`: bootstrap, confidence-interval, p-value, false-discovery-rate and regression outputs used in the manuscript and supplementary tables.
- `tables/`: LaTeX table source files used in the manuscript and supplementary information.
- `scripts/`: custom scripts for source-data export, de-identified label-table export, statistical summaries and figure generation.
- `docs/`: consistency checks and submission-readiness notes.
- `MANIFEST.csv`: SHA-256 checksums for the released files.

## Data Scope

The released derived label tables cover:

| Corpus | Task setting | Conversations |
|---|---:|---:|
| WildChat | coding | 31,878 |
| WildChat | writing | 39,534 |
| LMSYS Chat | coding | 32,114 |
| LMSYS Chat | writing | 21,023 |
| ShareChat | coding | 2,481 |
| ShareChat | writing | 1,539 |

The repository intentionally does not redistribute raw message text, original conversation identifiers, URLs, timestamps, user identifiers, linked user histories or API keys. Conversation and turn identifiers in `derived_label_tables/` are one-way SHA-256 hashes generated only for joining analytic rows within this release.

The validation files follow the same privacy boundary. User-framing case-level audit files exclude raw first-turn text and original conversation/source identifiers; they retain only de-identified case hashes, corpus/task strata, production labels, human-verified labels and non-identifying decision notes.

Raw public corpora should be obtained from the original providers under their own licences and terms:

- WildChat-4.8M: https://huggingface.co/datasets/allenai/WildChat-4.8M
- LMSYS Chat-1M: https://huggingface.co/datasets/lmsys/lmsys-chat-1m
- ShareChat: https://huggingface.co/datasets/tucnguyen/ShareChat

## Reproduction Notes

Install the lightweight analysis dependencies with:

```bash
python -m pip install -r requirements.txt
```

The released aggregate figures can be regenerated from the included source-data CSV files using:

```bash
python scripts/make_camera_ready_figures.py
python scripts/make_wo_copilot_appendix_figures.py
```

The de-identified label tables can be regenerated only on a machine that has access to the production annotation outputs described in `tables/table_corpus_provenance_artifacts.tex`. Set `PRODUCTION_OUTPUT_ROOT` to the directory containing those outputs:

```bash
export PRODUCTION_OUTPUT_ROOT=/path/to/level_analysis/outputs
python scripts/export_derived_label_tables.py
```

Full re-annotation from raw conversations additionally requires user-provided API credentials and access to the original public corpora. Do not commit API keys or raw corpus files to this repository.
