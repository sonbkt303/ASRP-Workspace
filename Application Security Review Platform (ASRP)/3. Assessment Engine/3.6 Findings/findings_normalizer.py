#!/usr/bin/env python3
"""
ASRP Findings Normalizer Module (Layer 3.6)
============================================
Normalizes raw scanner outputs (Semgrep, Gitleaks, Trivy, Checkov, Custom AI)
into a unified, enriched ASRP Standard Finding Schema.
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Force UTF-8 encoding for Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def load_json(filepath):
    """Utility to safely load a JSON file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, filepath):
    """Utility to safely save a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class FindingsNormalizer:
    def __init__(self, workspace_root, project_id="cleverdent", run_id=None):
        self.workspace_root = workspace_root
        self.project_id = project_id
        
        # Paths setup
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
        
        # Determine target run directory
        if run_id:
            self.run_id = run_id
        else:
            self.run_id = self._find_latest_run_id()
            
        self.target_run_dir = os.path.join(self.runs_dir, self.run_id)
        self.raw_outputs_dir = os.path.join(self.target_run_dir, "raw_outputs")

    def _find_latest_run_id(self):
        """Find the most recent run directory in project/runs/."""
        if not os.path.exists(self.runs_dir):
            raise FileNotFoundError(f"No runs directory found for project '{self.project_id}'.")
        
        run_folders = [f for f in os.listdir(self.runs_dir) if f.startswith("run-")]
        if not run_folders:
            raise FileNotFoundError(f"No run folders found under {self.runs_dir}.")
        
        run_folders.sort(reverse=True)
        return run_folders[0]

    def load_rules_map(self):
        """Load resolved-rules.json to create a lookup dict by rule ID."""
        resolved_path = os.path.join(self.target_run_dir, "resolved-rules.json")
        payload = load_json(resolved_path)
        if not payload:
            return {}
            
        rules_map = {}
        for r in payload.get("rules", []):
            rules_map[r["id"]] = r
        return rules_map

    def normalize_gitleaks(self, raw_data, rules_map, counter):
        """Adapter for Gitleaks raw JSON."""
        findings = []
        if not raw_data:
            return findings, counter

        for item in raw_data:
            rule_id = item.get("RuleID", "ASRP-SEC-001")
            tags = item.get("Tags", [])
            # Search rule metadata
            rule_meta = rules_map.get(rule_id, {})
            if not rule_meta:
                # Search by tag
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
                "location": {
                    "file_path": item.get("File", "unknown"),
                    "start_line": item.get("StartLine", 1),
                    "end_line": item.get("EndLine", 1),
                    "commit_sha": item.get("Commit", "head")
                },
                "evidence": {
                    "code_snippet": item.get("Match", ""),
                    "masked_secret": item.get("Secret", "")[:4] + "****" if item.get("Secret") else "****"
                },
                "standard_mapping": rule_meta.get("standard_mapping", {
                    "cwe": ["CWE-798"],
                    "owasp_top10_2021": ["A07:2021-Identification and Authentication Failures"]
                }),
                "remediation": rule_meta.get("remediation", {
                    "summary": "Loại bỏ secret ra khỏi mã nguồn và quản lý qua biến môi trường."
                })
            }
            findings.append(finding)
        return findings, counter

    def normalize_semgrep(self, raw_data, rules_map, counter):
        """Adapter for Semgrep SAST raw JSON."""
        findings = []
        if not raw_data or "results" not in raw_data:
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
                "location": {
                    "file_path": item.get("path", "unknown"),
                    "start_line": item.get("start", {}).get("line", 1),
                    "end_line": item.get("end", {}).get("line", 1),
                    "start_column": item.get("start", {}).get("col", 1),
                    "end_column": item.get("end", {}).get("col", 1)
                },
                "evidence": {
                    "code_snippet": extra.get("lines", ""),
                    "message": extra.get("message", rule_meta.get("description", ""))
                },
                "standard_mapping": rule_meta.get("standard_mapping", {
                    "cwe": extra.get("metadata", {}).get("cwe", []),
                    "owasp_top10_2021": extra.get("metadata", {}).get("owasp", [])
                }),
                "remediation": rule_meta.get("remediation", {
                    "summary": "Áp dụng Parameterized Query hoặc Input Validation."
                })
            }
            findings.append(finding)
        return findings, counter

    def normalize_trivy(self, raw_data, rules_map, counter):
        """Adapter for Trivy SCA & Container raw JSON."""
        findings = []
        if not raw_data or "Results" not in raw_data:
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
                    "location": {
                        "file_path": target,
                        "package_name": vuln.get("PkgName"),
                        "installed_version": vuln.get("InstalledVersion"),
                        "fixed_version": vuln.get("FixedVersion")
                    },
                    "evidence": {
                        "cve_id": vuln.get("VulnerabilityID"),
                        "title": vuln.get("Title")
                    },
                    "standard_mapping": rule_meta.get("standard_mapping", {
                        "cwe": ["CWE-1395"],
                        "owasp_top10_2021": ["A06:2021-Vulnerable and Outdated Components"]
                    }),
                    "remediation": {
                        "summary": f"Nâng cấp gói {vuln.get('PkgName')} lên phiên bản {vuln.get('FixedVersion')}."
                    }
                }
                findings.append(finding)
        return findings, counter

    def normalize_custom_ai(self, raw_data, rules_map, counter):
        """Adapter for Custom AI Reviewer raw JSON."""
        findings = []
        if not raw_data or "ai_findings" not in raw_data:
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
                "location": {
                    "file_path": item.get("target_file", "unknown"),
                    "endpoint": item.get("target_endpoint", "")
                },
                "evidence": {
                    "confidence_score": item.get("confidence_score", 0.9),
                    "reasoning": item.get("reasoning", "")
                },
                "standard_mapping": rule_meta.get("standard_mapping", {
                    "cwe": ["CWE-639"],
                    "owasp_top10_2021": ["A01:2021-Broken Access Control"]
                }),
                "remediation": {
                    "summary": item.get("suggested_fix", rule_meta.get("remediation", {}).get("summary", ""))
                }
            }
            findings.append(finding)
        return findings, counter

    def run(self):
        """Run normalization across all raw output files."""
        rules_map = self.load_rules_map()
        all_findings = []
        counter = 0

        print(f"\n=======================================================")
        print(f"🔄 STARTING FINDINGS NORMALIZER")
        print(f"📌 Project: {self.project_id} | Run ID: {self.run_id}")
        print(f"=======================================================\n")

        # 1. Gitleaks
        gitleaks_raw = load_json(os.path.join(self.raw_outputs_dir, "gitleaks_raw.json"))
        g_findings, counter = self.normalize_gitleaks(gitleaks_raw, rules_map, counter)
        all_findings.extend(g_findings)
        print(f"[*] Normalized Gitleaks: {len(g_findings)} findings")

        # 2. Semgrep
        semgrep_raw = load_json(os.path.join(self.raw_outputs_dir, "semgrep_raw.json"))
        s_findings, counter = self.normalize_semgrep(semgrep_raw, rules_map, counter)
        all_findings.extend(s_findings)
        print(f"[*] Normalized Semgrep SAST: {len(s_findings)} findings")

        # 3. Trivy
        trivy_raw = load_json(os.path.join(self.raw_outputs_dir, "trivy_raw.json"))
        t_findings, counter = self.normalize_trivy(trivy_raw, rules_map, counter)
        all_findings.extend(t_findings)
        print(f"[*] Normalized Trivy SCA: {len(t_findings)} findings")

        # 4. Custom AI
        custom_ai_raw = load_json(os.path.join(self.raw_outputs_dir, "custom_ai_raw.json"))
        ai_findings, counter = self.normalize_custom_ai(custom_ai_raw, rules_map, counter)
        all_findings.extend(ai_findings)
        print(f"[*] Normalized Custom AI: {len(ai_findings)} findings")

        # Severity breakdown
        severity_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in all_findings:
            sev = f.get("severity", "MEDIUM").upper()
            severity_summary[sev] = severity_summary.get(sev, 0) + 1

        # Output payload
        findings_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "normalized_at": datetime.now().isoformat() + "Z",
            "total_findings": len(all_findings),
            "severity_summary": severity_summary,
            "findings": all_findings
        }

        # Save findings.json
        findings_file = os.path.join(self.target_run_dir, "findings.json")
        save_json(findings_payload, findings_file)

        # Save findings_summary.json
        summary_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "total_findings": len(all_findings),
            "severity_summary": severity_summary,
            "by_engine": {
                "gitleaks": len(g_findings),
                "semgrep": len(s_findings),
                "trivy": len(t_findings),
                "custom_ai": len(ai_findings)
            }
        }
        summary_file = os.path.join(self.target_run_dir, "findings_summary.json")
        save_json(summary_payload, summary_file)

        print(f"\n=======================================================")
        print(f"🎉 NORMALIZATION COMPLETE!")
        print(f"📍 Location: {findings_file}")
        print(f"📊 Total Findings: {len(all_findings)}")
        print(f"📈 Severity Breakdown: {severity_summary}")
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
