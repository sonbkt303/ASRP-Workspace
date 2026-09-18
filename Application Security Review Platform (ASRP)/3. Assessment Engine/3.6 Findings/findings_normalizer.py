#!/usr/bin/env python3
"""
ASRP Findings Normalizer Module (Layer 3.6)
============================================
Merges supplementary raw scanner outputs (Semgrep, Gitleaks, Trivy, Checkov,
Custom AI) into existing AI-written findings.json. AI remains primary for
logic/contextual findings; normalizer dedupes by location+rule_id and appends
only new raw tool hits — never replaces AI-only findings.
"""

import os
import sys
import json
import argparse
import yaml
from datetime import datetime

# Force UTF-8 encoding for Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SEVERITY_RANK = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
THRESHOLD_MAX_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}

ENGINE_PRIORITY = {
    "ai_reviewer": 0,
    "custom_ai": 1,
    "semgrep": 2,
    "gitleaks": 3,
    "trivy": 4,
    "checkov": 5,
    "cicd": 6,
}

# Paths from ASRP demo seed (source_acquisition.populate_workspace_files) — never merge as evidence.
SYNTHETIC_PATHS = {
    "app/main.py",
    "config/settings.py",
    "app/api/v1/orders.py",
    "requirements.txt",
}


def load_json(filepath):
    """Utility to safely load a JSON file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_yaml(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def save_json(data, filepath):
    """Utility to safely save a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def passes_severity_threshold(severity: str, threshold: str) -> bool:
    """Return True if finding severity meets assessment severity_threshold."""
    sev = str(severity or "MEDIUM").upper()
    thresh = str(threshold or "low").lower()
    rank = SEVERITY_RANK.get(sev, 2)
    max_rank = THRESHOLD_MAX_RANK.get(thresh, 3)
    return rank <= max_rank


def finding_dedupe_key(finding: dict) -> tuple:
    loc = finding.get("location") or {}
    return (
        finding.get("rule_id") or "",
        finding.get("component_id") or "",
        loc.get("file_path") or "",
        loc.get("start_line"),
    )


def engine_priority(engine: str) -> int:
    return ENGINE_PRIORITY.get(engine or "", 99)


