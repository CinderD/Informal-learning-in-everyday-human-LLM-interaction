# Informal learning in everyday human-LLM interaction

This repository contains derived data, source values and custom code supporting verification of the aggregate figures, tables and statistical summaries for the manuscript "Informal learning in everyday human-LLM interaction".

## Repository Contents

- `source_data/`: numeric source data used to render the main manuscript figures and Appendix C visual summaries.
- `derived_label_tables/`: compressed, label-only conversation-level and adjacent-turn analytic tables for the six main WildChat, LMSYS Chat and ShareChat task settings.
- `validation/`: label-only validation and audit outputs for human agreement and user-framing checks.
- `statistical_outputs/`: bootstrap, confidence-interval, p-value, false-discovery-rate and regression outputs used in the manuscript and supplementary tables.
- `tables/`: LaTeX table source files used in the manuscript and supplementary information.
- `scripts/`: custom scripts for source-data export, label-table export, release verification, statistical summaries and figure generation.
- `tables/table_prompt_template_summary.tex` and `tables/table_annotation_implementation_controls.tex`: annotation reproducibility summaries covering prompt families, output fields, parser checks, retry logic and rule-based post-processing.
- `docs/`: consistency checks and submission-readiness notes.
- `MANIFEST.csv`: SHA-256 checksums for the released files.

## Data Scope

The released derived label-only tables cover:

| Corpus | Task setting | Conversations |
|---|---:|---:|
| WildChat | coding | 31,878 |
| WildChat | writing | 39,534 |
| LMSYS Chat | coding | 32,114 |
| LMSYS Chat | writing | 21,023 |
| ShareChat | coding | 2,481 |
| ShareChat | writing | 1,539 |

The repository intentionally does not redistribute raw message text, original conversation identifiers, URLs, timestamps, user identifiers, linked user histories or API keys. Conversation and turn identifiers in `derived_label_tables/` use release-local random pseudonymous IDs under legacy `*_hash` column names; they support joins within this release only, and no raw-ID mapping is published. The label-only tables are distributed as `.csv.gz` files to keep the release compact.

The validation files follow the same privacy boundary. User-framing case-level audit files exclude raw first-turn text and original conversation/source identifiers; they retain only release-local case IDs, corpus/task strata, production labels, human-verified labels and non-identifying decision notes.

Raw public corpora should be obtained from the original providers under their own licences and terms:

- WildChat-4.8M: https://huggingface.co/datasets/allenai/WildChat-4.8M
- LMSYS Chat-1M: https://huggingface.co/datasets/lmsys/lmsys-chat-1m
- ShareChat: https://huggingface.co/datasets/tucnguyen/ShareChat

## License

The custom code, derived data and source-value artifacts in this repository are
released under CC0 1.0 Universal (`CC0-1.0`). This licence does not apply to the
third-party raw conversation corpora, which are not redistributed here and remain
subject to their original providers' licences and terms.

## Reproduction Notes

The public release supports two reviewer-facing workflows: integrity checks for
the released derived data and regeneration of the manuscript figures from the
released numeric source data. Full re-annotation and model refitting require the
original public corpora, API credentials and the corpus-scale annotation outputs
described below.

### System requirements

- Python 3.10 or later.
- Linux, macOS or Windows; no non-standard hardware or GPU is required for the
  released verification and figure-generation workflows.
- Python dependencies listed in `requirements.txt`.

The release was tested on Ubuntu Linux with Python 3.10.12, Matplotlib 3.10.9,
NumPy 2.2.6 and SciPy 1.15.3. In a clean environment on a standard server CPU,
creating the virtual environment and installing dependencies took approximately
31 seconds. Installation time will vary with network and package cache state.

### Installation

Create an isolated environment and install the lightweight analysis dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Verification

Run the release integrity checks:

```bash
python scripts/verify_release.py --check
```

Expected output consists of four `PASS` lines covering numeric consistency,
Figure 2b source data, derived label-table totals and manifest integrity. The
check took approximately 12 seconds in the tested environment and works from
both a GitHub clone and an extracted release archive.

### Demo

For a quick reviewer demo, run the following command from the repository root
on the released numeric inputs in `source_data/`:

```bash
python scripts/make_camera_ready_figures.py
```

Expected output: regenerated PDF manuscript figures in `figures/` and editable
SVG files in `figures_svg_editable/final_figures/`.

Typical runtime was approximately 10 seconds in the tested environment and
should generally be under one minute on a standard desktop. Runtime may vary
across systems.

Additional Appendix C visual summaries can be regenerated with:

```bash
python scripts/make_support_intent_form_profile.py
python scripts/make_wildchat_model_family_robustness.py
```

In the tested environment, these two additional commands took approximately
2.5 and 1.8 seconds, respectively.

The corresponding numeric inputs are provided in `source_data/`, and the
precomputed inferential outputs are provided in `statistical_outputs/`.

### Using other compatible analysis outputs

The label-only analytic tables can be regenerated only on a machine that has access to the corpus-scale annotation outputs described in `tables/table_corpus_provenance_artifacts.tex`. Set `PRODUCTION_OUTPUT_ROOT` to the directory containing those outputs:

```bash
export PRODUCTION_OUTPUT_ROOT=/path/to/level_analysis/outputs
python scripts/export_derived_label_tables.py
```

Full re-annotation from raw conversations additionally requires user-provided API credentials and access to the original public corpora. Do not commit API keys or raw corpus files to this repository.
