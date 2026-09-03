"""
Layer 5 Report Validator — Step 3 DoD checks for risk_assessment.json and report artifacts.
Used by `asrp.py validate --stage report --run-id {run_id}`.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z0-9_]+\}\}")

REQUIRED_REPORTS = [
    "risk_assessment.json",
    "security_review_report.html",
    "security_review_report.md",
]


@dataclass
class ReportValidationResult:
    project_id: str
    run_id: str
    passed: bool = False
    missing_files: list[str] = field(default_factory=list)
    placeholder_errors: list[str] = field(default_factory=list)
    component_errors: list[str] = field(default_factory=list)
    consistency_errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    @property
    def errors(self) -> list[str]:
        errs: list[str] = []
        errs.extend(f"Missing file: {f}" for f in self.missing_files)
        errs.extend(self.placeholder_errors)
        errs.extend(self.component_errors)
        errs.extend(self.consistency_errors)
        return errs


class ReportValidator:
    def __init__(self, asrp_dir: str, project_id: str, run_id: str):
        self.asrp_dir = asrp_dir
        self.project_id = project_id
        self.run_id = run_id
        registry = os.path.join(asrp_dir, "1. Projects Registry")
        self.project_dir = os.path.join(registry, project_id)
        self.run_dir = os.path.join(self.project_dir, "runs", run_id)

    def _load_json(self, name: str) -> dict | None:
        path = os.path.join(self.run_dir, name)
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _load_yaml_list(self, filename: str, key: str) -> list:
        path = os.path.join(self.project_dir, filename)
        if not os.path.exists(path):
            return []
        import yaml

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        block = data.get(key, [])
        return block if isinstance(block, list) else []

    def run(self) -> ReportValidationResult:
        result = ReportValidationResult(self.project_id, self.run_id)

        for fname in REQUIRED_REPORTS:
            if not os.path.exists(os.path.join(self.run_dir, fname)):
                result.missing_files.append(fname)

        findings = self._load_json("findings.json")
        risk = self._load_json("risk_assessment.json")
        html_path = os.path.join(self.run_dir, "security_review_report.html")

        if os.path.exists(html_path):
            with open(html_path, encoding="utf-8") as f:
                html = f.read()
            for match in PLACEHOLDER_PATTERN.findall(html):
                result.placeholder_errors.append(
                    f"security_review_report.html: unresolved placeholder {match}"
                )
            if 'data-stages="all"' in html and findings:
                refs = [
                    f for f in findings.get("findings", [])
                    if f.get("stage_refs")
                ]
                if refs:
                    result.warnings.append(
                        "Executive HTML may still use data-stages='all' on finding cards"
                    )

        components = self._load_yaml_list("components.yaml", "components")
        comp_ids = [c.get("id") for c in components if c.get("id")]
        comp_summary = (findings or {}).get("components_summary") or {}

        for cid in comp_ids:
            comp_html = os.path.join(self.run_dir, f"security_review_report_{cid}.html")
            comp_md = os.path.join(self.run_dir, f"security_review_report_{cid}.md")
            if not os.path.exists(comp_html):
                result.component_errors.append(f"Missing component report: {comp_html}")
            if not os.path.exists(comp_md):
                result.component_errors.append(f"Missing component report: {comp_md}")
            meta = comp_summary.get(cid) or {}
            if meta and meta.get("health_score") is None:
                result.component_errors.append(
                    f"components_summary[{cid}] missing health_score — run risk_assessor after normalizer"
                )

        if risk and findings:
            scoring = risk.get("risk_scoring", {})
            expected = scoring.get("security_score")
            sev = findings.get("severity_summary") or scoring.get("severity_counts") or {}
            result.stats = {
                "security_score": expected,
                "grade": scoring.get("grade"),
                "total_findings": findings.get("total_findings"),
                "severity_summary": sev,
                "component_reports": len(comp_ids),
            }
            if expected is None:
                result.consistency_errors.append("risk_assessment.json missing risk_scoring.security_score")

        result.passed = (
            not result.missing_files
            and not result.placeholder_errors
            and not result.component_errors
            and not result.consistency_errors
        )
        return result


def print_report_validation_report(result: ReportValidationResult) -> None:
    print(f"\n{'=' * 55}")
    print("STEP 3 REPORT VALIDATION")
    print(f"Project: {result.project_id} | Run: {result.run_id}")
    print(f"{'=' * 55}")
    if result.passed:
        print("[✓] PASS — Step 3 report artifacts valid")
    else:
        print("[X] FAIL — Step 3 report validation errors:")
        for err in result.errors:
            print(f"    • {err}")
    for warn in result.warnings:
        print(f"[!] {warn}")
    if result.stats:
        print(f"Stats: score={result.stats.get('security_score')} "
              f"grade={result.stats.get('grade')} findings={result.stats.get('total_findings')}")
    print(f"{'=' * 55}\n")


def validate_report(
    asrp_dir: str,
    project_id: str,
    run_id: str,
    exit_on_fail: bool = False,
) -> ReportValidationResult:
    validator = ReportValidator(asrp_dir, project_id, run_id)
    result = validator.run()
    print_report_validation_report(result)
    if exit_on_fail and not result.passed:
        import sys

        sys.exit(1)
    return result
