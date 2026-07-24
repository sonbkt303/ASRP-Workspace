#!/usr/bin/env python3
"""
ASRP Rule Resolver Module (Layer 3.4)
======================================
Connects Layer 1 (Projects Registry) profile with Layer 2 (Rule Library) rules
and resolves the exact execution set of security rules for an Assessment Run.
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


def load_yaml(filepath):
    """Utility to safely load a YAML file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class RuleResolver:
    def __init__(self, workspace_root, project_id="cleverdent"):
        self.workspace_root = workspace_root
        self.project_id = project_id
        
        # Paths setup
        self.asrp_dir = os.path.join(self.workspace_root, "Application Security Review Platform (ASRP)")
        self.project_dir = os.path.join(self.asrp_dir, "1. Projects Registry", self.project_id)
        self.rule_lib_dir = os.path.join(
            self.asrp_dir, "2. Security Knowledge Base ⭐ (Core Asset)", "2.3 Rule Library"
        )
        
    def validate_human_gate(self):
        """Step 1: Check if project lifecycle_status is validated in manifest."""
        manifest_path = os.path.join(self.project_dir, "registry.manifest.yaml")
        if not os.path.exists(manifest_path):
            raise ValueError(f"CRITICAL: registry.manifest.yaml not found for project '{self.project_id}'.")
            
        manifest = load_yaml(manifest_path).get("registry_manifest", {})
        status = manifest.get("lifecycle_status")
        
        if status != "validated":
            raise ValueError(
                f"ABORT: Assessment Engine cannot run scan when lifecycle_status is '{status}'. Must be 'validated'."
            )
            
        print(f"[OK] Human Gate Validated: Project '{self.project_id}' is READY TO SCAN (Status: validated).")
        return manifest

    def load_project_profiles(self):
        """Step 2: Read Layer 1 profile YAML files."""
        tech_data = load_yaml(os.path.join(self.project_dir, "technologies.yaml")).get("technologies", [])
        assessment_data = load_yaml(os.path.join(self.project_dir, "assessment.yaml")).get("assessment", {})
        scope_data = load_yaml(os.path.join(self.project_dir, "scope.yaml")).get("scope", {})
        
        # Extract tech stack
        languages = set()
        frameworks = set()
        for comp in tech_data:
            languages.add(comp.get("language", "").lower())
            for fw in comp.get("frameworks", []):
                frameworks.add(fw.lower())
                
        # Extract assessment lens
        rule_sets = set(assessment_data.get("rule_set_ids", []))
        tools_enabled = assessment_data.get("tools_enabled", {})
        
        print(f"[OK] Profile Loaded: Languages={list(languages)}, Frameworks={list(frameworks)}, RuleSets={list(rule_sets)}")
        return {
            "languages": languages,
            "frameworks": frameworks,
            "rule_sets": rule_sets,
            "tools_enabled": tools_enabled,
            "scope": scope_data
        }

    def resolve_rules(self, profile):
        """Step 3 & 4: Ingest Rule Library index & match rules against project profile."""
        index_path = os.path.join(self.rule_lib_dir, "index.yaml")
        catalog = load_yaml(index_path).get("rule_library", {})
        all_rules = catalog.get("rules", [])
        
        resolved_rules = []
        engines_summary = {}
        
        for entry in all_rules:
            if not entry.get("enabled", True):
                continue
                
            rule_rel_path = entry.get("path")
            rule_full_path = os.path.join(self.rule_lib_dir, rule_rel_path)
            
            if not os.path.exists(rule_full_path):
                print(f"[!] Warning: Rule file missing: {rule_full_path}")
                continue
                
            rule_data = load_yaml(rule_full_path).get("rule", {})
            engine = rule_data.get("engine")
            
            # Check tool enabled status from assessment.yaml
            tool_key_map = {
                "semgrep": "sast",
                "gitleaks": "secrets",
                "trivy": "sca",
                "checkov": "iac",
                "cicd": "sast",
                "custom_ai": "sast"
            }
            tool_type = tool_key_map.get(engine, "sast")
            if not profile["tools_enabled"].get(tool_type, True):
                continue
                
            # Tech matching (Multi-Language Pattern check)
            app_tech = rule_data.get("applicable_technologies", {})
            rule_langs = set(l.lower() for l in app_tech.get("languages", []))
            rule_fws = set(f.lower() for f in app_tech.get("frameworks", []))
            
            lang_match = "all" in rule_langs or bool(rule_langs.intersection(profile["languages"]))
            fw_match = "all" in rule_fws or bool(rule_fws.intersection(profile["frameworks"]))
            
            if lang_match and fw_match:
                resolved_rule_entry = {
                    "id": rule_data.get("id"),
                    "name": rule_data.get("name"),
                    "severity": rule_data.get("severity"),
                    "engine": engine,
                    "category": rule_data.get("category"),
                    "standard_mapping": rule_data.get("standard_mapping"),
                    "engine_config": rule_data.get("engine_config"),
                    "remediation": rule_data.get("remediation")
                }
                resolved_rules.append(resolved_rule_entry)
                engines_summary[engine] = engines_summary.get(engine, 0) + 1
                
        print(f"[OK] Resolution Complete: {len(resolved_rules)} rules resolved across {len(engines_summary)} engines.")
        return resolved_rules, engines_summary

    def run(self):
        """Execute full resolution and output resolved-rules.json."""
        manifest = self.validate_human_gate()
        profile = self.load_project_profiles()
        resolved_rules, engines_summary = self.resolve_rules(profile)
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"run-{timestamp}"
        run_dir = os.path.join(self.project_dir, "runs", run_id)
        os.makedirs(run_dir, exist_ok=True)
        
        output_payload = {
            "run_id": run_id,
            "project_id": self.project_id,
            "resolved_at": datetime.now().isoformat() + "Z",
            "manifest_hash": manifest.get("profile_hash"),
            "rules_count": len(resolved_rules),
            "engines_summary": engines_summary,
            "rules": resolved_rules
        }
        
        output_path = os.path.join(run_dir, "resolved-rules.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_payload, f, indent=2, ensure_ascii=False)
            
        print(f"\n=======================================================")
        print(f"🎉 SUCCESS: resolved-rules.json generated successfully!")
        print(f"📍 Location: {output_path}")
        print(f"📊 Summary : {len(resolved_rules)} rules | Engines: {engines_summary}")
        print(f"=======================================================\n")
        return output_path


def main():
    parser = argparse.ArgumentParser(description="ASRP Rule Resolver CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID in Projects Registry")
    args = parser.parse_args()
    
    # Determine workspace root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    
    resolver = RuleResolver(workspace_root, project_id=args.project)
    resolver.run()


if __name__ == "__main__":
    main()