class FindingsNormalizer:
    def __init__(self, workspace_root, project_id="cleverdent", run_id=None):
        self.workspace_root = workspace_root
        self.project_id = project_id

        self.asrp_dir = os.path.join(self.workspace_root, "Application Security Review Platform (ASRP)")
        registry_dir = os.path.join(self.asrp_dir, "1. Projects Registry")

        self.project_dir = os.path.join(registry_dir, self.project_id)
        if os.path.exists(registry_dir):
            for folder in os.listdir(registry_dir):
                if folder.lower() == self.project_id.lower():
                    self.project_dir = os.path.join(registry_dir, folder)
                    self.project_id = folder
                    break

        self.runs_dir = os.path.join(self.project_dir, "runs")

        if run_id:
            self.run_id = run_id
        else:
            self.run_id = self._find_latest_run_id()

        self.target_run_dir = os.path.join(self.runs_dir, self.run_id)
        self.raw_outputs_dir = os.path.join(self.target_run_dir, "raw_outputs")
        self.severity_threshold = self._load_severity_threshold()

    def _find_latest_run_id(self):
        if not os.path.exists(self.runs_dir):
            raise FileNotFoundError(f"No runs directory found for project '{self.project_id}'.")

        run_folders = [f for f in os.listdir(self.runs_dir) if f.startswith("run-")]
        if not run_folders:
            raise FileNotFoundError(f"No run folders found under {self.runs_dir}.")

        run_folders.sort(reverse=True)
        return run_folders[0]

    def _load_severity_threshold(self):
        scan_ctx = load_json(os.path.join(self.target_run_dir, "scan_context.json"))
        if scan_ctx:
            assessment = scan_ctx.get("assessment") or {}
            return assessment.get("severity_threshold", "low")
        assessment = load_yaml(os.path.join(self.project_dir, "assessment.yaml")).get("assessment", {})
        return assessment.get("severity_threshold", "low")

    def _load_component_ids(self):
        components = load_yaml(os.path.join(self.project_dir, "components.yaml")).get("components") or []
        ids = [c.get("id") for c in components if c.get("id")]
        if os.path.isdir(self.raw_outputs_dir):
            for name in os.listdir(self.raw_outputs_dir):
                sub = os.path.join(self.raw_outputs_dir, name)
                if os.path.isdir(sub) and name not in ids:
                    ids.append(name)
        return ids or [None]

    def load_rules_map(self):
        resolved_path = os.path.join(self.target_run_dir, "resolved-rules.json")
        payload = load_json(resolved_path)
        if not payload:
            return {}

        rules_map = {}
        for r in payload.get("rules", []):
            rules_map[r["id"]] = r
        return rules_map

    def _load_execution_summary(self) -> dict:
        summary_path = os.path.join(self.raw_outputs_dir, "execution_summary.json")
        return load_json(summary_path) or {}

    def _is_synthetic_location(self, finding: dict) -> bool:
        loc = (finding.get("location") or {}).get("file_path", "")
        normalized = str(loc).replace("\\", "/").lstrip("./")
        return normalized in SYNTHETIC_PATHS

    def _should_exclude_finding(self, finding: dict) -> bool:
        """Drop scanner hits on ASRP demo seed paths; keep AI-primary FND-* findings."""
        if not self._is_synthetic_location(finding):
            return False
        finding_id = str(finding.get("finding_id") or "")
        return not finding_id.startswith("FND-")

    def normalize_gitleaks(self, raw_data, rules_map, counter, component_id=None):
        findings = []
        if not raw_data or (isinstance(raw_data, dict) and raw_data.get("_meta")):
            return findings, counter

        for item in raw_data:
            rule_id = item.get("RuleID", "ASRP-SEC-001")
            tags = item.get("Tags", [])
            rule_meta = rules_map.get(rule_id, {})
            if not rule_meta:
                for tag in tags:
                    if tag in rules_map:
                        rule_meta = rules_map[tag]
                        rule_id = tag
                        break

            counter += 1
            finding = {
                "finding_id": f"FIND-{self.project_id}-{counter:03d}",
                "rule_id": rule_id,
                "title": rule_meta.get("name", item.get("Description", "Hardcoded Secret Finding")),
                "engine": "gitleaks",
                "category": rule_meta.get("category", "secrets"),
                "severity": rule_meta.get("severity", "high").upper(),
                "component_id": component_id or item.get("component_id"),
                "location": {
                    "file_path": item.get("File", "unknown"),
                    "start_line": item.get("StartLine", 1),
                    "end_line": item.get("EndLine", 1),
                    "commit_sha": item.get("Commit", "head"),
                },
                "evidence": {
                    "code_snippet": item.get("Match", ""),
                    "masked_secret": item.get("Secret", "")[:4] + "****" if item.get("Secret") else "****",
                },
                "standard_mapping": rule_meta.get(
                    "standard_mapping",
                    {
                        "cwe": ["CWE-798"],
                        "owasp_top10_2021": ["A07:2021-Identification and Authentication Failures"],
                    },
                ),
                "remediation": rule_meta.get(
                    "remediation",
                    {"summary": "Remove secret from source; use environment variables or secrets manager."},
                ),
            }
            findings.append(finding)
        return findings, counter

    def normalize_semgrep(self, raw_data, rules_map, counter, component_id=None):
        findings = []
        if not raw_data or (isinstance(raw_data, dict) and raw_data.get("_meta")):
            return findings, counter
        if "results" not in raw_data:
            return findings, counter

        for item in raw_data.get("results", []):
            rule_id = item.get("check_id", "ASRP-SAST-001")
            rule_meta = rules_map.get(rule_id, {})
            extra = item.get("extra", {})
            counter += 1
            finding = {
                "finding_id": f"FIND-{self.project_id}-{counter:03d}",
                "rule_id": rule_id,
                "title": rule_meta.get("name", "SAST Security Finding"),
                "engine": "semgrep",
                "category": rule_meta.get("category", "code_security"),
                "severity": extra.get("severity", rule_meta.get("severity", "medium")).upper(),
                "component_id": component_id or extra.get("component_id"),
                "location": {
                    "file_path": item.get("path", "unknown"),
                    "start_line": item.get("start", {}).get("line", 1),
                    "end_line": item.get("end", {}).get("line", 1),
                    "start_column": item.get("start", {}).get("col", 1),
                    "end_column": item.get("end", {}).get("col", 1),
                },
                "evidence": {
                    "code_snippet": extra.get("lines", ""),
                    "message": extra.get("message", rule_meta.get("description", "")),
                },
                "standard_mapping": rule_meta.get(
                    "standard_mapping",
                    {
                        "cwe": extra.get("metadata", {}).get("cwe", []),
                        "owasp_top10_2021": extra.get("metadata", {}).get("owasp", []),
                    },
                ),
                "remediation": rule_meta.get(
                    "remediation",
                    {"summary": "Apply parameterized queries or input validation."},
                ),
            }
            findings.append(finding)
        return findings, counter

    def normalize_trivy(self, raw_data, rules_map, counter, component_id=None):
        findings = []
        if not raw_data or (isinstance(raw_data, dict) and raw_data.get("_meta")):
            return findings, counter
        if "Results" not in raw_data:
            return findings, counter

        rule_meta = rules_map.get("ASRP-SCA-001", {})

        for result in raw_data.get("Results", []):
            target = result.get("Target", "requirements.txt")
            for vuln in result.get("Vulnerabilities", []):
                counter += 1
                finding = {
                    "finding_id": f"FIND-{self.project_id}-{counter:03d}",
                    "rule_id": rule_meta.get("id", "ASRP-SCA-001"),
                    "title": f"Vulnerable Dependency: {vuln.get('PkgName')} ({vuln.get('VulnerabilityID')})",
                    "engine": "trivy",
                    "category": rule_meta.get("category", "dependencies"),
                    "severity": vuln.get("Severity", "HIGH").upper(),
                    "component_id": component_id or vuln.get("component_id"),
                    "location": {
                        "file_path": target,
                        "package_name": vuln.get("PkgName"),
                        "installed_version": vuln.get("InstalledVersion"),
                        "fixed_version": vuln.get("FixedVersion"),
                    },
                    "evidence": {
                        "cve_id": vuln.get("VulnerabilityID"),
                        "title": vuln.get("Title"),
                    },
                    "standard_mapping": rule_meta.get(
                        "standard_mapping",
                        {
                            "cwe": ["CWE-1395"],
                            "owasp_top10_2021": ["A06:2021-Vulnerable and Outdated Components"],
                        },
                    ),
                    "remediation": {
                        "summary": f"Upgrade {vuln.get('PkgName')} to {vuln.get('FixedVersion')}."
                    },
                }
                findings.append(finding)
        return findings, counter

    def normalize_custom_ai(self, raw_data, rules_map, counter, component_id=None):
        findings = []
        if not raw_data or (isinstance(raw_data, dict) and raw_data.get("_meta")):
            return findings, counter
        if "ai_findings" not in raw_data:
            return findings, counter

        for item in raw_data.get("ai_findings", []):
            rule_id = item.get("rule_id", "ASRP-AI-001")
            rule_meta = rules_map.get(rule_id, {})
            counter += 1
            finding = {
                "finding_id": f"FIND-{self.project_id}-{counter:03d}",
                "rule_id": rule_id,
                "title": rule_meta.get("name", "AI Logic Review Finding"),
                "engine": "custom_ai",
                "category": item.get("focus_domain", "access-control"),
                "severity": rule_meta.get("severity", "high").upper(),
                "component_id": component_id or item.get("component_id"),
                "location": {
                    "file_path": item.get("target_file", "unknown"),
                    "endpoint": item.get("target_endpoint", ""),
                },
                "evidence": {
                    "confidence_score": item.get("confidence_score", 0.9),
                    "reasoning": item.get("reasoning", ""),
                },
                "standard_mapping": rule_meta.get(
                    "standard_mapping",
                    {
                        "cwe": ["CWE-639"],
                        "owasp_top10_2021": ["A01:2021-Broken Access Control"],
                    },
                ),
                "remediation": {
                    "summary": item.get(
                        "suggested_fix",
                        rule_meta.get("remediation", {}).get("summary", ""),
                    )
                },
            }
            findings.append(finding)
        return findings, counter

    def merge_findings(self, existing: list, supplementary: list) -> list:
        """Merge supplementary raw hits into AI-primary findings; dedupe by location+rule_id."""
        merged: dict[tuple, dict] = {}
        for finding in existing:
            key = finding_dedupe_key(finding)
            merged[key] = finding

        for finding in supplementary:
            key = finding_dedupe_key(finding)
            if key not in merged:
                merged[key] = finding
                continue
            current = merged[key]
            if engine_priority(finding.get("engine")) < engine_priority(current.get("engine")):
                # Keep higher-priority engine metadata but preserve AI stage traceability
                preserved = {
                    k: current[k]
                    for k in ("stage_refs", "stage_item_ids", "finding_id")
                    if current.get(k)
                }
                merged[key] = {**finding, **preserved}

        return list(merged.values())

    def _load_technology_map(self) -> dict[str, str]:
        tech_path = os.path.join(self.project_dir, "technologies.yaml")
        raw = load_yaml(tech_path) if os.path.exists(tech_path) else {}
        mapping = {}
        for entry in (raw or {}).get("technologies", []) if isinstance(raw, dict) else []:
            if not isinstance(entry, dict):
                continue
            cid = entry.get("component_id")
            if not cid:
                continue
            lang = entry.get("language", "")
            fw = entry.get("framework", "")
            mapping[cid] = f"{lang} / {fw}".strip(" /") or "Source Sub-repository"
        return mapping

    def build_components_summary(self, findings: list) -> dict:
        tech_map = self._load_technology_map()
        summary = {}
        for f in findings:
            cid = f.get("component_id") or "unknown"
            sev = str(f.get("severity", "MEDIUM")).upper()
            bucket = summary.setdefault(
                cid,
                {
                    "total": 0,
                    "findings_count": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "info": 0,
                    "tech_stack": tech_map.get(cid, "Source Sub-repository"),
                },
            )
            bucket["total"] += 1
            bucket["findings_count"] = bucket["total"]
            key = sev.lower() if sev.lower() in bucket else "medium"
            if key in bucket:
                bucket[key] += 1
        return summary

    def build_severity_summary(self, findings: list) -> dict:
        summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in findings:
            sev = str(f.get("severity", "MEDIUM")).upper()
            summary[sev] = summary.get(sev, 0) + 1
        return summary

    def run(self):
        """Merge raw outputs into existing findings.json (AI-primary)."""
        rules_map = self.load_rules_map()
        component_ids = self._load_component_ids()

        existing_payload = load_json(os.path.join(self.target_run_dir, "findings.json")) or {}
        existing_findings = list(existing_payload.get("findings") or [])

        print(f"\n=======================================================")
        print(f"STARTING FINDINGS NORMALIZER (merge mode)")
        print(f"Project: {self.project_id} | Run ID: {self.run_id}")
        print(f"Existing AI findings: {len(existing_findings)}")
        print(f"Severity threshold: {self.severity_threshold}")
        print(f"=======================================================\n")

        supplementary = []
        counter = len(existing_findings)
        engine_counts = {"gitleaks": 0, "semgrep": 0, "trivy": 0, "custom_ai": 0}
        execution_summary = self._load_execution_summary()
        skip_supplementary = execution_summary.get("all_engines_emulated", False)

        if skip_supplementary:
            print(
                "[!] All scanner engines emulated/empty — skipping supplementary merge "
                "(AI-primary findings only; install native tools for real SAST/SCA evidence)"
            )

        normalizers = [
            ("gitleaks", self.normalize_gitleaks),
            ("semgrep", self.normalize_semgrep),
            ("trivy", self.normalize_trivy),
            ("custom_ai", self.normalize_custom_ai),
        ]

        if not skip_supplementary:
            for cid in component_ids:
                comp_dir = os.path.join(self.raw_outputs_dir, cid) if cid else self.raw_outputs_dir
                if not os.path.isdir(comp_dir):
                    comp_dir = self.raw_outputs_dir
                for engine_name, fn in normalizers:
                    raw_path = os.path.join(comp_dir, f"{engine_name}_raw.json")
                    raw_data = load_json(raw_path)
                    new_findings, counter = fn(raw_data, rules_map, counter, component_id=cid)
                    new_findings = [f for f in new_findings if not self._is_synthetic_location(f)]
                    supplementary.extend(new_findings)
                    engine_counts[engine_name] += len(new_findings)
                    if new_findings:
                        label = cid or "global"
                        print(f"[*] {engine_name} @ {label}: {len(new_findings)} supplementary hits")

        merged = self.merge_findings(existing_findings, supplementary)
        after_synthetic_filter = [f for f in merged if not self._should_exclude_finding(f)]
        synthetic_removed = len(merged) - len(after_synthetic_filter)
        if synthetic_removed:
            print(f"[*] Removed {synthetic_removed} findings on ASRP demo seed paths")

        filtered = [
            f for f in after_synthetic_filter
            if passes_severity_threshold(f.get("severity"), self.severity_threshold)
        ]
        removed = len(after_synthetic_filter) - len(filtered)
        if removed:
            print(f"[*] Filtered {removed} findings below severity_threshold '{self.severity_threshold}'")

        severity_summary = self.build_severity_summary(filtered)
        components_summary = self.build_components_summary(filtered)

        findings_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "normalized_at": datetime.now().isoformat() + "Z",
            "severity_threshold": self.severity_threshold,
            "total_findings": len(filtered),
            "severity_summary": severity_summary,
            "components_summary": components_summary,
            "findings": filtered,
        }

        findings_file = os.path.join(self.target_run_dir, "findings.json")
        save_json(findings_payload, findings_file)

        summary_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "total_findings": len(filtered),
            "severity_summary": severity_summary,
            "components_summary": components_summary,
            "merge_stats": {
                "ai_primary_count": len(existing_findings),
                "supplementary_added": len(supplementary),
                "supplementary_skipped_emulated": skip_supplementary,
                "synthetic_paths_removed": synthetic_removed,
                "after_dedupe": len(merged),
                "after_threshold_filter": len(filtered),
            },
            "by_engine": engine_counts,
        }
        save_json(summary_payload, os.path.join(self.target_run_dir, "findings_summary.json"))

        print(f"\n=======================================================")
        print(f"NORMALIZATION COMPLETE (merge mode)")
        print(f"Location: {findings_file}")
        print(f"Total Findings: {len(filtered)} (AI: {len(existing_findings)}, +raw: {len(supplementary)})")
        print(f"Severity Breakdown: {severity_summary}")
        print(f"=======================================================\n")


def main():
    parser = argparse.ArgumentParser(description="ASRP Findings Normalizer CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID")
    parser.add_argument("--run-id", default=None, help="Target run ID (defaults to latest)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    normalizer = FindingsNormalizer(workspace_root, project_id=args.project, run_id=args.run_id)
    normalizer.run()


if __name__ == "__main__":
    main()
