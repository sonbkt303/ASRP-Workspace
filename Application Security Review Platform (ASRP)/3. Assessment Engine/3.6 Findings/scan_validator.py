"""
Layer 3.6 Scan Validator — schema, summary integrity, copy-paste detection,
consolidation checks for Step 2 stage outputs and findings.json.
Used by `asrp.py validate --stage scan --run-id {run_id}`.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any

NON_PASS_STATUSES = frozenset({"FAIL", "WARNING", "TRIGGERED", "CONFIRMED", "REQUIRES_FIX"})

STAGE_FILES = [
    "stage_2_1_standards.json",
    "stage_2_2_domains.json",
    "stage_2_3_rules.json",
    "stage_2_4_checklists.json",
    "stage_2_5_playbooks.json",
    "stage_2_6_threats.json",
    "stage_2_7_guidelines.json",
    "stage_2_8_best_practices.json",
    "stage_2_9_attack_patterns.json",
    "stage_2_10_remediations.json",
    "stage_2_11_case_studies.json",
    "stage_2_12_decision_logs.json",
]

STAGE_ID_BY_FILE = {
    "stage_2_1_standards.json": "2.1",
    "stage_2_2_domains.json": "2.2",
    "stage_2_3_rules.json": "2.3",
    "stage_2_4_checklists.json": "2.4",
    "stage_2_5_playbooks.json": "2.5",
    "stage_2_6_threats.json": "2.6",
    "stage_2_7_guidelines.json": "2.7",
    "stage_2_8_best_practices.json": "2.8",
    "stage_2_9_attack_patterns.json": "2.9",
    "stage_2_10_remediations.json": "2.10",
    "stage_2_11_case_studies.json": "2.11",
    "stage_2_12_decision_logs.json": "2.12",
}

FND_ITEM_ID_PATTERN = re.compile(r"^(FND|FIND)-", re.IGNORECASE)


@dataclass
class ScanValidationResult:
    project_id: str
    run_id: str
    passed: bool = False
    missing_files: list[str] = field(default_factory=list)
    schema_results: dict[str, bool] = field(default_factory=dict)
    schema_errors: dict[str, str] = field(default_factory=dict)
    summary_errors: list[str] = field(default_factory=list)
    copy_paste_errors: list[str] = field(default_factory=list)
    item_id_errors: list[str] = field(default_factory=list)
    consolidation_errors: list[str] = field(default_factory=list)
    freshness_errors: list[str] = field(default_factory=list)
    evidence_errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    @property
    def errors(self) -> list[str]:
        errs: list[str] = []
        errs.extend(f"Missing file: {f}" for f in self.missing_files)
        for fname, msg in self.schema_errors.items():
            if fname == "__tool__":
                errs.append(msg)
            else:
                errs.append(f"Schema fail ({fname}): {msg}")
        errs.extend(self.summary_errors)
        errs.extend(self.copy_paste_errors)
        errs.extend(self.item_id_errors)
        errs.extend(self.consolidation_errors)
        errs.extend(self.freshness_errors)
        errs.extend(self.evidence_errors)
        return errs


class ScanValidator:
    def __init__(
        self,
        asrp_dir: str,
        project_id: str,
        run_id: str,
        skill_refs_dir: str | None = None,
        strict: bool = False,
    ):
        self.asrp_dir = asrp_dir
        self.project_id = project_id
        self.run_id = run_id
        self.strict = strict
        self.project_dir = os.path.join(asrp_dir, "1. Projects Registry", project_id)
        self.run_dir = os.path.join(self.project_dir, "runs", run_id)
        self.stage_dir = os.path.join(self.run_dir, "stage_outputs")
        self.skill_refs_dir = skill_refs_dir or self._default_skill_refs_dir()

    @staticmethod
    def _default_skill_refs_dir() -> str:
        # scan_validator.py lives at ASRP/3. Assessment Engine/3.6 Findings/
        workspace = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )
        return os.path.join(
            workspace,
            ".agents",
            "skills",
            "asrp-security-review",
            "references",
        )

    def run(self) -> ScanValidationResult:
        result = ScanValidationResult(project_id=self.project_id, run_id=self.run_id)

        # File presence
        for fname in STAGE_FILES:
            if not os.path.exists(os.path.join(self.stage_dir, fname)):
                result.missing_files.append(f"stage_outputs/{fname}")

        findings_path = os.path.join(self.run_dir, "findings.json")
        if not os.path.exists(findings_path):
            result.missing_files.append("findings.json")

        if result.missing_files:
            return result

        self._validate_schemas(result)
        if result.schema_errors.get("__tool__"):
            return result

        stage_data = {}
        for fname in STAGE_FILES:
            path = os.path.join(self.stage_dir, fname)
            with open(path, encoding="utf-8") as f:
                stage_data[fname] = json.load(f)

        with open(findings_path, encoding="utf-8") as f:
            findings_data = json.load(f)

        self._validate_summaries(stage_data, result)
        self._validate_item_ids(stage_data, result)
        self._validate_copy_paste(stage_data, result)
        self._validate_consolidation(stage_data, findings_data, result)
        self._validate_profile_freshness(result)
        self._validate_scan_evidence(result)
        self._collect_stats(stage_data, findings_data, result)

        result.passed = (
            not result.missing_files
            and all(result.schema_results.values())
            and not result.summary_errors
            and not result.copy_paste_errors
            and not result.item_id_errors
            and not result.consolidation_errors
            and not result.freshness_errors
            and not result.evidence_errors
            and "__tool__" not in result.schema_errors
        )
        return result

    def _validate_schemas(self, result: ScanValidationResult) -> None:
        if not self._check_jsonschema_available():
            result.schema_errors["__tool__"] = (
                "check-jsonschema not installed. Run: pip install check-jsonschema"
            )
            result.schema_results["__tool__"] = False
            return

        stage_schema = os.path.join(self.skill_refs_dir, "stage-output.schema.json")
        findings_schema = os.path.join(self.skill_refs_dir, "findings.schema.json")

        for fname in STAGE_FILES:
            fpath = os.path.join(self.stage_dir, fname)
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "check_jsonschema",
                    "--schemafile",
                    stage_schema,
                    fpath,
                ],
                capture_output=True,
                text=True,
            )
            if proc.returncode == 0:
                result.schema_results[fname] = True
            else:
                result.schema_results[fname] = False
                detail = (proc.stdout + proc.stderr).strip()
                result.schema_errors[fname] = detail.splitlines()[-1] if detail else "validation failed"

        findings_path = os.path.join(self.run_dir, "findings.json")
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "check_jsonschema",
                "--schemafile",
                findings_schema,
                findings_path,
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            result.schema_results["findings.json"] = True
        else:
            result.schema_results["findings.json"] = False
            detail = (proc.stdout + proc.stderr).strip()
            result.schema_errors["findings.json"] = detail.splitlines()[-1] if detail else "validation failed"

    def _validate_summaries(self, stage_data: dict, result: ScanValidationResult) -> None:
        for fname, data in stage_data.items():
            summary = data.get("summary") or {}
            results = data.get("results") or []
            passed = sum(1 for r in results if r.get("status") == "PASS")
            failed = sum(1 for r in results if r.get("status") == "FAIL")
            warnings = sum(1 for r in results if r.get("status") == "WARNING")
            other = len(results) - passed - failed - warnings
            total = len(results)

            checks = [
                ("total_checks", total),
                ("passed", passed),
                ("failed", failed),
                ("warnings", warnings),
            ]
            for key, actual in checks:
                expected = summary.get(key)
                if expected is not None and expected != actual:
                    result.summary_errors.append(
                        f"{fname}: summary.{key}={expected} but counted {actual} in results[]"
                    )
            if other > 0 and summary.get("total_checks") == total:
                result.warnings.append(
                    f"{fname}: {other} results with non-standard status (TRIGGERED/CONFIRMED/REQUIRES_FIX)"
                )

    def _validate_item_ids(self, stage_data: dict, result: ScanValidationResult) -> None:
        for fname, data in stage_data.items():
            for row in data.get("results") or []:
                item_id = row.get("item_id", "")
                if FND_ITEM_ID_PATTERN.match(str(item_id)):
                    result.item_id_errors.append(
                        f"{fname}: item_id '{item_id}' uses finding namespace (FND-* forbidden in stage files)"
                    )

            stage_id = data.get("stage_id") or STAGE_ID_BY_FILE.get(fname, "")
            non_pass = [r for r in data.get("results") or [] if r.get("status") in NON_PASS_STATUSES]
            all_results = data.get("results") or []
            if stage_id in ("2.1", "2.2", "2.3", "2.4") and non_pass and len(all_results) == len(non_pass):
                msg = f"{fname}: P0 stage has no PASS items — incomplete catalog evaluation"
                if self.strict:
                    result.item_id_errors.append(msg)
                else:
                    result.warnings.append(msg)

    def _load_manifest_hash(self) -> str | None:
        manifest_path = os.path.join(self.project_dir, "registry.manifest.yaml")
        if not os.path.exists(manifest_path):
            return None
        try:
            import yaml
            with open(manifest_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return (data.get("registry_manifest") or {}).get("profile_hash")
        except Exception:
            return None

    def _run_manifest_hash(self) -> str | None:
        for fname in ("scan_context.json", "resolved-rules.json"):
            path = os.path.join(self.run_dir, fname)
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("manifest_hash"):
                    return data.get("manifest_hash")
        return None

    def _validate_profile_freshness(self, result: ScanValidationResult) -> None:
        """Ensure run manifest_hash matches current registry.manifest (Step 1 not stale)."""
        expected = self._load_manifest_hash()
        actual = self._run_manifest_hash()
        if not expected or not actual:
            result.warnings.append("Could not compare manifest_hash (missing manifest or run metadata)")
            return
        if expected != actual:
            result.freshness_errors.append(
                f"Profile stale: run manifest_hash ({actual[:20]}...) != "
                f"registry.manifest profile_hash ({expected[:20]}...). Re-sign-off or re-run rule_resolver."
            )
        else:
            result.stats["manifest_hash_match"] = True

    def _validate_scan_evidence(self, result: ScanValidationResult) -> None:
        """Warn/fail when tools are enabled but all scanner output is emulated or empty."""
        summary_path = os.path.join(self.run_dir, "raw_outputs", "execution_summary.json")
        if not os.path.exists(summary_path):
            result.warnings.append("raw_outputs/execution_summary.json missing — scanner not run")
            return

        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)

        tools_enabled = summary.get("tools_enabled") or {}
        any_tool_on = any(tools_enabled.values()) if tools_enabled else True
        all_emulated = summary.get("all_engines_emulated", True)
        total_raw = summary.get("total_raw_findings", 0)

        result.stats["all_engines_emulated"] = all_emulated
        result.stats["total_raw_findings"] = total_raw

        if any_tool_on and all_emulated:
            msg = (
                "All scanner engines emulated/empty while assessment.tools_enabled is true — "
                "install native tools (gitleaks, semgrep, trivy) or use --allow-emulated for dev only"
            )
            if self.strict:
                result.evidence_errors.append(msg)
            else:
                result.warnings.append(msg)

    def _results_fingerprint(self, results: list) -> str:
        """Hash non-PASS results for copy-paste detection."""
        non_pass = [r for r in results if r.get("status") in NON_PASS_STATUSES]
        canonical = json.dumps(non_pass, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def _validate_copy_paste(self, stage_data: dict, result: ScanValidationResult) -> None:
        fingerprints: dict[str, list[str]] = {}
        for fname, data in stage_data.items():
            fp = self._results_fingerprint(data.get("results") or [])
            if not fp or fp == hashlib.sha256(b"[]").hexdigest():
                continue
            fingerprints.setdefault(fp, []).append(fname)

        for fp, files in fingerprints.items():
            if len(files) >= 2:
                result.copy_paste_errors.append(
                    f"Identical non-PASS results[] across stages: {', '.join(files)} "
                    "(copy-paste anti-pattern — use catalog-specific item_ids per stage)"
                )

    @staticmethod
    def _finding_key(row: dict) -> tuple | None:
        evidence = row.get("evidence") or {}
        file_path = evidence.get("file_path") or ""
        start_line = evidence.get("start_line")
        rule_id = row.get("rule_id") or row.get("item_id") or ""
        component_id = row.get("component_id") or ""
        if not file_path and not rule_id:
            return None
        return (rule_id, component_id, file_path, start_line)

    def _validate_consolidation(
        self,
        stage_data: dict,
        findings_data: dict,
        result: ScanValidationResult,
    ) -> None:
        stage_keys: dict[tuple, set[str]] = {}
        stage_item_map: dict[tuple, set[str]] = {}

        for fname, data in stage_data.items():
            stage_id = data.get("stage_id") or STAGE_ID_BY_FILE.get(fname, "")
            for row in data.get("results") or []:
                if row.get("status") not in NON_PASS_STATUSES:
                    continue
                key = self._finding_key(row)
                if not key:
                    continue
                stage_keys.setdefault(key, set()).add(stage_id)
                stage_item_map.setdefault(key, set()).add(str(row.get("item_id", "")))

        findings = findings_data.get("findings") or []
        findings_by_key: dict[tuple, dict] = {}
        seen_finding_keys: set[tuple] = set()

        for finding in findings:
            loc = finding.get("location") or {}
            key = (
                finding.get("rule_id") or "",
                finding.get("component_id") or "",
                loc.get("file_path") or "",
                loc.get("start_line"),
            )
            if key in seen_finding_keys:
                result.consolidation_errors.append(
                    f"findings.json duplicate key: rule_id={key[0]}, file={key[2]}:{key[3]}"
                )
            seen_finding_keys.add(key)
            findings_by_key[key] = finding

        for key, stage_refs in stage_keys.items():
            rule_id, component_id, file_path, start_line = key
            matched = findings_by_key.get(key)
            if not matched:
                # Try fuzzy match without start_line
                alt_key = (rule_id, component_id, file_path, None)
                matched = next(
                    (f for k, f in findings_by_key.items() if k[:3] == alt_key[:3]),
                    None,
                )
            if not matched:
                result.consolidation_errors.append(
                    f"Non-PASS stage item not in findings.json: {rule_id} @ {file_path}:{start_line}"
                )
                continue

            finding_stage_refs = set(matched.get("stage_refs") or [])
            finding_item_ids = set(matched.get("stage_item_ids") or [])
            expected_items = stage_item_map.get(key, set())

            if stage_refs and not stage_refs.intersection(finding_stage_refs):
                result.consolidation_errors.append(
                    f"Finding {matched.get('finding_id')}: stage_refs missing mapped stages {stage_refs}"
                )
            if expected_items and not expected_items.intersection(finding_item_ids):
                result.warnings.append(
                    f"Finding {matched.get('finding_id')}: stage_item_ids may not include catalog IDs {expected_items}"
                )

        result.stats["unique_stage_keys"] = len(stage_keys)
        result.stats["findings_count"] = len(findings)

    def _collect_stats(
        self,
        stage_data: dict,
        findings_data: dict,
        result: ScanValidationResult,
    ) -> None:
        non_pass_total = 0
        for data in stage_data.values():
            non_pass_total += sum(
                1 for r in data.get("results") or [] if r.get("status") in NON_PASS_STATUSES
            )
        result.stats["non_pass_stage_items"] = non_pass_total
        result.stats["unique_findings"] = findings_data.get("total_findings", len(findings_data.get("findings") or []))
        result.stats["copy_paste_groups"] = len(result.copy_paste_errors)

    @staticmethod
    def _check_jsonschema_available() -> bool:
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "check_jsonschema", "--version"],
                capture_output=True,
                text=True,
            )
            return proc.returncode == 0
        except Exception:
            return False


def print_scan_validation_report(result: ScanValidationResult) -> None:
    print(f"\n=======================================================")
    print(f"Step 2 Scan Validation: {result.project_id} / {result.run_id}")
    print(f"=======================================================\n")

    print("── Stage Files ──")
    for fname in STAGE_FILES:
        if f"stage_outputs/{fname}" in result.missing_files:
            print(f"  [X] Missing: stage_outputs/{fname}")
        elif result.schema_results.get(fname):
            print(f"  [✓] {fname} — schema pass")
        elif fname in result.schema_errors:
            print(f"  [X] {fname} — schema fail")
        else:
            print(f"  [✓] {fname} — found")

    if "findings.json" in result.missing_files:
        print("  [X] Missing: findings.json")
    elif result.schema_results.get("findings.json"):
        print("  [✓] findings.json — schema pass")
    elif "findings.json" in result.schema_errors:
        print("  [X] findings.json — schema fail")

    if result.schema_errors.get("__tool__"):
        print(f"\n  [!] {result.schema_errors['__tool__']}")

    sections = [
        ("Summary Integrity", result.summary_errors),
        ("Copy-Paste Check", result.copy_paste_errors),
        ("Item ID Namespace", result.item_id_errors),
        ("Consolidation", result.consolidation_errors),
        ("Profile Freshness", result.freshness_errors),
        ("Scan Evidence", result.evidence_errors),
    ]
    for title, items in sections:
        print(f"\n── {title} ──")
        if items:
            for err in items:
                print(f"  [X] {err}")
        else:
            print("  [✓] pass")

    if result.warnings:
        print("\n── Warnings ──")
        for w in result.warnings:
            print(f"  [!] {w}")

    if result.stats:
        print("\n── Stats ──")
        for k, v in result.stats.items():
            print(f"  • {k}: {v}")

    print("\n-------------------------------------------------------")
    if result.passed:
        print("STEP 2 SCAN VALIDATION PASSED — ready for Step 3 report.\n")
    else:
        print("[X] STEP 2 SCAN VALIDATION FAILED.\n")
        for err in result.errors:
            print(f"    • {err}")
        print()


def validate_scan(
    asrp_dir: str,
    project_id: str,
    run_id: str,
    exit_on_fail: bool = False,
    strict: bool = False,
) -> ScanValidationResult:
    validator = ScanValidator(asrp_dir, project_id, run_id, strict=strict)
    result = validator.run()
    print_scan_validation_report(result)
    if exit_on_fail and not result.passed:
        sys.exit(1)
    return result
