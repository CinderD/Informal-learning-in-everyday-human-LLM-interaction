"""Verify the public release package.

The checks focus on release-package integrity rather than full re-annotation from
raw public corpora, which requires separate API credentials and raw-data access.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOTALS = {
    "conversations": 128_569,
    "user_turns": 491_685,
    "assistant_turns": 489_785,
}
SUPPORT_VALUES = {"", "S1", "S2"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_SETTING_NAMES = {
    "WildChat coding": "WC coding",
    "WildChat writing": "WC writing",
    "LMSYS coding": "LMSYS coding",
    "LMSYS writing": "LMSYS writing",
    "ShareChat coding": "SC coding",
    "ShareChat writing": "SC writing",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as handle:
        return list(csv.DictReader(handle))


def dataset_slug(name: str) -> str:
    return (
        name.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return [ROOT / line for line in out.splitlines() if line and line != "MANIFEST.csv"]


def check_manifest() -> tuple[bool, str]:
    manifest = ROOT / "MANIFEST.csv"
    if not manifest.exists():
        return False, "MANIFEST.csv is missing"
    with manifest.open(newline="") as handle:
        rows = {row["path"]: row for row in csv.DictReader(handle)}
    failures: list[str] = []
    for path in git_files():
        rel = path.relative_to(ROOT).as_posix()
        row = rows.get(rel)
        if row is None:
            failures.append(f"missing {rel}")
            continue
        size = path.stat().st_size
        digest = sha256_file(path)
        if str(size) != row["size_bytes"] or digest != row["sha256"]:
            failures.append(f"mismatch {rel}")
    extra = sorted(set(rows) - {p.relative_to(ROOT).as_posix() for p in git_files()})
    failures.extend(f"extra {rel}" for rel in extra)
    if failures:
        preview = "; ".join(failures[:8])
        if len(failures) > 8:
            preview += f"; ... {len(failures) - 8} more"
        return False, preview
    return True, f"{len(rows)} files verified"


def check_numeric_consistency() -> tuple[bool, str]:
    path = ROOT / "docs" / "numeric_consistency_checks.csv"
    if not path.exists():
        return False, "docs/numeric_consistency_checks.csv is missing"
    rows = read_csv(path)
    ok_values = [str(row.get("ok", "")).strip().lower() for row in rows]
    failed = sum(value not in {"true", "1", "yes"} for value in ok_values)
    return failed == 0, f"{len(rows) - failed}/{len(rows)} source-data checks passed"


def check_figure2b_source_data() -> tuple[bool, str]:
    """Check Fig. 2b against mean within-conversation user-turn ratios."""
    source_path = ROOT / "source_data" / "figure2_source_data.csv"
    source_rows = [
        row for row in read_csv(source_path)
        if row.get("figure") == "Figure 2" and row.get("panel") == "b"
    ]
    source = {
        (row["setting"], row["measure"], row["group"]): float(row["estimate"])
        for row in source_rows
    }
    failures: list[str] = []
    summary_rows = read_csv(ROOT / "derived_label_tables" / "derived_label_tables_summary.csv")
    for row in summary_rows:
        folder = ROOT / "derived_label_tables" / dataset_slug(row["dataset"]) / row["task"]
        conv = read_csv(folder / "conversation_labels.csv.gz")
        setting = SOURCE_SETTING_NAMES.get(row["setting"], row["setting"])
        for intent_flag, group in [("1", "intentional"), ("0", "unintentional")]:
            sub = [item for item in conv if item["is_intentional"] == intent_flag]
            expected = {
                "Cognitive": sum(float(item["cognitive_overall_user_turn_ratio"]) for item in sub) / len(sub) * 100,
                "Constructive": sum(float(item["constructive_user_turn_ratio"]) for item in sub) / len(sub) * 100,
            }
            for measure, value in expected.items():
                observed = source.get((setting, measure, group))
                if observed is None:
                    failures.append(f"missing {setting} {measure} {group}")
                    continue
                if min(abs(observed - value), abs(observed - round(value, 1))) > 5e-3:
                    failures.append(
                        f"{setting} {measure} {group}: source={observed:.3f}, expected={value:.3f}"
                    )
    if failures:
        return False, "; ".join(failures[:8])
    return True, f"{len(source_rows)} Fig. 2b rows match mean within-conversation ratios"


def check_derived_tables() -> tuple[bool, str]:
    summary_path = ROOT / "derived_label_tables" / "derived_label_tables_summary.csv"
    rows = read_csv(summary_path)
    total_conv = total_user = total_assistant = 0
    failures: list[str] = []
    for row in rows:
        folder = ROOT / "derived_label_tables" / dataset_slug(row["dataset"]) / row["task"]
        conv = read_csv(folder / "conversation_labels.csv.gz")
        u2a = read_csv(folder / "user_to_assistant_pair_labels.csv.gz")
        a2u = read_csv(folder / "assistant_to_user_pair_labels.csv.gz")
        if len(conv) != int(row["conversations"]):
            failures.append(f"{row['dataset']} {row['task']} conversation rows")
        if len(u2a) != int(row["user_to_assistant_pairs"]):
            failures.append(f"{row['dataset']} {row['task']} user-to-assistant rows")
        if len(a2u) != int(row["assistant_to_user_pairs"]):
            failures.append(f"{row['dataset']} {row['task']} assistant-to-user rows")

        total_conv += len(conv)
        total_user += sum(int(item["user_turns"]) for item in conv)
        total_assistant += sum(int(item["assistant_turns"]) for item in conv)

        for item in u2a:
            support = item.get("next_assistant_support_type", "")
            flag = item.get("next_assistant_is_scaffolded", "")
            if support not in SUPPORT_VALUES:
                failures.append(f"{row['dataset']} {row['task']} invalid next support {support!r}")
                break
            if (support, flag) not in {("S2", "1"), ("S1", "0"), ("", "")}:
                failures.append(f"{row['dataset']} {row['task']} invalid next support flag {support!r}/{flag!r}")
                break
        for item in a2u:
            support = item.get("assistant_support_type", "")
            flag = item.get("assistant_is_scaffolded", "")
            if support not in SUPPORT_VALUES:
                failures.append(f"{row['dataset']} {row['task']} invalid assistant support {support!r}")
                break
            if (support, flag) not in {("S2", "1"), ("S1", "0"), ("", "")}:
                failures.append(f"{row['dataset']} {row['task']} invalid assistant support flag {support!r}/{flag!r}")
                break

        for table, columns in [
            (conv, ["conversation_id_hash"]),
            (u2a, ["conversation_id_hash", "user_turn_id_hash"]),
            (a2u, ["conversation_id_hash", "assistant_turn_id_hash"]),
        ]:
            for item in table[:200]:
                for column in columns:
                    if SHA256_RE.fullmatch(item.get(column, "")):
                        failures.append(f"{row['dataset']} {row['task']} sha256-like {column}")
                        break
                if failures and "sha256-like" in failures[-1]:
                    break

    expected = (EXPECTED_TOTALS["conversations"], EXPECTED_TOTALS["user_turns"], EXPECTED_TOTALS["assistant_turns"])
    observed = (total_conv, total_user, total_assistant)
    if observed != expected:
        failures.append(f"Table 1 totals observed={observed} expected={expected}")
    if failures:
        return False, "; ".join(failures[:8])
    return True, f"Table 1 totals verified: conversations={total_conv}, user_turns={total_user}, assistant_turns={total_assistant}"


def write_outputs(checks: list[tuple[str, bool, str]]) -> None:
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    with (docs / "release_verification_checks.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "ok", "details"], lineterminator="\n")
        writer.writeheader()
        for name, ok, details in checks:
            writer.writerow({"check": name, "ok": ok, "details": details})
    lines = [
        "# Release Verification Report",
        "",
        "Date: 2026-07-16",
        "",
        "This report verifies the public release package after applying the v0.1.4 Fig. 2b source-data consistency update and prior release-audit fixes. The checks cover package integrity, manuscript source-data consistency and derived label-table encoding. They do not re-run raw-corpus annotation, which requires separate raw-data access and API credentials.",
        "",
        "## Checks",
        "",
    ]
    for name, ok, details in checks:
        status = "PASS" if ok else "FAIL"
        lines.append(f"- **{status}** `{name}`: {details}")
    lines += [
        "",
        "## Privacy Boundary",
        "",
        "The release contains label-only analytic tables and numeric source values. It excludes raw message text, original conversation identifiers, URLs, timestamps, user identifiers, linked user histories and API keys. The `*_hash` columns in derived label tables are legacy schema names; their current values are release-local random pseudonymous IDs rather than deterministic hashes of raw corpus identifiers.",
        "",
        "## Support-Type Encoding",
        "",
        "Assistant support type is encoded as `S1`, `S2` or blank. Blank support-type rows are outside the scaffolded-versus-reference contrast and have blank scaffolded indicators; they should not be interpreted as non-scaffolded reference rows.",
        "",
        "## Reproduction Scope",
        "",
        "`source_data/` contains the manuscript figure source values; `statistical_outputs/` contains model, bootstrap, confidence-interval, p-value and sensitivity outputs; `derived_label_tables/` supports label-level checks and secondary analyses under the privacy boundary above.",
        "",
    ]
    (docs / "release_verification_report.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Do not update report files.")
    args = parser.parse_args()

    checks = [
        ("numeric_consistency", *check_numeric_consistency()),
        ("figure2b_source_data", *check_figure2b_source_data()),
        ("derived_label_tables", *check_derived_tables()),
        ("manifest", *check_manifest()),
    ]
    if not args.check:
        write_outputs(checks)
    for name, ok, details in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {details}")
    if not all(ok for _, ok, _ in checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
