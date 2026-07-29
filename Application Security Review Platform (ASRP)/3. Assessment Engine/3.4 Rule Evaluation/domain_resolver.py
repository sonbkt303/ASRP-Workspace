#!/usr/bin/env python3
"""
ASRP Programmatic Domain Resolver Engine (domain_resolver.py)
==============================================================
Core Assessment Engine module that programmatically accesses Module 2.2
Security Domains, resolves domain metadata, and categorizes findings.
"""

import os
import sys
import yaml
import json

# Force UTF-8 encoding for Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


class DomainResolver:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.asrp_root = os.path.join(workspace_root, "Application Security Review Platform (ASRP)")
        self.domains_dir = os.path.join(self.asrp_root, "2. Security Knowledge Base ⭐ (Core Asset)", "2.2 Security Domains")
        self.master_index_path = os.path.join(self.domains_dir, "index.yaml")
        self._domain_cache = None

    def list_domains(self) -> list:
        """List all 13 registered security domains."""
        if not os.path.exists(self.master_index_path):
            return []

        with open(self.master_index_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data.get("domains", [])

    def get_domain(self, domain_code: str) -> dict:
        """Get full domain specification metadata by domain code."""
        domains = self.list_domains()
        for d in domains:
            if d.get("code") == domain_code:
                spec_rel_path = d.get("spec_file")
                spec_full_path = os.path.join(self.domains_dir, spec_rel_path)
                if os.path.exists(spec_full_path):
                    with open(spec_full_path, "r", encoding="utf-8") as f:
                        return yaml.safe_load(f) or {}
        return {}

    def categorize_finding(self, finding: dict) -> dict:
        """Categorize finding by resolving its CWE to a Security Domain."""
        standard_map = finding.get("standard_mapping", {})
        cwes = standard_map.get("cwe", [])

        if cwes:
            cwe = cwes[0]
            # Match CWE to domain
            domains = self.list_domains()
            for d in domains:
                spec = self.get_domain(d.get("code"))
                if cwe in spec.get("core_vulnerabilities", []):
                    finding["security_domain"] = spec.get("name")
                    finding["domain_code"] = spec.get("domain_code")
                    break

        return finding


if __name__ == "__main__":
    workspace = os.path.dirname(os.path.abspath(__file__))
    for _ in range(3):
        workspace = os.path.dirname(workspace)

    resolver = DomainResolver(workspace)
    sample = resolver.get_domain("authorization")
    domains_list = resolver.list_domains()

    print("=" * 55)
    print("🔎 TEST PROGRAMMATIC DOMAIN RESOLVER ENGINE")
    print(f"📌 Total Domains Registered: {len(domains_list)}")
    print("=" * 55)
    print(json.dumps(sample, indent=2, ensure_ascii=False))
