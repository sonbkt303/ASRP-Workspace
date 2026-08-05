#!/usr/bin/env python3
"""
ASRP Report Generator Module (Layer 5)
======================================
Generates standalone Executive HTML Dashboards and GitHub-Flavored Markdown
Security Review Reports based on Layer 1 Profile, Layer 3 Findings, Layer 2 Stage Outputs, and Risk Assessment.
Features interactive Stage Module filtering (2.1 to 2.10) for deep issue exploration.
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


class ReportGenerator:
    def __init__(self, workspace_root, project_id="cleverdent", run_id=None):
        self.workspace_root = workspace_root
        self.project_id = project_id
        
        # Paths setup
        if self.workspace_root.endswith("Application Security Review Platform (ASRP)"):
            self.asrp_dir = self.workspace_root
        else:
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
        self.stage_outputs_dir = os.path.join(self.target_run_dir, "stage_outputs")
        
        # Template Reference Path (Layer 1.1 Template / reports)
        self.template_reports_dir = os.path.join(registry_dir, "1.1 Template", "reports")
        self.exec_template_file = os.path.join(self.template_reports_dir, "executive_dashboard.html")
        self.comp_template_file = os.path.join(self.template_reports_dir, "component_report.html")

    def _find_latest_run_id(self):
        """Find the most recent run directory in project/runs/."""
        if not os.path.exists(self.runs_dir):
            raise FileNotFoundError(f"No runs directory found for project '{self.project_id}'.")
        
        run_folders = [f for f in os.listdir(self.runs_dir) if f.startswith("run-")]
        if not run_folders:
            raise FileNotFoundError(f"No run folders found under {self.runs_dir}.")
        
        run_folders.sort(reverse=True)
        return run_folders[0]

    def _load_stage_outputs(self):
        """Load all Stage JSON files from stage_outputs/ directory."""
        stages = {}
        if not os.path.exists(self.stage_outputs_dir):
            return stages
        
        stage_files = {
            "2.1": "stage_2_1_standards.json",
            "2.2": "stage_2_2_domains.json",
            "2.3": "stage_2_3_rules.json",
            "2.4": "stage_2_4_checklists.json",
            "2.6": "stage_2_6_threats.json",
            "2.7": "stage_2_7_guidelines.json",
            "2.10": "stage_2_10_remediations.json"
        }
        for key, fname in stage_files.items():
            fpath = os.path.join(self.stage_outputs_dir, fname)
            stages[key] = load_json(fpath)
        return stages

    def _count_stage_issues(self, stage_id, stages_data, component_id=None):
        """Count non-PASS items in a stage output JSON file for a specific component (or all components)."""
        stage_file_data = stages_data.get(stage_id) or {}
        results = stage_file_data.get("results", []) if isinstance(stage_file_data, dict) else []
        count = 0
        for r in results:
            status = str(r.get("status", "")).upper()
            cid = r.get("component_id")
            if status in ["FAIL", "WARNING", "TRIGGERED", "CONFIRMED", "REQUIRES_FIX"]:
                if component_id is None or cid == component_id or not cid:
                    count += 1
        return count

    def _get_finding_stages(self, finding, stages_data=None):
        """Dynamically determine which Layer 2 Stage Modules a finding genuinely maps to based on strict specific criteria."""
        stages = []
        
        std = finding.get("standard_mapping", {})
        dom = finding.get("security_domain", "")
        rule_id = finding.get("rule_id", "") or ""
        chk_ref = finding.get("review_checklist_ref", "") or ""
        threat_ref = finding.get("threat_model_ref", "") or ""
        guideline_ref = finding.get("guideline_ref", "") or ""
        rem_ref = finding.get("remediation_ref", "") or ""
        
        # 2.1 Security Standards: Explicit standard mapping or STD- checklist ref
        if std.get("cwe") or std.get("owasp_top10_2021") or std.get("asvs_v4") or (chk_ref and chk_ref.startswith("STD-")):
            stages.append("2.1")
            
        # 2.2 Security Domains: Explicit DOM- checklist ref or 2.2.x security domain classification
        if (chk_ref and chk_ref.startswith("DOM-")) or (dom and ("2.2" in dom or dom != "")):
            stages.append("2.2")
            
        # 2.3 Rule Library: Triggered by an executable rule ID
        if rule_id and (rule_id.startswith("ASRP-") or rule_id.startswith("RULE-")):
            stages.append("2.3")
            
        # 2.4 Review Checklists: Associated with an auditor checklist item (CHK-*)
        if chk_ref and chk_ref.startswith("CHK-"):
            stages.append("2.4")
            
        # 2.6 Threat Models: ONLY IF explicitly linked to a STRIDE threat model scenario (threat_model_ref or THREAT-*)
        if threat_ref and (threat_ref.startswith("THREAT-") or threat_ref.startswith("ASRP-TM-")):
            stages.append("2.6")
            
        # 2.7 Secure Coding Guidelines: ONLY IF explicitly linked to a Secure Coding Guideline (guideline_ref or SCG-*)
        if guideline_ref or rule_id.startswith("SCG-") or (chk_ref and chk_ref.startswith("SCG-")):
            stages.append("2.7")

        # 2.10 Remediation Guides: ONLY IF explicitly linked to an Actionable Remediation Patch (remediation_ref or REM-*)
        if rem_ref and (rem_ref.startswith("REM-") or rem_ref.startswith("ASRP-REM-")):
            stages.append("2.10")
            
        return ",".join(stages) if stages else "2.1"

    def _render_stage_output_cards(self, stages_data, component_id=None):
        """Render HTML cards for all non-PASS items across Layer 2 Stage Output JSON files."""
        cards = []

        # 2.1 Standards
        s21 = (stages_data.get("2.1") or {}).get("results", [])
        for item in s21:
            if item.get("status") in ["PASS", "COMPLIANT", "NOT_APPLICABLE"]: continue
            cid = item.get("component_id", "all")
            if component_id and cid != component_id: continue
            
            item_id = item.get("item_id", "STD-000")
            clean_id = str(item_id).replace('.', '_').replace('/', '_').replace(':', '_').replace('-', '_')
            title = item.get("control", item.get("item_id"))
            sev = item.get("severity", "HIGH").upper()
            sev_class = sev.lower()
            ev = item.get("evidence", {})
            if isinstance(ev, dict):
                fpath = ev.get("file_path", "N/A")
                line = ev.get("line", 1)
                desc = ev.get("description", "")
                snippet = ev.get("snippet", "")
            else:
                fpath, line, desc, snippet = "N/A", 1, str(ev or ""), ""
            rem = item.get("remediation", "")
            
            snippet_html = f'<div class="code-block">{snippet}</div>' if snippet else ''
            
            card = f'''
      <div class="finding-card" id="card-{clean_id}" data-stages="2.1" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{clean_id}\')">
          <span class="finding-sev sev-{sev_class}">{sev}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.1 Security Standards</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fb-grid">
            <div class="fb-field"><label>Standard / Control</label><p>{item.get("standard", "OWASP ASVS")}</p></div>
            <div class="fb-field"><label>File Location</label><p class="path">{fpath}:{line}</p></div>
          </div>
          {snippet_html}
          <p style="font-size:13px;color:var(--text-secondary);margin:8px 0;">{desc}</p>
          <div class="fix-box">
            <label>✅ Standard Remediation Guidance</label>
            <p>{rem}</p>
          </div>
        </div>
      </div>'''
            cards.append(card)

        # 2.2 Domains
        s22 = (stages_data.get("2.2") or {}).get("results", [])
        for item in s22:
            if item.get("status") in ["PASS", "COMPLIANT", "NOT_APPLICABLE"]: continue
            cid = item.get("component_id", "all")
            if component_id and cid != component_id: continue
            
            item_id = item.get("item_id", "DOM-000")
            clean_id = str(item_id).replace('.', '_').replace('/', '_').replace(':', '_').replace('-', '_')
            title = item.get("domain", item_id)
            sev = item.get("severity", "MEDIUM").upper()
            sev_class = sev.lower()
            ev = item.get("evidence", {})
            if isinstance(ev, dict):
                fpath = ev.get("file_path", "N/A")
                desc = ev.get("description", "")
            else:
                fpath, desc = "N/A", str(ev or "")
            rem = item.get("remediation", "")
            
            card = f'''
      <div class="finding-card" id="card-{clean_id}" data-stages="2.2" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{clean_id}\')">
          <span class="finding-sev sev-{sev_class}">{sev}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.2 Security Domains</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fb-grid">
            <div class="fb-field"><label>Security Domain</label><p>{title}</p></div>
            <div class="fb-field"><label>Target Scope</label><p class="path">{fpath}</p></div>
          </div>
          <p style="font-size:13px;color:var(--text-secondary);margin:8px 0;">{desc}</p>
          <div class="fix-box">
            <label>✅ Domain Security Remediation</label>
            <p>{rem}</p>
          </div>
        </div>
      </div>'''
            cards.append(card)

        # 2.3 Rule Library
        s23 = (stages_data.get("2.3") or {}).get("results", [])
        for item in s23:
            if item.get("status") in ["PASS", "COMPLIANT", "NOT_TRIGGERED"]: continue
            cid = item.get("component_id", "all")
            if component_id and cid != component_id: continue
            
            item_id = item.get("rule_id", item.get("item_id", "RULE-000"))
            clean_id = str(item_id).replace('.', '_').replace('/', '_').replace(':', '_').replace('-', '_')
            title = item.get("rule_name", item_id)
            sev = item.get("severity", "HIGH").upper()
            sev_class = sev.lower()
            ev = item.get("evidence", {})
            if isinstance(ev, dict):
                fpath = ev.get("file_path", "N/A")
                line = ev.get("line", 1)
                snippet = ev.get("snippet", "")
            else:
                fpath, line, snippet = "N/A", 1, ""
            rem = item.get("remediation", "")
            
            snippet_html = f'<div class="code-block">{snippet}</div>' if snippet else ''
            
            card = f'''
      <div class="finding-card" id="card-{clean_id}" data-stages="2.3" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{clean_id}\')">
          <span class="finding-sev sev-{sev_class}">{sev}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.3 Rule Library</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fb-grid">
            <div class="fb-field"><label>Rule Pattern ID</label><p>{item_id}</p></div>
            <div class="fb-field"><label>File Location</label><p class="path">{fpath}:{line}</p></div>
          </div>
          {snippet_html}
          <div class="fix-box" style="margin-top:8px;">
            <label>✅ Rule Remediation Guidance</label>
            <p>{rem}</p>
          </div>
        </div>
      </div>'''
            cards.append(card)

        # 2.4 Checklists
        s24 = (stages_data.get("2.4") or {}).get("results", [])
        for item in s24:
            if item.get("status") in ["PASS", "COMPLIANT", "NOT_APPLICABLE"]: continue
            cid = item.get("component_id", "all")
            if component_id and cid != component_id: continue
            
            item_id = item.get("item_id", "CHK-000")
            clean_id = str(item_id).replace('.', '_').replace('/', '_').replace(':', '_').replace('-', '_')
            title = item.get("verification_requirement", item_id)
            sev = item.get("severity", "MEDIUM").upper()
            sev_class = sev.lower()
            ev = item.get("evidence", {})
            if isinstance(ev, dict):
                fpath = ev.get("file_path", "N/A")
                desc = ev.get("description", "")
            else:
                fpath, desc = "N/A", str(ev or "")
            rem = item.get("remediation", "")
            
            card = f'''
      <div class="finding-card" id="card-{clean_id}" data-stages="2.4" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{clean_id}\')">
          <span class="finding-sev sev-{sev_class}">{sev}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.4 Review Checklists</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fb-grid">
            <div class="fb-field"><label>Auditor Requirement</label><p>{title}</p></div>
            <div class="fb-field"><label>Target Scope</label><p class="path">{fpath}</p></div>
          </div>
          <p style="font-size:13px;color:var(--text-secondary);margin:8px 0;">{desc}</p>
          <div class="fix-box">
            <label>✅ Verification Remediation</label>
            <p>{rem}</p>
          </div>
        </div>
      </div>'''
            cards.append(card)

        # 2.6 Threat Models
        s26 = (stages_data.get("2.6") or {}).get("results", [])
        for item in s26:
            if item.get("status") in ["PASS", "COMPLIANT", "MITIGATED"]: continue
            cid = item.get("component_id", "all")
            if component_id and cid != component_id: continue
            
            item_id = item.get("item_id", "THREAT-000")
            clean_id = str(item_id).replace('.', '_').replace('/', '_').replace(':', '_').replace('-', '_')
            title = item.get("threat_title", item_id)
            cat = item.get("stride_category", "STRIDE Threat")
            sev = item.get("severity", "HIGH").upper()
            sev_class = sev.lower()
            ev = item.get("evidence", {})
            if isinstance(ev, dict):
                fpath = ev.get("file_path", "N/A")
                desc = ev.get("description", "")
            else:
                fpath, desc = "N/A", str(ev or "")
            rem = item.get("remediation", "")
            
            card = f'''
      <div class="finding-card" id="card-{clean_id}" data-stages="2.6" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{clean_id}\')">
          <span class="finding-sev sev-{sev_class}">{sev}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.6 Threat Models ({cat})</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fb-grid">
            <div class="fb-field"><label>STRIDE Category</label><p>{cat}</p></div>
            <div class="fb-field"><label>Target File</label><p class="path">{fpath}</p></div>
          </div>
          <p style="font-size:13px;color:var(--text-secondary);margin:8px 0;">{desc}</p>
          <div class="fix-box">
            <label>✅ Architectural Threat Mitigation</label>
            <p>{rem}</p>
          </div>
        </div>
      </div>'''
            cards.append(card)

        # 2.7 Secure Coding Guidelines
        s27 = (stages_data.get("2.7") or {}).get("results", [])
        for item in s27:
            if item.get("status") in ["PASS", "COMPLIANT", "NOT_APPLICABLE"]: continue
            cid = item.get("component_id", "all")
            if component_id and cid != component_id: continue
            
            item_id = item.get("item_id", "SCG-000")
            clean_id = str(item_id).replace('.', '_').replace('/', '_').replace(':', '_').replace('-', '_')
            title = item.get("guideline_title", item_id)
            sev = item.get("severity", "HIGH").upper()
            sev_class = sev.lower()
            ev = item.get("evidence", {})
            if isinstance(ev, dict):
                fpath = ev.get("file_path", "N/A")
                line = ev.get("line", 1)
                snippet = ev.get("snippet", "")
            else:
                fpath, line, snippet = "N/A", 1, ""
            rem = item.get("remediation", "")
            
            snippet_html = f'<div class="code-block">{snippet}</div>' if snippet else ''
            
            card = f'''
      <div class="finding-card" id="card-{clean_id}" data-stages="2.7" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{clean_id}\')">
          <span class="finding-sev sev-{sev_class}">{sev}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.7 Secure Coding Guidelines</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fb-grid">
            <div class="fb-field"><label>Guideline Rule</label><p>{title}</p></div>
            <div class="fb-field"><label>File Location</label><p class="path">{fpath}:{line}</p></div>
          </div>
          {snippet_html}
          <div class="fix-box" style="margin-top:8px;">
            <label>✅ Secure Coding Remediation</label>
            <p>{rem}</p>
          </div>
        </div>
      </div>'''
            cards.append(card)

        # 2.10 Remediation Guides
            item_id = item.get("item_id", "REM-000")
            clean_id = str(item_id).replace('.', '_').replace('/', '_').replace(':', '_').replace('-', '_')
            title = item.get("summary", item_id)
            sla = item.get("priority_sla", "24h")
            sev = "HIGH" if sla in ["24h", "immediate_24h"] else "MEDIUM"
            sev_class = sev.lower()
            patch = item.get("code_patch", "")
            patch_html = f'<div class="code-block" style="background:#062016;color:#6ee7b7;">{patch}</div>' if patch else ''
            
            card = f'''
      <div class="finding-card" id="card-{clean_id}" data-stages="2.10" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{clean_id}\')">
          <span class="finding-sev sev-{sev_class}">SLA {sla}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.10 Remediation Guide</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fix-box">
            <label>✅ Actionable Code Patch ({item.get("target_finding_ref", "")})</label>
            <p>{title}</p>
            {patch_html}
          </div>
        </div>
      </div>'''
            cards.append(card)

        # 2.10 Remediation Guides
        s210 = stages_data.get("2.10", {}).get("results", [])
        for item in s210:
            if item.get("status") in ["PASS", "DONE", "RESOLVED"]: continue
            cid = item.get("component_id", "all")
            if component_id and cid != component_id: continue
            
            item_id = item.get("item_id", "REM-000")
            title = item.get("summary", item_id)
            sla = item.get("priority_sla", "24h")
            sev = "HIGH" if sla in ["24h", "immediate_24h"] else "MEDIUM"
            sev_class = sev.lower()
            patch = item.get("code_patch", "")
            patch_html = f'<div class="code-block" style="background:#062016;color:#6ee7b7;">{patch}</div>' if patch else ''
            
            card = f'''
      <div class="finding-card" id="card-{item_id}" data-stages="2.10" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'card-{item_id}\')">
          <span class="finding-sev sev-{sev_class}">SLA {sla}</span>
          <span class="finding-name">[{cid}] [{item_id}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">2.10 Remediation Guide</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fix-box">
            <label>✅ Actionable Code Patch ({item.get("target_finding_ref", "")})</label>
            <p>{title}</p>
            {patch_html}
          </div>
        </div>
      </div>'''
            cards.append(card)

        return cards

    def build_markdown_report(self, project_info, findings_data, risk_data, component_id=None):
        """Build GitHub-Flavored Markdown Report."""
        risk_scoring = risk_data.get("risk_scoring", {})
        roadmap = risk_data.get("remediation_roadmap", {})
        all_findings = findings_data.get("findings", [])

        if component_id:
            findings = [f for f in all_findings if f.get("component_id") == component_id]
            title_suffix = f"— {component_id.upper()}"
        else:
            findings = all_findings
            title_suffix = f"— {self.project_id.upper()} (Executive Overview)"

        md = []
        md.append(f"# 🛡️ ASRP Application Security Review Report {title_suffix}\n")
        md.append(f"> **Run ID:** `{self.run_id}` | **Audit Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        md.append(f"> **Target Project:** {project_info.get('name', self.project_id)}  \n")
        md.append(f"> **Security Gate Status:** **`{risk_scoring.get('status', 'ACTION REQUIRED')}`**\n")
        md.append("---\n")

        # Executive Summary Scorecard
        md.append("## 📊 Executive Scorecard & Risk Rating\n")
        md.append(f"| Metric | Value |")
        md.append(f"|---|---|")
        md.append(f"| **Security Health Score** | **`{risk_scoring.get('security_score', 0)} / 100`** (Grade `{risk_scoring.get('grade', 'F')}`) |")
        md.append(f"| **Risk Rating** | **{risk_scoring.get('rating', 'FAIL / CRITICAL RISK')}** |")
        md.append(f"| **Total Findings** | **{len(findings)}** |")
        md.append(f"| **Business Criticality** | `{risk_data.get('business_context', {}).get('business_criticality', 'N/A')}` |\n")

        md.append("### 📈 Severity Breakdown\n")
        sev = risk_scoring.get("severity_counts", {})
        md.append(f"- 🔴 **CRITICAL:** `{sev.get('CRITICAL', 0)}`")
        md.append(f"- 🟠 **HIGH:** `{sev.get('HIGH', 0)}`")
        md.append(f"- 🟡 **MEDIUM:** `{sev.get('MEDIUM', 0)}`")
        md.append(f"- 🔵 **LOW:** `{sev.get('LOW', 0)}`")
        md.append("\n---\n")

        # SLA Roadmap
        md.append("## 📅 Prioritized Remediation Roadmap (SLA)\n")
        for phase_key, phase_name in [("phase_1_immediate", "Phase 1: Emergency Fixes (SLA 24-48h)"), 
                                     ("phase_2_shortterm", "Phase 2: High Priority Hardening (SLA 7 days)"), 
                                     ("phase_3_maintenance", "Phase 3: General Maintenance (SLA 30 days)")]:
            p_data = roadmap.get(phase_key, {})
            items = p_data.get("items", [])
            if component_id:
                items = [i for i in items if component_id in i.get("finding_id", "")]
            md.append(f"### 🎯 {phase_name} ({len(items)} items)")
            for item in items:
                md.append(f"- **`[{item.get('severity')}]` [{item.get('finding_id')}]** `{item.get('title')}` — *{item.get('file')}*")
            md.append("")

        md.append("---\n")

        # Detailed Findings Table
        md.append(f"## 🔍 Detailed Security Findings ({len(findings)})\n")
        for f in findings:
            md.append(f"### [{f.get('finding_id')}] {f.get('title')}")
            md.append(f"- **Component:** `{f.get('component_id')}` | **Severity:** `{f.get('severity')}` | **Engine:** `{f.get('engine')}`")
            md.append(f"- **Domain:** `{f.get('security_domain')}` | **Checklist Ref:** `{f.get('review_checklist_ref')}`")
            md.append(f"- **File:** `{f.get('location', {}).get('file_path')}` (Line: `{f.get('location', {}).get('start_line', 1)}`)")
            owasp_str = ", ".join(f.get("standard_mapping", {}).get("owasp_top10_2021", []))
            cwe_str = ", ".join(f.get("standard_mapping", {}).get("cwe", []))
            md.append(f"- **Standard Mapping:** {owasp_str} | {cwe_str}")
            md.append("\n**Evidence Code Snippet:**")
            md.append("```typescript")
            md.append(f"{f.get('evidence', {}).get('code_snippet', '# No snippet')}")
            md.append("```")
            md.append(f"\n💡 **Remediation:** {f.get('remediation', {}).get('summary')}")
            if f.get('remediation', {}).get('code_patch'):
                md.append(f"```diff\n{f.get('remediation', {}).get('code_patch')}\n```")
            md.append("\n---\n")

        return "\n".join(md)

    def _build_html_head_styles(self, title):
        return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-card: #1e293b;
            --bg-card-hover: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-red: #ef4444;
            --accent-orange: #f97316;
            --accent-yellow: #eab308;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', system-ui, -apple-system, sans-serif; }}
        body {{ background-color: var(--bg-primary); color: var(--text-main); padding: 2rem; line-height: 1.6; }}
        .container {{ max-width: 1250px; margin: 0 auto; }}

        .header {{ display: flex; justify-content: space-between; align-items: center; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); margin-bottom: 2rem; }}
        .brand {{ display: flex; align-items: center; gap: 14px; }}
        .brand-logo {{ width: 46px; height: 46px; background: linear-gradient(135deg, #6366f1, #a855f7); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 22px; color: #fff; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4); }}
        .brand-title h1 {{ font-size: 1.5rem; font-weight: 700; background: linear-gradient(to right, #ffffff, #cbd5e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .brand-title p {{ color: var(--text-muted); font-size: 0.875rem; }}
        .status-badge {{ background: rgba(16, 185, 129, 0.15); color: var(--accent-green); padding: 8px 18px; border-radius: 20px; font-weight: 700; border: 1px solid var(--accent-green); font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.5px; }}
        .back-link {{ color: #38bdf8; text-decoration: none; font-size: 0.875rem; font-weight: 600; margin-bottom: 1.25rem; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s; }}
        .back-link:hover {{ color: #7dd3fc; transform: translateX(-3px); }}

        .hero-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 1.5rem; margin-bottom: 2rem; }}
        .card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); }}
        .score-card {{ text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .score-ring {{ width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-direction: column; margin: 1rem 0; box-shadow: 0 0 20px rgba(16, 185, 129, 0.2); }}
        .score-val {{ font-size: 2.2rem; font-weight: 800; }}
        .score-grade {{ font-size: 1rem; font-weight: 700; color: var(--text-muted); }}

        .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }}
        .metric-box {{ background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border-color); border-radius: 10px; padding: 1rem; text-align: center; }}
        .metric-val {{ font-size: 1.8rem; font-weight: 800; margin-top: 4px; }}
        .val-critical {{ color: var(--accent-red); }}
        .val-high {{ color: var(--accent-orange); }}
        .val-medium {{ color: var(--accent-yellow); }}
        .val-low {{ color: var(--accent-blue); }}

        .section-title {{ font-size: 1.25rem; font-weight: 700; margin: 2.5rem 0 1rem 0; color: #f1f5f9; display: flex; align-items: center; justify-content: space-between; }}

        /* Interactive Stage Cards Grid */
        .stages-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .stage-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-left: 4px solid #38bdf8; border-radius: 12px; padding: 1.25rem; cursor: pointer; transition: all 0.25s ease; position: relative; user-select: none; }}
        .stage-card:hover {{ background: var(--bg-card-hover); transform: translateY(-2px); border-color: #38bdf8; box-shadow: 0 6px 16px rgba(56, 189, 248, 0.2); }}
        .stage-card.active-stage {{ border-color: #38bdf8; border-left-width: 6px; background: rgba(56, 189, 248, 0.12); box-shadow: 0 0 20px rgba(56, 189, 248, 0.3); }}
        .stage-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }}
        .stage-name {{ font-weight: 700; font-size: 1rem; color: #38bdf8; display: flex; align-items: center; gap: 8px; }}
        .stage-file {{ font-size: 0.8rem; font-family: 'Fira Code', monospace; color: var(--text-muted); margin-bottom: 0.5rem; }}
        .stage-badge {{ padding: 3px 9px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; background: rgba(16, 185, 129, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }}
        .stage-click-hint {{ font-size: 0.75rem; color: #38bdf8; font-weight: 600; margin-top: 0.5rem; display: inline-flex; align-items: center; gap: 4px; }}

        /* Filter Banner */
        .filter-banner {{ display: none; background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1.5rem; justify-content: space-between; align-items: center; color: #7dd3fc; font-weight: 600; font-size: 0.95rem; animation: fadeIn 0.3s ease; }}
        .btn-reset-filter {{ background: #38bdf8; color: #0f172a; border: none; padding: 6px 14px; border-radius: 6px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }}
        .btn-reset-filter:hover {{ background: #7dd3fc; }}

        /* Findings List */
        .finding-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.25rem; transition: all 0.2s; position: relative; }}
        .finding-card:hover {{ border-color: #475569; }}
        .finding-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }}
        .finding-id {{ font-family: 'Fira Code', monospace; font-weight: 700; color: #38bdf8; font-size: 1.05rem; }}
        .sev-badge {{ padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; }}
        .sev-CRITICAL, .sev-critical {{ background: rgba(239, 68, 68, 0.2); color: var(--accent-red); border: 1px solid var(--accent-red); }}
        .sev-HIGH, .sev-high {{ background: rgba(249, 115, 22, 0.2); color: var(--accent-orange); border: 1px solid var(--accent-orange); }}
        .sev-MEDIUM, .sev-medium {{ background: rgba(234, 179, 8, 0.2); color: var(--accent-yellow); border: 1px solid var(--accent-yellow); }}
        .sev-LOW, .sev-low {{ background: rgba(59, 130, 246, 0.2); color: var(--accent-blue); border: 1px solid var(--accent-blue); }}

        .stage-tag-list {{ display: flex; gap: 6px; margin-top: 0.5rem; flex-wrap: wrap; }}
        .stage-tag {{ background: rgba(148, 163, 184, 0.1); border: 1px solid rgba(148, 163, 184, 0.2); color: #cbd5e1; font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 4px; }}

        pre {{ background: #090d16; padding: 1rem; border-radius: 8px; font-family: 'Fira Code', monospace; font-size: 0.85rem; overflow-x: auto; color: #38bdf8; margin-top: 0.75rem; border: 1px solid var(--border-color); line-height: 1.5; }}
        .patch-box {{ background: rgba(16, 185, 129, 0.08); border-left: 4px solid var(--accent-green); padding: 1rem; margin-top: 0.75rem; border-radius: 6px; font-size: 0.875rem; color: #6ee7b7; }}

        /* Component Cards */
        .comp-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
        .comp-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; transition: all 0.2s; }}
        .comp-card:hover {{ border-color: #38bdf8; transform: translateY(-2px); }}
        .comp-title {{ font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.25rem; display: flex; justify-content: space-between; align-items: center; }}
        .comp-tech {{ color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1rem; }}
        .comp-action-btn {{ display: inline-block; margin-top: 1rem; background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid #38bdf8; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }}
        .comp-action-btn:hover {{ background: #38bdf8; color: #0f172a; }}

        footer {{ text-align: center; padding: 2.5rem 0; color: var(--text-muted); font-size: 0.85rem; border-top: 1px solid var(--border-color); margin-top: 3.5rem; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(-4px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
"""

    def _build_interactive_js(self):
        return """
    <script>
        function filterByStage(stageKey, cardEl) {
            const allCards = document.querySelectorAll('.stage-card');
            const isActive = cardEl.classList.contains('active-stage');

            // Reset active states
            allCards.forEach(c => c.classList.remove('active-stage'));

            const banner = document.getElementById('filter-banner');
            const findings = document.querySelectorAll('.finding-card');

            // Toggle off if clicking the already active card
            if (isActive || stageKey === 'all') {
                banner.style.display = 'none';
                findings.forEach(f => f.style.display = 'block');
                return;
            }

            cardEl.classList.add('active-stage');
            banner.style.display = 'flex';

            let count = 0;
            findings.forEach(f => {
                const stagesStr = f.getAttribute('data-stages') || '';
                const stagesList = stagesStr.split(' ');
                if (stagesList.includes(stageKey)) {
                    f.style.display = 'block';
                    count++;
                } else {
                    f.style.display = 'none';
                }
            });

            const stageNames = {
                '2.1': '2.1 Security Standards (OWASP & CWE)',
                '2.2': '2.2 Security Domains (Domain Classification)',
                '2.3': '2.3 Rule Library (Static & AI Rules)',
                '2.4': '2.4 Review Checklists (Verification Items)',
                '2.6': '2.6 Threat Models (STRIDE Threat Scenarios)',
                '2.10': '2.10 Remediation Guides (Code Diff Patches)'
            };

            const filterText = document.getElementById('filter-text');
            filterText.innerHTML = '🎯 Đang lọc theo Module <strong>[' + (stageNames[stageKey] || stageKey) + ']</strong> — Hiển thị <strong>' + count + '</strong> lỗ hổng tương ứng.';
            
            // Smooth scroll down to findings section
            document.getElementById('findings-section').scrollIntoView({ behavior: 'smooth' });
        }

        function resetStageFilter() {
            filterByStage('all', null);
        }
    </script>
"""

    def build_executive_html_report(self, project_info, findings_data, risk_data, stages_data):
        """Build Consolidated Executive Project Dashboard HTML Report using executive_dashboard.html template."""
        risk_scoring = risk_data.get("risk_scoring", {})
        roadmap = risk_data.get("remediation_roadmap", {})
        findings = findings_data.get("findings", [])
        sev = risk_scoring.get("severity_counts", {})
        score = risk_scoring.get('security_score', 0)
        grade = risk_scoring.get('grade', 'F')
        comp_summary = findings_data.get("components_summary", {})

        if os.path.exists(self.exec_template_file):
            with open(self.exec_template_file, 'r', encoding='utf-8') as f:
                template = f.read()
        else:
            raise FileNotFoundError(f"Template file not found: {self.exec_template_file}")

        # Render Component Cards for score-grid
        comp_cards_html = []
        for comp_id, comp_meta in comp_summary.items():
            c_score = comp_meta.get("health_score", 100)
            c_grade = comp_meta.get("grade", "A")
            c_color = "#10b981" if c_score >= 80 else ("#f59e0b" if c_score >= 70 else "#ef4444")
            c_bg = "rgba(16,185,129,0.12)" if c_score >= 80 else ("rgba(245,158,11,0.12)" if c_score >= 70 else "rgba(239,68,68,0.12)")
            c_rating = "PASS" if c_score >= 80 else ("MODERATE RISK" if c_score >= 70 else "ACTION REQUIRED")
            c_stack = comp_meta.get('tech_stack', 'Source Sub-repository')
            c_findings = [f for f in findings if f.get('component_id') == comp_id]
            c_sev = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for f in c_findings:
                s = f.get('severity', 'MEDIUM').upper()
                c_sev[s] = c_sev.get(s, 0) + 1

            comp_card_html = f'''
    <div class="score-card" id="card-{comp_id}" style="border-top: 3px solid {c_color}; cursor: pointer;" onclick="window.location.href=\'security_review_report_{comp_id}.html\'">
      <div class="score-card-label">COMPONENT SECURITY REPORT</div>
      <div class="score-card-name">{comp_id}</div>
      <div class="score-card-stack">{c_stack}</div>
      <div class="score-display">
        <div class="score-num" style="color:{c_color}">{c_score}</div>
        <div>
          <div class="score-grade-badge" style="background:{c_bg};color:{c_color}">Grade {c_grade}</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">{c_rating}</div>
        </div>
      </div>
      <div class="score-progress">
        <div class="score-progress-fill" style="background:{c_color};width:{c_score}%"></div>
      </div>
      <div class="score-breakdown">
        <div class="score-bk crit"><div class="score-bk-num">{c_sev['CRITICAL']}</div><div class="score-bk-label">Critical</div></div>
        <div class="score-bk high"><div class="score-bk-num">{c_sev['HIGH']}</div><div class="score-bk-label">High</div></div>
        <div class="score-bk med"> <div class="score-bk-num">{c_sev['MEDIUM']}</div><div class="score-bk-label">Medium</div></div>
        <div class="score-bk low"> <div class="score-bk-num">{c_sev['LOW']}</div><div class="score-bk-label">Low</div></div>
      </div>
      <a href="security_review_report_{comp_id}.html" style="margin-top:12px;display:inline-block;font-size:12px;color:var(--accent-blue);font-weight:600;text-decoration:none;">🔍 Open Component Report →</a>
    </div>'''
            comp_cards_html.append(comp_card_html)

        grid_html = "\n".join(comp_cards_html)

        # Render Quick Links Cards
        ql_cards = []
        for cid, cm in comp_summary.items():
            icon = '⚙️' if 'api' in cid else '🖥️'
            ql_cards.append(f'''
    <a class="ql-card" href="security_review_report_{cid}.html" target="_blank">
      <div class="ql-icon">{icon}</div>
      <div>
        <div class="ql-title">{cid} Detail Security Report</div>
        <div class="ql-sub">{cm.get('tech_stack', 'Sub-repo')} · {cm.get('findings_count', 0)} findings · Grade {cm.get('grade', 'B')} · Click to view →</div>
      </div>
      <div class="ql-arrow">→</div>
    </a>''')
        quick_links_html = "\n".join(ql_cards)

        # Render Component Filter Pills
        cpills = []
        for cid in comp_summary.keys():
            icon = '⚙️' if 'api' in cid else '🖥️'
            cpills.append(f'<div class="comp-pill" id="cpill-{cid}" onclick="filterComp(\'{cid}\')">{icon} {cid}</div>')
        comp_pills_html = "\n".join(cpills)

        # Render Findings Cards for Executive Dashboard
        exec_findings_cards = []
        for f in findings:
            fid = f.get('finding_id', 'F-000')
            sev_name = f.get('severity', 'MEDIUM').upper()
            sev_class = sev_name.lower()
            title = f.get('title', '')
            domain = f.get('security_domain', 'security')
            cid = f.get('component_id', '')
            loc = f.get('location', {})
            file_path = loc.get('file_path', 'N/A')
            start_line = loc.get('start_line', 1)
            mapped_stages_str = self._get_finding_stages(f, stages_data)
            stage_refs_display = " · ".join(mapped_stages_str.split())
            
            snippet = f.get('evidence', {}).get('code_snippet', '# No code snippet')
            snippet_html = f'<div class="code-block">{snippet}</div>' if snippet else ''
            msg = f.get('evidence', {}).get('message', '')
            
            owasp_list = f.get('standard_mapping', {}).get('owasp_top10_2021', [])
            cwe_list = f.get('standard_mapping', {}).get('cwe', [])
            asvs_list = f.get('standard_mapping', {}).get('asvs_v4', [])
            
            tags_html = ""
            for cwe in cwe_list:
                tags_html += f'<span class="tag tag-cwe">{cwe}</span> '
            for owasp in owasp_list:
                tags_html += f'<span class="tag tag-owasp">{owasp}</span> '
            for asvs in asvs_list:
                tags_html += f'<span class="tag tag-asvs">{asvs}</span> '
                
            rem = f.get('remediation', {})
            rem_ref = f.get('review_checklist_ref', '')
            rem_summary = rem.get('summary', 'Remediate issue.')
            code_patch = rem.get('code_patch', '')
            patch_html = f'<div class="code-block" style="margin-top:6px;background:#062016;color:#6ee7b7;">{code_patch}</div>' if code_patch else ''

            card_html = f'''
      <div class="finding-card" id="F-{fid}" data-stages="all" data-comp="{cid}">
        <div class="finding-header" onclick="toggleF(\'F-{fid}\')">
          <span class="finding-sev sev-{sev_class}">{sev_name}</span>
          <span class="finding-name">[{cid}] {title}</span>
          <span class="comp-tag" style="background:rgba(59,130,246,0.12);color:var(--accent-blue)">{cid}</span>
          <span class="stage-tag">{stage_refs_display}</span>
          <span class="find-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="fb-grid">
            <div class="fb-field"><label>File</label><p class="path">{file_path}:{start_line}</p></div>
            <div class="fb-field"><label>Domain</label><p>{domain}</p></div>
          </div>
          {snippet_html}
          <p style="font-size:13px;color:var(--text-secondary);margin:8px 0;">{msg}</p>
          <div class="tags-row">{tags_html}</div>
          <div class="fix-box">
            <label>✅ Actionable Remediation ({rem_ref})</label>
            <p>{rem_summary}</p>
            {patch_html}
          </div>
        </div>
      </div>'''
            exec_findings_cards.append(card_html)

        stage_cards = self._render_stage_output_cards(stages_data, component_id=None)
        exec_findings_cards.extend(stage_cards)

        exec_findings_html = "\n".join(exec_findings_cards)

        # Replace placeholders in template
        html = template
        html = html.replace("{{PROJECT_NAME}}", project_info.get('name', self.project_id))
        html = html.replace("{{RUN_ID}}", self.run_id)
        html = html.replace("{{RUN_DATE}}", datetime.now().strftime('%Y-%m-%d'))
        html = html.replace("{{RUN_YEAR}}", datetime.now().strftime('%Y'))
        html = html.replace("{{ENGINE}}", "Claude Sonnet 4.6 Thinking")
        html = html.replace("{{TOTAL_FINDINGS}}", str(len(findings)))
        html = html.replace("{{COUNT_CRITICAL}}", str(sev.get('CRITICAL', 0)))
        html = html.replace("{{COUNT_HIGH}}", str(sev.get('HIGH', 0)))
        html = html.replace("{{COUNT_MEDIUM}}", str(sev.get('MEDIUM', 0)))
        html = html.replace("{{COUNT_LOW}}", str(sev.get('LOW', 0)))
        html = html.replace("{{COMPONENT_COUNT}}", str(len(comp_summary)))
        html = html.replace("{{PROJECT_OVERALL_SCORE}}", str(score))
        html = html.replace("{{PROJECT_OVERALL_GRADE}}", grade)
        html = html.replace("{{PROJECT_OVERALL_RATING}}", risk_scoring.get('rating', 'PASS'))
        html = html.replace("{{GATE_STATUS_TEXT}}", risk_scoring.get('status', 'ACTION REQUIRED'))
        html = html.replace("{{GATE_STATUS_EMOJI}}", "🔴" if risk_scoring.get('status') == 'ACTION REQUIRED' else "🟢")

        html = html.replace("{{STAGE_2_1_COUNT}}", str(self._count_stage_issues("2.1", stages_data)))
        html = html.replace("{{STAGE_2_2_COUNT}}", str(self._count_stage_issues("2.2", stages_data)))
        html = html.replace("{{STAGE_2_3_COUNT}}", str(self._count_stage_issues("2.3", stages_data)))
        html = html.replace("{{STAGE_2_4_COUNT}}", str(self._count_stage_issues("2.4", stages_data)))
        html = html.replace("{{STAGE_2_6_COUNT}}", str(self._count_stage_issues("2.6", stages_data)))
        html = html.replace("{{STAGE_2_7_COUNT}}", str(self._count_stage_issues("2.7", stages_data)))
        html = html.replace("{{STAGE_2_10_COUNT}}", str(self._count_stage_issues("2.10", stages_data)))

        html = html.replace("{{SCORE_GRID_CARDS}}", grid_html)
        html = html.replace("{{QUICK_LINKS_CARDS}}", quick_links_html)
        html = html.replace("{{COMPONENT_PILLS_HTML}}", comp_pills_html)
        html = html.replace("{{EXECUTIVE_FINDINGS_HTML}}", exec_findings_html)

        return html

    def build_component_html_report(self, project_info, findings_data, risk_data, stages_data, component_id):
        """Build Standalone HTML Security Report for a specific component using component_report.html template."""
        risk_scoring = risk_data.get("risk_scoring", {})
        all_findings = findings_data.get("findings", [])
        findings = [f for f in all_findings if f.get("component_id") == component_id]
        
        comp_summary = findings_data.get("components_summary", {}).get(component_id, {})
        c_score = comp_summary.get("health_score", risk_scoring.get('security_score', 80))
        c_grade = comp_summary.get("grade", risk_scoring.get('grade', 'B'))
        c_color = "#10b981" if c_score >= 80 else ("#f59e0b" if c_score >= 70 else "#ef4444")
        c_bg = "rgba(16,185,129,0.12)" if c_score >= 80 else ("rgba(245,158,11,0.12)" if c_score >= 70 else "rgba(239,68,68,0.12)")

        sev_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for f in findings:
            s = f.get("severity", "MEDIUM").upper()
            sev_counts[s] = sev_counts.get(s, 0) + 1

        if os.path.exists(self.comp_template_file):
            with open(self.comp_template_file, 'r', encoding='utf-8') as f:
                template = f.read()
        else:
            raise FileNotFoundError(f"Template file not found: {self.comp_template_file}")

        # Render Finding Cards for component
        findings_cards_html = []
        for f in findings:
            fid = f.get('finding_id', 'F-000')
            sev_name = f.get('severity', 'MEDIUM').upper()
            sev_class = sev_name.lower()
            title = f.get('title', '')
            domain = f.get('security_domain', 'security')
            loc = f.get('location', {})
            file_path = loc.get('file_path', 'N/A')
            start_line = loc.get('start_line', 1)
            end_line = loc.get('end_line', start_line)
            mapped_stages_str = self._get_finding_stages(f, stages_data)
            stage_refs_display = " · ".join(mapped_stages_str.split())
            
            snippet = f.get('evidence', {}).get('code_snippet', '# No code snippet')
            snippet_html = f'<div class="code-snippet">{snippet}</div>' if snippet else ''
            msg = f.get('evidence', {}).get('message', '')
            
            owasp_list = f.get('standard_mapping', {}).get('owasp_top10_2021', [])
            cwe_list = f.get('standard_mapping', {}).get('cwe', [])
            asvs_list = f.get('standard_mapping', {}).get('asvs_v4', [])
            
            tags_html = ""
            for cwe in cwe_list:
                tags_html += f'<span class="finding-tag cwe">{cwe}</span> '
            for owasp in owasp_list:
                tags_html += f'<span class="finding-tag owasp">{owasp}</span> '
            for asvs in asvs_list:
                tags_html += f'<span class="finding-tag asvs">{asvs}</span> '
                
            rem = f.get('remediation', {})
            rem_ref = f.get('review_checklist_ref', '')
            rem_summary = rem.get('summary', 'Review and remediate issue.')
            code_patch = rem.get('code_patch', '')
            patch_html = f'<div class="code-snippet" style="margin-top:8px;">{code_patch}</div>' if code_patch else ''

            card_html = f'''
      <div class="finding-card" id="F-{fid}" data-stages="all">
        <div class="finding-header" onclick="toggleFinding(\'F-{fid}\')">
          <span class="finding-severity sev-{sev_class}">{sev_name}</span>
          <span class="finding-title">{title}</span>
          <span class="stage-badge">{stage_refs_display}</span>
          <span class="finding-id">{fid}</span>
          <span class="finding-toggle">▼</span>
        </div>
        <div class="finding-body">
          <div class="finding-grid">
            <div class="finding-field">
              <label>File Location</label>
              <p class="file-path">{file_path} · Lines {start_line}–{end_line}</p>
            </div>
            <div class="finding-field">
              <label>Security Domain</label>
              <p>{domain}</p>
            </div>
          </div>
          <label style="font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--text-muted);display:block;margin-bottom:4px;">Evidence Code</label>
          {snippet_html}
          <p style="font-size:13px;color:var(--text-secondary);margin:12px 0;">{msg}</p>
          <div class="finding-tags">{tags_html}</div>
          <div class="remediation-box">
            <label>✅ Remediation ({rem_ref}) – SLA Roadmap</label>
            <p>{rem_summary}</p>
            {patch_html}
          </div>
        </div>
      </div>'''
            findings_cards_html.append(card_html)

        stage_cards = self._render_stage_output_cards(stages_data, component_id=component_id)
        findings_cards_html.extend(stage_cards)

        comp_findings_html = "\n".join(findings_cards_html) if findings_cards_html else "<p style='color:var(--pass);'>No security vulnerabilities detected for this component.</p>"

        # Security Strengths
        checklists = stages_data.get("2.4", {}).get("results", [])
        pass_items = [item for item in checklists if item.get("status") == "PASS"]
        if pass_items:
            strengths_cards = []
            for item in pass_items:
                ev = item.get("evidence", "")
                ev_msg = ev.get("message", "Compliant with security standards.") if isinstance(ev, dict) else str(ev or "Compliant with security standards.")
                strengths_cards.append(f'''
    <div class="pos-card">
      <div class="pos-icon">✅</div>
      <div>
        <div class="pos-title">{item.get("verification_requirement", "Security Verification Passed")}</div>
        <div class="pos-desc">{ev_msg}</div>
      </div>
    </div>''')
            strengths_html = f'''
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:rgba(16,185,129,0.15)">✅</div>
      <div>
        <div class="section-title">Security Strengths</div>
        <div class="section-sub">Những gì đang hoạt động tốt trong {component_id}</div>
      </div>
    </div>
    {"".join(strengths_cards)}
  </div>'''
        else:
            strengths_html = ""

        # SLA Roadmap
        roadmap = risk_data.get("remediation_roadmap", {})
        p1_items = [i for i in roadmap.get("phase_1_immediate", {}).get("items", []) if component_id in i.get("finding_id", "") or not component_id]
        p2_items = [i for i in roadmap.get("phase_2_shortterm", {}).get("items", []) if component_id in i.get("finding_id", "") or not component_id]
        p3_items = [i for i in roadmap.get("phase_3_maintenance", {}).get("items", []) if component_id in i.get("finding_id", "") or not component_id]

        def _render_sla_items(items):
            out = []
            for it in items:
                s_class = it.get('severity', 'MEDIUM').lower()
                out.append(f'''
        <div class="sla-item">
          <span class="finding-severity sev-{s_class}" style="font-size:10px;min-width:65px;text-align:center;">{it.get('severity')}</span>
          <span class="sla-item-title">{it.get('title')} ({it.get('file')})</span>
          <span class="sla-effort">{it.get('effort', '1d')} · {it.get('team', 'DevSecOps')}</span>
        </div>''')
            return "\n".join(out)

        sla_html = f'''
    <div class="sla-phase phase-1 open">
      <div class="sla-phase-header" onclick="toggleSLA(this)">
        <div class="sla-phase-icon">🚨</div>
        <div class="sla-phase-title">Phase 1 – Emergency Fixes</div>
        <div class="sla-phase-badge">SLA 24-48 Hours · {len(p1_items)} items</div>
        <span style="color:var(--text-muted)">▼</span>
      </div>
      <div class="sla-body">
        {_render_sla_items(p1_items) if p1_items else '<p style="font-size:12px;color:var(--text-muted);padding:8px 0;">No immediate SLA items required.</p>'}
      </div>
    </div>

    <div class="sla-phase phase-2 open">
      <div class="sla-phase-header" onclick="toggleSLA(this)">
        <div class="sla-phase-icon">⚡</div>
        <div class="sla-phase-title">Phase 2 – High Priority Hardening</div>
        <div class="sla-phase-badge">SLA 7 Days · {len(p2_items)} items</div>
        <span style="color:var(--text-muted)">▼</span>
      </div>
      <div class="sla-body">
        {_render_sla_items(p2_items) if p2_items else '<p style="font-size:12px;color:var(--text-muted);padding:8px 0;">No phase 2 items required.</p>'}
      </div>
    </div>

    <div class="sla-phase phase-3">
      <div class="sla-phase-header" onclick="toggleSLA(this)">
        <div class="sla-phase-icon">🔧</div>
        <div class="sla-phase-title">Phase 3 – General Maintenance</div>
        <div class="sla-phase-badge">SLA 30 Days · {len(p3_items)} items</div>
        <span style="color:var(--text-muted)">▼</span>
      </div>
      <div class="sla-body">
        {_render_sla_items(p3_items) if p3_items else '<p style="font-size:12px;color:var(--text-muted);padding:8px 0;">No phase 3 items required.</p>'}
      </div>
    </div>'''

        # Extract prefix / suffix
        comp_parts = component_id.split('-')
        prefix = comp_parts[0].upper() if comp_parts else component_id.upper()
        suffix = "-".join(comp_parts[1:]).upper() if len(comp_parts) > 1 else ""
        dash_offset = f"{364.4 * (1 - c_score / 100):.1f}"

        # Replace placeholders in template
        html = template
        html = html.replace("{{PROJECT_NAME}}", project_info.get('name', self.project_id))
        html = html.replace("{{COMPONENT_NAME}}", component_id)
        html = html.replace("{{COMPONENT_NAME_PREFIX}}", prefix)
        html = html.replace("{{COMPONENT_NAME_SUFFIX}}", suffix)
        html = html.replace("{{COMPONENT_ICON}}", "🛡️" if "api" in component_id else "🎨")
        html = html.replace("{{COMPONENT_DESC}}", comp_summary.get('tech_stack', 'Source Sub-repository Component'))
        html = html.replace("{{COMPONENT_HEADER_GRADIENT}}", "linear-gradient(135deg, #f97316, #ef4444)" if "api" in component_id else "linear-gradient(135deg, #10b981, #06b6d4)")
        html = html.replace("{{COMPONENT_HERO_TINT}}", "rgba(249, 115, 22, 0.15)" if "api" in component_id else "rgba(16, 185, 129, 0.15)")
        html = html.replace("{{COMPONENT_STACK}}", comp_summary.get('tech_stack', 'TypeScript / Node.js'))
        html = html.replace("{{ENGINE}}", "Claude Sonnet 4.6 Thinking")
        html = html.replace("{{RUN_ID}}", self.run_id)
        html = html.replace("{{RUN_DATE}}", datetime.now().strftime('%Y-%m-%d'))
        html = html.replace("{{TOTAL_FINDINGS}}", str(len(findings)))
        html = html.replace("{{COUNT_CRITICAL}}", str(sev_counts['CRITICAL']))
        html = html.replace("{{COUNT_HIGH}}", str(sev_counts['HIGH']))
        html = html.replace("{{COUNT_MEDIUM}}", str(sev_counts['MEDIUM']))
        html = html.replace("{{COUNT_LOW}}", str(sev_counts['LOW']))
        html = html.replace("{{HEALTH_SCORE}}", str(c_score))
        html = html.replace("{{HEALTH_GRADE}}", c_grade)
        html = html.replace("{{GRADE_COLOR}}", c_color)
        html = html.replace("{{GRADE_BG}}", c_bg)
        html = html.replace("{{SCORE_DASHOFFSET}}", dash_offset)

        html = html.replace("{{GATE_STATUS_TEXT}}", risk_scoring.get('status', 'ACTION REQUIRED'))
        html = html.replace("{{GATE_ICON}}", "⚠️" if risk_scoring.get('status') == 'ACTION REQUIRED' else "✅")
        html = html.replace("{{GATE_DESC}}", f"Component Health Score is {c_score}/100 (Grade {c_grade}). Remediation required.")
        html = html.replace("{{GATE_TITLE_COLOR}}", c_color)
        html = html.replace("{{GATE_BANNER_BG}}", "rgba(239, 68, 68, 0.1)" if c_score < 70 else "rgba(16, 185, 129, 0.1)")
        html = html.replace("{{GATE_BANNER_BORDER}}", "rgba(239, 68, 68, 0.3)" if c_score < 70 else "rgba(16, 185, 129, 0.3)")
        html = html.replace("{{GATE_BADGE_BG}}", "rgba(239, 68, 68, 0.15)" if c_score < 70 else "rgba(16, 185, 129, 0.15)")
        html = html.replace("{{GATE_BADGE_COLOR}}", c_color)
        html = html.replace("{{GATE_BADGE_BORDER}}", "rgba(239, 68, 68, 0.4)" if c_score < 70 else "rgba(16, 185, 129, 0.4)")
        html = html.replace("{{GATE_STATUS_EMOJI}}", "🔴" if c_score < 70 else "🟢")

        html = html.replace("{{STAGE_2_1_COUNT}}", str(self._count_stage_issues("2.1", stages_data, component_id)))
        html = html.replace("{{STAGE_2_2_COUNT}}", str(self._count_stage_issues("2.2", stages_data, component_id)))
        html = html.replace("{{STAGE_2_3_COUNT}}", str(self._count_stage_issues("2.3", stages_data, component_id)))
        html = html.replace("{{STAGE_2_4_COUNT}}", str(self._count_stage_issues("2.4", stages_data, component_id)))
        html = html.replace("{{STAGE_2_6_COUNT}}", str(self._count_stage_issues("2.6", stages_data, component_id)))
        html = html.replace("{{STAGE_2_7_COUNT}}", str(self._count_stage_issues("2.7", stages_data, component_id)))
        html = html.replace("{{STAGE_2_10_COUNT}}", str(self._count_stage_issues("2.10", stages_data, component_id)))

        html = html.replace("{{FINDINGS_CARDS_LIST}}", comp_findings_html)
        html = html.replace("{{SECURITY_STRENGTHS_BLOCK}}", strengths_html)
        html = html.replace("{{SLA_ROADMAP_BLOCK}}", sla_html)

        return html

    def run(self):
        """Execute Report Generator and output HTML & Markdown reports."""
        findings_file = os.path.join(self.target_run_dir, "findings.json")
        risk_file = os.path.join(self.target_run_dir, "risk_assessment.json")
        project_file = os.path.join(self.project_dir, "project.yaml")

        findings_data = load_json(findings_file)
        risk_data = load_json(risk_file)
        project_data = load_yaml(project_file) or {}
        stages_data = self._load_stage_outputs()

        if not findings_data or not risk_data:
            raise FileNotFoundError(f"Missing findings.json or risk_assessment.json in {self.target_run_dir}. Run Layer 3 first.")

        project_info = project_data.get("project", {})

        print(f"\n=======================================================")
        print(f"📊 STARTING LAYER 5 REPORT GENERATOR (STEP 3 execution)")
        print(f"📌 Project: {self.project_id} | Run ID: {self.run_id}")
        print(f"📋 Template Reference: {self.template_reports_dir}")
        print(f"=======================================================\n")

        generated_files = []

        # 1. Generate Executive Markdown & HTML Reports
        md_content = self.build_markdown_report(project_info, findings_data, risk_data)
        md_path = os.path.join(self.target_run_dir, "security_review_report.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        generated_files.append(md_path)
        print(f"[✓] Executive Markdown Report generated : {md_path}")

        html_content = self.build_executive_html_report(project_info, findings_data, risk_data, stages_data)
        html_path = os.path.join(self.target_run_dir, "security_review_report.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        generated_files.append(html_path)
        print(f"[✓] Executive HTML Dashboard generated   : {html_path}")

        # 2. Generate Component-Specific Markdown & HTML Reports
        comp_summary = findings_data.get("components_summary", {})
        for comp_id in comp_summary.keys():
            # Component MD
            c_md = self.build_markdown_report(project_info, findings_data, risk_data, component_id=comp_id)
            c_md_path = os.path.join(self.target_run_dir, f"security_review_report_{comp_id}.md")
            with open(c_md_path, 'w', encoding='utf-8') as f:
                f.write(c_md)
            generated_files.append(c_md_path)
            print(f"[✓] Component MD Report generated ({comp_id}) : {c_md_path}")

            # Component HTML
            c_html = self.build_component_html_report(project_info, findings_data, risk_data, stages_data, component_id=comp_id)
            c_html_path = os.path.join(self.target_run_dir, f"security_review_report_{comp_id}.html")
            with open(c_html_path, 'w', encoding='utf-8') as f:
                f.write(c_html)
            generated_files.append(c_html_path)
            print(f"[✓] Component HTML Report generated ({comp_id}) : {c_html_path}")

        print(f"\n=======================================================")
        print(f"🎉 SUCCESS: All Step 3 Reports generated successfully!")
        print(f"📍 Target Run Folder: {self.target_run_dir}")
        print(f"=======================================================\n")
        return generated_files


def main():
    parser = argparse.ArgumentParser(description="ASRP Layer 5 Report Generator CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID")
    parser.add_argument("--run-id", default=None, help="Target run ID (defaults to latest)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))

    generator = ReportGenerator(workspace_root, project_id=args.project, run_id=args.run_id)
    generator.run()


if __name__ == "__main__":
    main()
