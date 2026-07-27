#!/usr/bin/env python3
"""
ASRP Risk Assessment Module (Layer 3.7)
========================================
Calculates Security Health Score (0-100), Risk Rating (Grade A/B/C/F),
Business Impact Context, and SLA-based Remediation Roadmap.
"""

import os
import sys
import json
import yaml
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


def load_yaml(filepath):
    """Utility to safely load a YAML file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_json(data, filepath):
    """Utility to safely save a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class RiskAssessor:
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

    def _find_latest_run_id(self):
        """Find the most recent run directory in project/runs/."""
        if not os.path.exists(self.runs_dir):
            raise FileNotFoundError(f"No runs directory found for project '{self.project_id}'.")
        
        run_folders = [f for f in os.listdir(self.runs_dir) if f.startswith("run-")]
        if not run_folders:
            raise FileNotFoundError(f"No run folders found under {self.runs_dir}.")
        
        run_folders.sort(reverse=True)
        return run_folders[0]

    def load_business_context(self):
        """Load business context from Layer 1 context.yaml."""
        context_path = os.path.join(self.project_dir, "context.yaml")
        raw = load_yaml(context_path)
        if not raw or "context" not in raw:
            return {
                "business_criticality": "business-critical",
                "data_classification": "pii",
                "risk_tier": "high"
            }
        
        c = raw.get("context", {})
        sec = c.get("security", {})
        biz = c.get("business", {})
        return {
            "business_criticality": biz.get("criticality", "business-critical"),
            "data_classification": sec.get("data_classification", "pii"),
            "risk_tier": sec.get("risk_tier", "high")
        }

    def calculate_risk_score(self, findings_payload, context):
        """Calculate Security Health Score (0-100) based on findings and risk tier."""
        findings = findings_payload.get("findings", [])
        severity_counts = findings_payload.get("severity_summary", {
            "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0
        })

        # Risk Multiplier based on project risk tier
        risk_tier = context.get("risk_tier", "high").lower()
        multipliers = {
            "high": 1.2,
            "medium": 1.0,
            "low": 0.8
        }
        multiplier = multipliers.get(risk_tier, 1.0)

        # Base score 100
        base_score = 100.0
        deduction = (
            (severity_counts.get("CRITICAL", 0) * 15) +
            (severity_counts.get("HIGH", 0) * 8) +
            (severity_counts.get("MEDIUM", 0) * 3) +
            (severity_counts.get("LOW", 0) * 1)
        ) * multiplier

        final_score = max(0, min(100, round(base_score - deduction)))

        # Assign Grade
        if final_score >= 90:
            grade = "A"
            rating = "EXCELLENT / LOW RISK"
            status = "PASS"
        elif final_score >= 75:
            grade = "B"
            rating = "GOOD / MEDIUM RISK"
            status = "PASS WITH WARNINGS"
        elif final_score >= 50:
            grade = "C"
            rating = "NEEDS IMPROVEMENT / HIGH RISK"
            status = "CONDITIONAL APPROVAL"
        else:
            grade = "F"
            rating = "FAIL / CRITICAL RISK"
            status = "ACTION REQUIRED"

        return {
            "security_score": final_score,
            "grade": grade,
            "rating": rating,
            "status": status,
            "total_deduction": round(deduction, 1),
            "multiplier_applied": multiplier,
            "severity_counts": severity_counts
        }

    def build_remediation_roadmap(self, findings):
        """Build SLA-based Remediation Roadmap."""
        phase1_immediate = [] # SLA: 24h-48h
        phase2_shortterm = [] # SLA: 7 days
        phase3_maintenance = [] # SLA: 30 days

        for f in findings:
            sev = f.get("severity", "MEDIUM").upper()
            cat = f.get("category", "")
            
            entry = {
                "finding_id": f.get("finding_id"),
                "title": f.get("title"),
                "engine": f.get("engine"),
                "severity": sev,
                "file": f.get("location", {}).get("file_path", "unknown"),
                "remediation_summary": f.get("remediation", {}).get("summary", "")
            }

            if sev == "CRITICAL" or (sev == "HIGH" and cat in ["secrets", "injection", "access-control"]):
                phase1_immediate.append(entry)
            elif sev == "HIGH":
                phase2_shortterm.append(entry)
            else:
                phase3_maintenance.append(entry)

        return {
            "phase_1_immediate": {
                "sla": "24 hours - 48 hours",
                "priority_level": "P0 - Emergency Fixes",
                "count": len(phase1_immediate),
                "items": phase1_immediate
            },
            "phase_2_shortterm": {
                "sla": "7 days",
                "priority_level": "P1 - High Priority Hardening",
                "count": len(phase2_shortterm),
                "items": phase2_shortterm
            },
            "phase_3_maintenance": {
                "sla": "30 days",
                "priority_level": "P2 - General Security Maintenance",
                "count": len(phase3_maintenance),
                "items": phase3_maintenance
            }
        }

    def run(self):
        """Execute Risk Assessment and output risk_assessment.json."""
        findings_file = os.path.join(self.target_run_dir, "findings.json")
        findings_payload = load_json(findings_file)
        
        if not findings_payload:
            raise FileNotFoundError(f"findings.json not found in {self.target_run_dir}. Run Findings Normalizer first.")

        context = self.load_business_context()
        scoring_results = self.calculate_risk_score(findings_payload, context)
        roadmap = self.build_remediation_roadmap(findings_payload.get("findings", []))

        output_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "assessed_at": datetime.now().isoformat() + "Z",
            "business_context": context,
            "risk_scoring": scoring_results,
            "remediation_roadmap": roadmap
        }

        output_file = os.path.join(self.target_run_dir, "risk_assessment.json")
        save_json(output_payload, output_file)

        print(f"\n=======================================================")
        print(f"📊 STARTING RISK ASSESSMENT ENGINE")
        print(f"📌 Project: {self.project_id} | Run ID: {self.run_id}")
        print(f"🏢 Business Context: Criticality={context['business_criticality']} | Risk Tier={context['risk_tier']}")
        print(f"=======================================================")
        print(f"🎯 SECURITY HEALTH SCORE : {scoring_results['security_score']}/100 (GRADE {scoring_results['grade']})")
        print(f"🏷️  SECURITY RATING       : {scoring_results['rating']}")
        print(f"🚨 GATE STATUS           : {scoring_results['status']}")
        print(f"-------------------------------------------------------")
        print(f"📅 ROADMAP SUMMARY:")
        print(f"   • Phase 1 (Immediate SLA 24-48h): {roadmap['phase_1_immediate']['count']} items")
        print(f"   • Phase 2 (Short-term SLA 7d)  : {roadmap['phase_2_shortterm']['count']} items")
        print(f"   • Phase 3 (Maintenance SLA 30d): {roadmap['phase_3_maintenance']['count']} items")
        print(f"=======================================================")
        print(f"🎉 SUCCESS: risk_assessment.json generated successfully!")
        print(f"📍 Location: {output_file}\n")


def main():
    parser = argparse.ArgumentParser(description="ASRP Risk Assessment CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID")
    parser.add_argument("--run-id", default=None, help="Target run ID (defaults to latest)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    assessor = RiskAssessor(workspace_root, project_id=args.project, run_id=args.run_id)
    assessor.run()


if __name__ == "__main__":
    main()
