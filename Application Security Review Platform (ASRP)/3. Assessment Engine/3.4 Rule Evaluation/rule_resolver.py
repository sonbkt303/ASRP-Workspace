#!/usr/bin/env python3
"""
ASRP Rule Resolver Module (Layer 3.4)
======================================
Connects Layer 1 (Projects Registry) profile with Layer 2 (Rule Library) rules
and resolves the exact execution set of security rules for an Assessment Run.
"""

import os
import re
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


def normalize_framework(framework_str: str) -> set[str]:
    """Tokenize framework string like 'nestjs (v9.4.3) / express' -> {nestjs, express}."""
    if not framework_str:
        return set()
    tokens = re.split(r"[/,|]+", str(framework_str))
    normalized = set()
    for token in tokens:
        token = token.strip().lower()
        token = re.sub(r"\s*\([^)]*\)", "", token).strip()
        if token:
            normalized.add(token)
    return normalized


def load_rule_set_map(rule_lib_dir: str) -> dict[str, list[str]]:
    """Load rule set alias map from mappings/rule-set-map.yaml."""
    map_path = os.path.join(rule_lib_dir, "mappings", "rule-set-map.yaml")
    if not os.path.exists(map_path):
        return {}
    data = load_yaml(map_path).get("rule_set_map", {})
    return data.get("aliases", {}) or {}


def expand_rule_sets(rule_sets: set[str], alias_map: dict[str, list[str]]) -> set[str]:
    """Expand profile rule_set_ids via alias map (includes original ids)."""
    expanded = set(rule_sets)
    for rs in rule_sets:
        for alias in alias_map.get(rs, []):
            expanded.add(alias)
    return expanded


