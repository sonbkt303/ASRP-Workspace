#!/usr/bin/env python3
"""
ASRP Programmatic Standard Resolver Engine (standard_resolver.py)
==================================================================
Core Assessment Engine module that programmatically accesses Module 2.1
Security Standards, resolves CWE Primary Keys to international standards,
and filters standards based on project tech stack.
"""

import os
import sys
import yaml
import json

# Force UTF-8 encoding for Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


class StandardResolver:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.asrp_root = os.path.join(workspace_root, "Application Security Review Platform (ASRP)")
        self.standards_dir = os.path.join(self.asrp_root, "2. Security Knowledge Base ⭐ (Core Asset)", "2.1 Security Standards")
        self.matrix_path = os.path.join(self.standards_dir, "unified-standards-matrix.yaml")
        self.master_index_path = os.path.join(self.standards_dir, "index.yaml")
        self._matrix_cache = None

    def _load_matrix(self):
        if self._matrix_cache is not None:
            return self._matrix_cache

        if os.path.exists(self.matrix_path):
            with open(self.matrix_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                self._matrix_cache = {item["cwe_id"]: item for item in data.get("mappings", [])}
        else:
            self._matrix_cache = {}
        return self._matrix_cache

    def resolve_cwe(self, cwe_id: str) -> dict:
        """Resolve a single CWE ID to its complete cross-standard matrix."""
        matrix = self._load_matrix()
        return matrix.get(cwe_id.upper(), {
            "cwe_id": cwe_id,
            "cwe_name": "Unknown Weakness",
            "asvs_v4": [],
            "owasp_top10_2021": [],
            "owasp_api_top10_2023": [],
            "nist_ssdf": [],
            "capec": []
        })

    def get_profile_standards(self, tech_stack: list) -> list:
        """Extract targeted standard IDs based on project technology stack."""
        tech_set = {t.lower() for t in tech_stack}
        selected_standards = ["ASVS-V4.0.3", "OWASP-TOP10-2021", "CWE-TOP25-2023"]

        if any(t in tech_set for t in ["nestjs", "express", "fastapi", "graphql", "rest", "api"]):
            selected_standards.append("OWASP-API-TOP10-2023")

        if any(t in tech_set for t in ["docker", "kubernetes", "k8s", "terraform"]):
            selected_standards.append("CIS-CONTAINERS-V1.6")

        if any(t in tech_set for t in ["healthcare", "patient", "medical"]):
            selected_standards.append("HIPAA-TECHNICAL-SAFEGUARDS")

        if any(t in tech_set for t in ["payment", "card", "billing"]):
            selected_standards.append("PCI-DSS-V4.0")

        return selected_standards

    def enrich_finding(self, finding: dict) -> dict:
        """Enrich a finding dictionary with resolved international standards."""
        standard_map = finding.get("standard_mapping", {})
        cwes = standard_map.get("cwe", [])

        if cwes:
            primary_cwe = cwes[0]
            resolved = self.resolve_cwe(primary_cwe)
            if resolved:
                if not standard_map.get("asvs_v4") and resolved.get("asvs_v4"):
                    standard_map["asvs_v4"] = resolved["asvs_v4"]
                if not standard_map.get("owasp_top10_2021") and resolved.get("owasp_top10_2021"):
                    standard_map["owasp_top10_2021"] = resolved["owasp_top10_2021"]
                if resolved.get("capec"):
                    finding["capec_attack_pattern"] = resolved["capec"][0]

        finding["standard_mapping"] = standard_map
        return finding


if __name__ == "__main__":
    workspace = os.path.dirname(os.path.abspath(__file__))
    for _ in range(3):
        workspace = os.path.dirname(workspace)

    resolver = StandardResolver(workspace)
    sample = resolver.resolve_cwe("CWE-639")
    print("=" * 55)
    print("🔎 TEST PROGRAMMATIC STANDARD RESOLVER ENGINE")
    print("=" * 55)
    print(json.dumps(sample, indent=2, ensure_ascii=False))
