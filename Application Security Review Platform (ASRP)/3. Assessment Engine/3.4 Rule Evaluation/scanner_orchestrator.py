#!/usr/bin/env python3
"""
ASRP Scanner Orchestrator Module (Layer 3.4)
=============================================
Orchestrates security scans based on resolved-rules.json across SAST,
Secrets, SCA, IaC, CI/CD, and Custom AI engines. Scans component clone
paths (not registry folder) with exclude_paths support.
"""

import os
import sys
import json
import time
import shutil
import argparse
import subprocess
import yaml
from datetime import datetime

# Force UTF-8 encoding for Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

ENGINE_TOOL_MAP = {
    "gitleaks": "secrets",
    "semgrep": "sast",
    "trivy": "sca",
    "checkov": "iac",
    "cicd": "sast",
    "custom_ai": "sast",
}


def load_json(filepath):
    """Utility to safely load a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
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


class ScannerOrchestrator:
    def __init__(self, workspace_root, project_id="cleverdent", run_id=None, allow_emulated=False):
        self.workspace_root = workspace_root
        self.project_id = project_id
        self.allow_emulated = allow_emulated

        self.asrp_dir = os.path.join(self.workspace_root, "Application Security Review Platform (ASRP)")
        registry_dir = os.path.join(self.asrp_dir, "1. Projects Registry")

        self.project_dir = os.path.join(registry_dir, self.project_id)
        if os.path.exists(registry_dir):
            for folder in os.listdir(registry_dir):
                if folder.lower() == self.project_id.lower():
                    self.project_dir = os.path.join(registry_dir, folder)
                    self.project_id = folder
                    break

        self.clones_dir = os.path.join(
            self.asrp_dir, "3. Assessment Engine", "3.1 Source Acquisition", "clones"
        )
        self.runs_dir = os.path.join(self.project_dir, "runs")

        if run_id:
            self.run_id = run_id
        else:
            self.run_id = self._find_latest_run_id()

        self.target_run_dir = os.path.join(self.runs_dir, self.run_id)
        self.raw_outputs_dir = os.path.join(self.target_run_dir, "raw_outputs")
        self.components = self._load_components()
        self.tools_enabled = self._load_tools_enabled()
        self.emulated_flags = {}

    def _find_latest_run_id(self):
        if not os.path.exists(self.runs_dir):
            raise FileNotFoundError(
                f"No runs directory found for project '{self.project_id}'. Run Rule Resolver first."
            )
        run_folders = [f for f in os.listdir(self.runs_dir) if f.startswith("run-")]
        if not run_folders:
            raise FileNotFoundError(f"No run folders found under {self.runs_dir}. Run Rule Resolver first.")
        run_folders.sort(reverse=True)
        return run_folders[0]

    def _load_components(self):
        comp_path = os.path.join(self.project_dir, "components.yaml")
        data = load_yaml(comp_path)
        return data.get("components") or []

    def _load_tools_enabled(self):
        assessment_path = os.path.join(self.project_dir, "assessment.yaml")
        data = load_yaml(assessment_path).get("assessment", {})
        return data.get("tools_enabled") or {}

    def _component_clone_path(self, component_id):
        return os.path.join(self.clones_dir, self.project_id, component_id)

    def _resolve_scan_root(self, component):
        """Return clone root for a component (single scan root per component)."""
        cid = component.get("id")
        clone_root = self._component_clone_path(cid)
        if not os.path.isdir(clone_root):
            print(f"[!] Warning: Clone not found for component '{cid}': {clone_root}")
            return None
        return clone_root

    def _engine_enabled(self, engine):
        tool_type = ENGINE_TOOL_MAP.get(engine, "sast")
        return self.tools_enabled.get(tool_type, True)

    def check_tool_available(self, command_name):
        return shutil.which(command_name) is not None

    def _empty_payload(self, engine, reason):
        return {"_meta": {"emulated": True, "reason": reason, "engine": engine}}

    def execute_gitleaks(self, rules, source_path, out_dir, component_id):
        is_native = self.check_tool_available("gitleaks")
        mode = "Native Binary" if is_native else "Emulated Runner"
        print(f"[*] Engine: Gitleaks ({len(rules)} rules) @ {component_id} -> {mode}")

        if is_native:
            try:
                cmd = ["gitleaks", "detect", "--source", source_path, "--report-format", "json", "--no-git"]
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                raw_data = json.loads(res.stdout) if res.stdout else []
            except Exception as e:
                print(f"[!] Native Gitleaks failed: {e}. Falling back.")
                is_native = False

        if not is_native:
            if not self.allow_emulated:
                raw_data = self._empty_payload("gitleaks", "gitleaks binary not available")
            else:
                raw_data = [
                    {
                        "Description": r["name"],
                        "StartLine": 12,
                        "File": "config/settings.py",
                        "RuleID": r.get("engine_config", {}).get("gitleaks_rule_id", "generic-api-key"),
                        "Tags": [r["id"], r.get("severity", "MEDIUM")],
                        "component_id": component_id,
                    }
                    for r in rules
                ]

        output_file = os.path.join(out_dir, "gitleaks_raw.json")
        save_json(raw_data, output_file)
        count = len(raw_data) if isinstance(raw_data, list) else 0
        return count, mode, not is_native

    def execute_semgrep(self, rules, source_path, out_dir, component_id):
        is_native = self.check_tool_available("semgrep")
        mode = "Native Binary" if is_native else "Emulated Runner"
        print(f"[*] Engine: Semgrep ({len(rules)} rules) @ {component_id} -> {mode}")

        if is_native:
            try:
                cmd = ["semgrep", "scan", "--json", source_path]
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                raw_data = json.loads(res.stdout) if res.stdout else {"results": []}
            except Exception as e:
                print(f"[!] Native Semgrep failed: {e}. Falling back.")
                is_native = False

        if not is_native:
            if not self.allow_emulated:
                raw_data = self._empty_payload("semgrep", "semgrep binary not available")
            else:
                raw_data = {
                    "results": [
                        {
                            "check_id": r["id"],
                            "path": "app/main.py",
                            "start": {"line": 45, "col": 5},
                            "extra": {
                                "message": r.get("description", r.get("name", "")),
                                "severity": r.get("severity", "MEDIUM").upper(),
                                "component_id": component_id,
                            },
                        }
                        for r in rules
                    ],
                    "errors": [],
                }

        output_file = os.path.join(out_dir, "semgrep_raw.json")
        save_json(raw_data, output_file)
        if isinstance(raw_data, dict) and "_meta" in raw_data:
            return 0, mode, True
        return len(raw_data.get("results", [])), mode, not is_native

    def execute_trivy(self, rules, source_path, out_dir, component_id):
        is_native = self.check_tool_available("trivy")
        mode = "Native Binary" if is_native else "Emulated Runner"
        print(f"[*] Engine: Trivy ({len(rules)} rules) @ {component_id} -> {mode}")

        if is_native:
            try:
                cmd = ["trivy", "fs", "--format", "json", source_path]
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                raw_data = json.loads(res.stdout) if res.stdout else {"Results": []}
            except Exception as e:
                print(f"[!] Native Trivy failed: {e}. Falling back.")
                is_native = False

        if not is_native:
            if not self.allow_emulated:
                raw_data = self._empty_payload("trivy", "trivy binary not available")
            else:
                raw_data = {
                    "Results": [
                        {
                            "Target": "requirements.txt",
                            "Vulnerabilities": [
                                {
                                    "VulnerabilityID": "CVE-2023-32681",
                                    "Severity": "HIGH",
                                    "component_id": component_id,
                                }
                            ],
                        }
                    ]
                }

        output_file = os.path.join(out_dir, "trivy_raw.json")
        save_json(raw_data, output_file)
        if isinstance(raw_data, dict) and "_meta" in raw_data:
            return 0, mode, True
        count = sum(len(res.get("Vulnerabilities", [])) for res in raw_data.get("Results", []))
        return count, mode, not is_native

    def execute_custom_ai(self, rules, source_path, out_dir, component_id):
        mode = "Internal LLM Agent"
        print(f"[*] Engine: Custom AI ({len(rules)} rules) @ {component_id} -> {mode}")

        if not self.allow_emulated:
            raw_data = self._empty_payload("custom_ai", "custom_ai requires AI audit phase (Phase 2B)")
        else:
            raw_data = {
                "ai_findings": [
                    {
                        "rule_id": r["id"],
                        "focus_domain": r.get("category"),
                        "target_file": "app/api/v1/orders.py",
                        "confidence_score": 0.92,
                        "component_id": component_id,
                    }
                    for r in rules
                ]
            }

        output_file = os.path.join(out_dir, "custom_ai_raw.json")
        save_json(raw_data, output_file)
        if isinstance(raw_data, dict) and "_meta" in raw_data:
            return 0, mode, True
        return len(raw_data.get("ai_findings", [])), mode, True

    def run(self):
        """Run orchestration across all resolved rules per component clone."""
        resolved_file = os.path.join(self.target_run_dir, "resolved-rules.json")
        if not os.path.exists(resolved_file):
            raise FileNotFoundError(
                f"resolved-rules.json not found in {self.target_run_dir}. Run Rule Resolver first."
            )

        resolved_payload = load_json(resolved_file)
        rules = resolved_payload.get("rules", [])

        print(f"\n=======================================================")
        print(f"STARTING SCANNER ORCHESTRATOR")
        print(f"Project: {self.project_id} | Run ID: {self.run_id}")
        print(f"Rules Loaded: {len(rules)} rules | Components: {len(self.components)}")
        print(f"Allow emulated: {self.allow_emulated} | Tools enabled: {self.tools_enabled}")
        print(f"=======================================================\n")

        os.makedirs(self.raw_outputs_dir, exist_ok=True)

        grouped_rules = {}
        for r in rules:
            eng = r.get("engine", "semgrep")
            grouped_rules.setdefault(eng, []).append(r)

        start_time = time.time()
        findings_summary = {}
        execution_modes = {}
        component_breakdown = {}
        skipped_engines = []

        engine_map = {
            "gitleaks": self.execute_gitleaks,
            "semgrep": self.execute_semgrep,
            "trivy": self.execute_trivy,
            "custom_ai": self.execute_custom_ai,
        }

        for eng, fn in engine_map.items():
            if eng not in grouped_rules:
                continue
            if not self._engine_enabled(eng):
                skipped_engines.append(eng)
                print(f"[*] Skipping {eng} — disabled in assessment.tools_enabled")
                continue

            total = 0
            comp_outputs = {}
            for component in self.components:
                cid = component.get("id")
                comp_rules = [r for r in grouped_rules[eng] if r.get("component_id") in (cid, None)]
                if not comp_rules:
                    comp_rules = grouped_rules[eng]
                scan_root = self._resolve_scan_root(component)
                if not scan_root:
                    continue
                comp_out_dir = os.path.join(self.raw_outputs_dir, cid)
                os.makedirs(comp_out_dir, exist_ok=True)
                count, mode, emulated = fn(comp_rules, scan_root, comp_out_dir, cid)
                total += count
                comp_outputs[cid] = {"count": count, "mode": mode, "emulated": emulated}
                self.emulated_flags[eng] = emulated
            findings_summary[eng] = total
            execution_modes[eng] = "Emulated Runner" if self.emulated_flags.get(eng) else "Native Binary"
            component_breakdown[eng] = comp_outputs

        elapsed_time = round(time.time() - start_time, 2)
        active_engines = list(findings_summary.keys())
        all_emulated = (
            all(self.emulated_flags.get(e, False) for e in active_engines)
            if active_engines
            else True
        )

        summary_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "executed_at": datetime.now().isoformat() + "Z",
            "duration_seconds": elapsed_time,
            "total_raw_findings": sum(findings_summary.values()),
            "findings_summary_by_engine": findings_summary,
            "execution_modes": execution_modes,
            "emulated_by_engine": {e: self.emulated_flags.get(e, True) for e in active_engines},
            "all_engines_emulated": all_emulated,
            "allow_emulated": self.allow_emulated,
            "tools_enabled": self.tools_enabled,
            "skipped_engines_disabled": skipped_engines,
            "component_breakdown": component_breakdown,
            "scan_roots": {
                c.get("id"): self._component_clone_path(c.get("id")).replace("\\", "/")
                for c in self.components
            },
            "raw_output_files": [
                f"raw_outputs/{cid}/{eng}_raw.json"
                for cid in [c.get("id") for c in self.components]
                for eng in active_engines
            ],
        }

        save_json(summary_payload, os.path.join(self.raw_outputs_dir, "execution_summary.json"))

        if all_emulated and active_engines and any(self.tools_enabled.values()):
            print(
                "\n[!] WARNING: All active scanner engines ran in EMULATED or empty mode while "
                "tools_enabled is true. Install native tools or pass --allow-emulated for dev/demo."
            )
        elif not self.allow_emulated and all_emulated and active_engines:
            print(
                "\n[!] NOTE: Raw outputs are empty (_meta placeholders). "
                "Install gitleaks/semgrep/trivy for real evidence, or use --allow-emulated."
            )

        print(f"\n=======================================================")
        print(f"ORCHESTRATION COMPLETE in {elapsed_time}s!")
        print(f"Raw Outputs Dir : {self.raw_outputs_dir}")
        print(f"Total Raw Findings: {sum(findings_summary.values())}")
        print(f"Engine Breakdown : {findings_summary}")
        print(f"=======================================================\n")


def main():
    parser = argparse.ArgumentParser(description="ASRP Scanner Orchestrator CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID")
    parser.add_argument("--run-id", default=None, help="Target run ID (defaults to latest)")
    parser.add_argument(
        "--allow-emulated",
        action="store_true",
        help="Emit synthetic raw outputs when native tools are unavailable (dev/demo only)",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    orchestrator = ScannerOrchestrator(
        workspace_root,
        project_id=args.project,
        run_id=args.run_id,
        allow_emulated=args.allow_emulated,
    )
    orchestrator.run()


if __name__ == "__main__":
    main()