class RuleResolver:
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

        self.rule_lib_dir = os.path.join(
            self.asrp_dir, "2. Security Knowledge Base ⭐ (Core Asset)", "2.3 Rule Library"
        )
        self.clones_dir = os.path.join(
            self.asrp_dir, "3. Assessment Engine", "3.1 Source Acquisition", "clones"
        )
        self.run_id = run_id
        self.alias_map = load_rule_set_map(self.rule_lib_dir)

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
        context_data = load_yaml(os.path.join(self.project_dir, "context.yaml")).get("context", {})
        components_data = load_yaml(os.path.join(self.project_dir, "components.yaml")).get("components", [])

        # Global tech stack (union across components)
        languages = set()
        frameworks = set()
        component_profiles = {}

        if isinstance(tech_data, list):
            for comp in tech_data:
                if not isinstance(comp, dict):
                    continue
                cid = comp.get("component_id")
                comp_langs = set()
                comp_fws = set()
                if comp.get("language"):
                    lang = str(comp.get("language")).lower()
                    languages.add(lang)
                    comp_langs.add(lang)
                comp_fws = normalize_framework(comp.get("framework", ""))
                frameworks.update(comp_fws)
                comp_rule_sets = set(comp.get("rule_set_ids") or [])
                component_profiles[cid] = {
                    "languages": comp_langs,
                    "frameworks": comp_fws,
                    "rule_set_ids": comp_rule_sets,
                }

        # Extract assessment lens
        rule_sets = set(assessment_data.get("rule_sets", assessment_data.get("rule_set_ids", [])))
        tools_enabled = assessment_data.get("tools_enabled", {})

        expanded_rule_sets = expand_rule_sets(rule_sets, self.alias_map)
        print(
            f"[OK] Profile Loaded: Languages={list(languages)}, Frameworks={list(frameworks)}, "
            f"RuleSets={list(rule_sets)} (expanded: {len(expanded_rule_sets)})"
        )
        return {
            "languages": languages,
            "frameworks": frameworks,
            "rule_sets": rule_sets,
            "expanded_rule_sets": expanded_rule_sets,
            "tools_enabled": tools_enabled,
            "scope": scope_data,
            "context": context_data,
            "assessment": assessment_data,
            "components": components_data,
            "component_profiles": component_profiles,
        }

    def _rule_set_match(self, entry_rule_sets: list, expanded_sets: set[str]) -> bool:
        """True if rule index entry intersects expanded project rule sets."""
        if not entry_rule_sets:
            return True
        entry = set(entry_rule_sets)
        return bool(entry.intersection(expanded_sets))

    def _tech_match(self, rule_data: dict, profile: dict, comp_profile: dict | None) -> bool:
        """Match rule against global or per-component tech profile."""
        app_tech = rule_data.get("applicable_technologies", {})
        rule_langs = set(str(l).lower() for l in app_tech.get("languages", []))
        rule_fws = set(str(f).lower() for f in app_tech.get("frameworks", []))

        langs = comp_profile["languages"] if comp_profile else profile["languages"]
        fws = comp_profile["frameworks"] if comp_profile else profile["frameworks"]

        lang_match = "all" in rule_langs or bool(rule_langs.intersection(langs))
        fw_match = "all" in rule_fws or bool(rule_fws.intersection(fws))
        return lang_match and fw_match

    def resolve_rules(self, profile):
        """Step 3 & 4: Ingest Rule Library index & match rules against project profile."""
        index_path = os.path.join(self.rule_lib_dir, "index.yaml")
        catalog = load_yaml(index_path).get("rule_library", {})
        all_rules = catalog.get("rules", [])

        resolved_rules = []
        engines_summary = {}
        seen_rule_ids = set()

        # Per-component resolution for component-specific rule sets
        component_ids = [c.get("id") for c in profile["components"] if c.get("id")]
        if not component_ids:
            component_ids = [None]

        for comp_id in component_ids:
            comp_profile = profile["component_profiles"].get(comp_id) if comp_id else None
            comp_expanded = profile["expanded_rule_sets"]
            if comp_profile:
                comp_expanded = expand_rule_sets(
                    profile["rule_sets"].union(comp_profile["rule_set_ids"]),
                    self.alias_map,
                )

            for entry in all_rules:
                if not entry.get("enabled", True):
                    continue

                rule_id = entry.get("id")
                dedupe_key = (rule_id, comp_id)
                if dedupe_key in seen_rule_ids:
                    continue

                # Rule set filter from index entry
                entry_sets = entry.get("rule_set_ids") or []
                if not self._rule_set_match(entry_sets, comp_expanded):
                    continue

                rule_rel_path = entry.get("path")
                rule_full_path = os.path.join(self.rule_lib_dir, rule_rel_path)

                if not os.path.exists(rule_full_path):
                    print(f"[!] Warning: Rule file missing: {rule_full_path}")
                    continue

                rule_data = load_yaml(rule_full_path).get("rule", {})
                engine = rule_data.get("engine")

                tool_key_map = {
                    "semgrep": "sast",
                    "gitleaks": "secrets",
                    "trivy": "sca",
                    "checkov": "iac",
                    "cicd": "sast",
                    "custom_ai": "sast",
                }
                tool_type = tool_key_map.get(engine, "sast")
                if not profile["tools_enabled"].get(tool_type, True):
                    continue

                if not self._tech_match(rule_data, profile, comp_profile):
                    continue

                resolved_rule_entry = {
                    "id": rule_data.get("id"),
                    "name": rule_data.get("name"),
                    "description": rule_data.get("description"),
                    "severity": rule_data.get("severity"),
                    "engine": engine,
                    "category": rule_data.get("category"),
                    "standard_mapping": rule_data.get("standard_mapping"),
                    "engine_config": rule_data.get("engine_config"),
                    "remediation": rule_data.get("remediation"),
                    "rule_set_ids": entry_sets,
                }
                if comp_id:
                    resolved_rule_entry["component_id"] = comp_id

                resolved_rules.append(resolved_rule_entry)
                seen_rule_ids.add(dedupe_key)
                engines_summary[engine] = engines_summary.get(engine, 0) + 1

        print(f"[OK] Resolution Complete: {len(resolved_rules)} rules resolved across {len(engines_summary)} engines.")
        return resolved_rules, engines_summary

    def build_scan_scope(self, profile):
        """Build scan_scope block from scope.yaml and components."""
        scope = profile["scope"]
        components = []
        for comp in profile["components"]:
            cid = comp.get("id")
            clone_path = os.path.join(self.clones_dir, self.project_id, cid)
            components.append({
                "id": cid,
                "scan_paths": comp.get("scan_paths") or [],
                "exclude_paths": comp.get("exclude_paths") or [],
                "clone_path": clone_path.replace("\\", "/"),
            })
        return {
            "include": scope.get("include") or [],
            "exclude": scope.get("exclude") or [],
            "review_level": scope.get("review_level"),
            "component_ids": scope.get("component_ids") or [c["id"] for c in components],
            "components": components,
        }

    def _build_technologies_block(self, profile):
        """Per-component tech stack from technologies.yaml for AI pre-flight."""
        tech_path = os.path.join(self.project_dir, "technologies.yaml")
        if not os.path.exists(tech_path):
            return []
        tech_data = load_yaml(tech_path).get("technologies", [])
        block = []
        for comp in tech_data if isinstance(tech_data, list) else []:
            if not isinstance(comp, dict):
                continue
            block.append({
                "component_id": comp.get("component_id"),
                "language": comp.get("language"),
                "framework": comp.get("framework"),
                "rule_set_ids": comp.get("rule_set_ids") or [],
            })
        return block

    @staticmethod
    def _rules_by_component(resolved_rules):
        """Group resolved rule IDs by component for AI stage 2.3 pre-flight."""
        by_comp: dict[str, list[str]] = {}
        for rule in resolved_rules:
            cid = rule.get("component_id") or "_global"
            by_comp.setdefault(cid, []).append(rule.get("id"))
        return by_comp

    def build_scan_context(self, profile, manifest, resolved_rules, run_dir):
        """Build scan_context.json for AI pre-flight."""
        context = profile["context"]
        assessment = profile["assessment"]
        security = context.get("security", {})
        return {
            "project_id": self.project_id,
            "run_id": self.run_id,
            "manifest_hash": manifest.get("profile_hash"),
            "generated_at": datetime.now().isoformat() + "Z",
            "components": self.build_scan_scope(profile)["components"],
            "technologies": self._build_technologies_block(profile),
            "context": {
                "risk_tier": context.get("risk_tier"),
                "business": context.get("business") or {},
                "compliance": context.get("compliance") or [],
                "data_classification": security.get("data_classification"),
                "contains_pii": security.get("contains_pii"),
                "internet_facing": security.get("internet_facing"),
            },
            "assessment": {
                "standards": assessment.get("standards") or [],
                "security_domains": assessment.get("security_domains") or [],
                "rule_set_ids": assessment.get("rule_set_ids") or [],
                "severity_threshold": assessment.get("severity_threshold"),
                "tools_enabled": assessment.get("tools_enabled") or {},
                "ai": assessment.get("ai") or {},
            },
            "scan_scope": self.build_scan_scope(profile),
            "resolved_rule_count": len(resolved_rules),
            "resolved_rules_by_component": self._rules_by_component(resolved_rules),
            "resolved_rules_path": os.path.join(run_dir, "resolved-rules.json").replace("\\", "/"),
        }

    def run(self):
        """Execute full resolution and output resolved-rules.json + scan_context.json."""
        manifest = self.validate_human_gate()
        profile = self.load_project_profiles()
        resolved_rules, engines_summary = self.resolve_rules(profile)

        if not self.run_id:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.run_id = f"run-{timestamp}"

        run_dir = os.path.join(self.project_dir, "runs", self.run_id)
        os.makedirs(run_dir, exist_ok=True)

        scan_scope = self.build_scan_scope(profile)

        output_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "resolved_at": datetime.now().isoformat() + "Z",
            "manifest_hash": manifest.get("profile_hash"),
            "rules_count": len(resolved_rules),
            "engines_summary": engines_summary,
            "scan_scope": scan_scope,
            "rules": resolved_rules,
        }

        output_path = os.path.join(run_dir, "resolved-rules.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_payload, f, indent=2, ensure_ascii=False)

        scan_context = self.build_scan_context(profile, manifest, resolved_rules, run_dir)
        context_path = os.path.join(run_dir, "scan_context.json")
        with open(context_path, 'w', encoding='utf-8') as f:
            json.dump(scan_context, f, indent=2, ensure_ascii=False)

        print(f"\n=======================================================")
        print(f"SUCCESS: resolved-rules.json generated successfully!")
        print(f"Location: {output_path}")
        print(f"Scan context: {context_path}")
        print(f"Summary : {len(resolved_rules)} rules | Engines: {engines_summary}")
        print(f"=======================================================\n")
        return output_path


def main():
    parser = argparse.ArgumentParser(description="ASRP Rule Resolver CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID in Projects Registry")
    parser.add_argument("--run-id", default=None, help="Target run ID (optional)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    resolver = RuleResolver(workspace_root, project_id=args.project, run_id=args.run_id)
    resolver.run()


if __name__ == "__main__":
    main()
