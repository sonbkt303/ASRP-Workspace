#!/usr/bin/env python3
"""
ASRP Report Generator Module (Layer 5)
======================================
Generates standalone Executive HTML Dashboards and GitHub-Flavored Markdown
Security Review Reports based on Layer 1 Profile, Layer 3 Findings, and Risk Assessment.
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

    def build_markdown_report(self, project_info, findings_data, risk_data):
        """Build GitHub-Flavored Markdown Report."""
        risk_scoring = risk_data.get("risk_scoring", {})
        roadmap = risk_data.get("remediation_roadmap", {})
        findings = findings_data.get("findings", [])

        md = []
        md.append(f"# 🛡️ ASRP Application Security Review Report — {self.project_id.upper()}\n")
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
        md.append(f"| **Total Findings** | **{findings_data.get('total_findings', 0)}** |")
        md.append(f"| **Business Criticality** | `{risk_data.get('business_context', {}).get('business_criticality', 'N/A')}` |\n")

        md.append("### 📈 Severity Breakdown\n")
        sev = risk_scoring.get("severity_counts", {})
        md.append(f"- 🔴 **CRITICAL:** `{sev.get('CRITICAL', 0)}`")
        md.append(f"- 🟠 **HIGH:** `{sev.get('HIGH', 0)}`")
        md.append(f"- 🟡 **MEDIUM:** `{sev.get('MEDIUM', 0)}`")
        md.append(f"- 🔵 **LOW:** `{sev.get('LOW', 0)}`")
        md.append("\n---\n")

        # Remediation Roadmap
        md.append("## 📅 Prioritized Remediation Roadmap (SLA)\n")
        for phase_key, phase_name in [("phase_1_immediate", "Phase 1: Emergency Fixes (SLA 24-48h)"), 
                                     ("phase_2_shortterm", "Phase 2: High Priority Hardening (SLA 7 days)"), 
                                     ("phase_3_maintenance", "Phase 3: General Maintenance (SLA 30 days)")]:
            p_data = roadmap.get(phase_key, {})
            md.append(f"### 🎯 {phase_name} ({p_data.get('count', 0)} items)")
            for item in p_data.get("items", []):
                md.append(f"- **`[{item.get('severity')}]` [{item.get('finding_id')}]** `{item.get('title')}` — *{item.get('file')}*")
            md.append("")

        md.append("---\n")

        # Detailed Findings Table
        md.append("## 🔍 Detailed Security Findings\n")
        for f in findings:
            md.append(f"### [{f.get('finding_id')}] {f.get('title')}")
            md.append(f"- **Severity:** `{f.get('severity')}` | **Engine:** `{f.get('engine')}` | **Category:** `{f.get('category')}`")
            md.append(f"- **File:** `{f.get('location', {}).get('file_path')}` (Line: `{f.get('location', {}).get('start_line', 1)}`)")
            owasp_str = ", ".join(f.get("standard_mapping", {}).get("owasp_top10_2021", []))
            cwe_str = ", ".join(f.get("standard_mapping", {}).get("cwe", []))
            md.append(f"- **Standard Mapping:** {owasp_str} | {cwe_str}")
            md.append("\n**Evidence Code Snippet:**")
            md.append("```python")
            md.append(f"{f.get('evidence', {}).get('code_snippet', '# No snippet')}")
            md.append("```")
            md.append(f"\n💡 **Remediation:** {f.get('remediation', {}).get('summary')}\n")
            md.append("---\n")

        return "\n".join(md)

    def build_html_report(self, project_info, findings_data, risk_data):
        """Build Rich Standalone HTML Executive Dashboard."""
        risk_scoring = risk_data.get("risk_scoring", {})
        roadmap = risk_data.get("remediation_roadmap", {})
        findings = findings_data.get("findings", [])
        sev = risk_scoring.get("severity_counts", {})
        score = risk_scoring.get('security_score', 0)
        grade = risk_scoring.get('grade', 'F')

        # Color badges
        score_color = "#ef4444" if score < 50 else ("#f59e0b" if score < 75 else "#10b981")

        html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASRP Security Review Report — {self.project_id.upper()}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-card: #1e293b;
            --bg-card-hover: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --accent-red: #ef4444;
            --accent-orange: #f97316;
            --accent-yellow: #eab308;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            padding: 2rem;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Header */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-logo {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 20px;
        }}

        .brand-title h1 {{
            font-size: 1.5rem;
            font-weight: 700;
        }}

        .brand-title p {{
            color: var(--text-muted);
            font-size: 0.875rem;
        }}

        .status-badge {{
            background: rgba(239, 68, 68, 0.2);
            color: var(--accent-red);
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            border: 1px solid var(--accent-red);
            font-size: 0.875rem;
        }}

        /* Hero Scorecard */
        .hero-grid {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 1.5rem;
        }}

        .score-card {{
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .score-ring {{
            width: 130px;
            height: 130px;
            border-radius: 50%;
            border: 8px solid {score_color};
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            margin: 1rem 0;
        }}

        .score-val {{
            font-size: 2.2rem;
            font-weight: 800;
            color: {score_color};
        }}

        .score-grade {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-muted);
        }}

        /* Metrics Cards */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }}

        .metric-box {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }}

        .metric-val {{
            font-size: 1.8rem;
            font-weight: 800;
            margin-top: 4px;
        }}

        .val-critical {{ color: var(--accent-red); }}
        .val-high {{ color: var(--accent-orange); }}
        .val-medium {{ color: var(--accent-yellow); }}
        .val-low {{ color: var(--accent-blue); }}

        /* Sections */
        .section-title {{
            font-size: 1.25rem;
            font-weight: 700;
            margin: 2rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* SLA Roadmap */
        .sla-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
        }}

        .sla-card {{
            border-top: 4px solid var(--border-color);
        }}

        .sla-p1 {{ border-top-color: var(--accent-red); }}
        .sla-p2 {{ border-top-color: var(--accent-orange); }}
        .sla-p3 {{ border-top-color: var(--accent-blue); }}

        .sla-title {{
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 4px;
        }}

        .sla-time {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 12px;
        }}

        /* Findings List */
        .finding-item {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            margin-bottom: 1rem;
            overflow: hidden;
        }}

        .finding-header {{
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.8);
            border-bottom: 1px solid var(--border-color);
        }}

        .finding-title-group {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .badge-sev {{
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
        }}

        .sev-CRITICAL {{ background: rgba(239, 68, 68, 0.2); color: var(--accent-red); border: 1px solid var(--accent-red); }}
        .sev-HIGH {{ background: rgba(249, 115, 22, 0.2); color: var(--accent-orange); border: 1px solid var(--accent-orange); }}
        .sev-MEDIUM {{ background: rgba(234, 179, 8, 0.2); color: var(--accent-yellow); border: 1px solid var(--accent-yellow); }}

        .finding-body {{
            padding: 1.5rem;
        }}

        .finding-meta {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }}

        .code-box {{
            background: #090d16;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.85rem;
            color: #38bdf8;
            margin: 1rem 0;
            white-space: pre-wrap;
            overflow-x: auto;
        }}

        .remediation-box {{
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 8px;
            padding: 1rem;
            color: #6ee7b7;
            font-size: 0.875rem;
        }}

        footer {{
            text-align: center;
            padding: 2rem 0;
            color: var(--text-muted);
            font-size: 0.85rem;
            border-top: 1px solid var(--border-color);
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="brand">
                <div class="brand-logo">🛡️</div>
                <div class="brand-title">
                    <h1>ASRP Security Review Report</h1>
                    <p>Project: <strong>{project_info.get('name', self.project_id)}</strong> | Run ID: {self.run_id}</p>
                </div>
            </div>
            <div class="status-badge">{risk_scoring.get('status', 'ACTION REQUIRED')}</div>
        </header>

        <!-- Hero Section -->
        <div class="hero-grid">
            <div class="card score-card">
                <p style="color: var(--text-muted); font-size: 0.875rem; font-weight: 600;">SECURITY HEALTH SCORE</p>
                <div class="score-ring">
                    <span class="score-val">{score}</span>
                    <span class="score-grade">GRADE {grade}</span>
                </div>
                <p style="font-weight: 700; font-size: 0.9rem; color: {score_color};">{risk_scoring.get('rating')}</p>
            </div>

            <div class="card">
                <h3 style="margin-bottom: 1rem; font-weight: 700;">Findings Summary</h3>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">CRITICAL</p>
                        <p class="metric-val val-critical">{sev.get('CRITICAL', 0)}</p>
                    </div>
                    <div class="metric-box">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">HIGH</p>
                        <p class="metric-val val-high">{sev.get('HIGH', 0)}</p>
                    </div>
                    <div class="metric-box">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">MEDIUM</p>
                        <p class="metric-val val-medium">{sev.get('MEDIUM', 0)}</p>
                    </div>
                    <div class="metric-box">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">TOTAL</p>
                        <p class="metric-val" style="color: var(--text-main);">{findings_data.get('total_findings', 0)}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLA Roadmap -->
        <h2 class="section-title">📅 Prioritized Remediation Roadmap (SLA)</h2>
        <div class="sla-grid">
            <div class="card sla-card sla-p1">
                <div class="sla-title">Phase 1: Emergency Fixes</div>
                <div class="sla-time">SLA: 24h - 48h | Items: {roadmap.get('phase_1_immediate', {}).get('count', 0)}</div>
                <p style="font-size: 0.85rem; color: var(--text-muted);">Tất cả lỗ hổng Secrets, SQL Injection & BOLA khẩn cấp.</p>
            </div>
            <div class="card sla-card sla-p2">
                <div class="sla-title">Phase 2: High Priority Hardening</div>
                <div class="sla-time">SLA: 7 Days | Items: {roadmap.get('phase_2_shortterm', {}).get('count', 0)}</div>
                <p style="font-size: 0.85rem; color: var(--text-muted);">Các lỗi High SAST & Thư viện phụ thuộc CVEs.</p>
            </div>
            <div class="card sla-card sla-p3">
                <div class="sla-title">Phase 3: General Maintenance</div>
                <div class="sla-time">SLA: 30 Days | Items: {roadmap.get('phase_3_maintenance', {}).get('count', 0)}</div>
                <p style="font-size: 0.85rem; color: var(--text-muted);">Các lỗi cấu hình Medium & Low Best Practices.</p>
            </div>
        </div>

        <!-- Detailed Findings -->
        <h2 class="section-title">🔍 Detailed Security Findings ({len(findings)})</h2>
        """

        # Append HTML finding items
        for f in findings:
            sev_class = f"sev-{f.get('severity', 'MEDIUM')}"
            owasp_str = ", ".join(f.get("standard_mapping", {}).get("owasp_top10_2021", []))
            cwe_str = ", ".join(f.get("standard_mapping", {}).get("cwe", []))
            
            html_template += f"""
        <div class="finding-item">
            <div class="finding-header">
                <div class="finding-title-group">
                    <span class="badge-sev {sev_class}">{f.get('severity')}</span>
                    <strong style="font-size: 1rem;">[{f.get('finding_id')}] {f.get('title')}</strong>
                </div>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Engine: {f.get('engine')}</span>
            </div>
            <div class="finding-body">
                <div class="finding-meta">
                    <div>📍 <strong>File:</strong> {f.get('location', {}).get('file_path')} (Line {f.get('location', {}).get('start_line', 1)})</div>
                    <div>🏷️ <strong>Category:</strong> {f.get('category')}</div>
                    <div>🛡️ <strong>Mapping:</strong> {owasp_str} ({cwe_str})</div>
                </div>
                <p style="font-size: 0.875rem; color: var(--text-muted);"><strong>Evidence Code Snippet:</strong></p>
                <div class="code-box">{f.get('evidence', {}).get('code_snippet', '# No code snippet')}</div>
                <div class="remediation-box">
                    💡 <strong>Remediation Guidance:</strong> {f.get('remediation', {}).get('summary')}
                </div>
            </div>
        </div>
        """

        html_template += f"""
        <footer>
            <p>Generated automatically by Application Security Review Platform (ASRP) Layer 5 Report Generator</p>
            <p>Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>
"""
        return html_template

    def run(self):
        """Execute Report Generator and output HTML & Markdown reports."""
        findings_file = os.path.join(self.target_run_dir, "findings.json")
        risk_file = os.path.join(self.target_run_dir, "risk_assessment.json")
        project_file = os.path.join(self.project_dir, "project.yaml")

        findings_data = load_json(findings_file)
        risk_data = load_json(risk_file)
        project_data = load_yaml(project_file) or {}

        if not findings_data or not risk_data:
            raise FileNotFoundError(f"Missing findings.json or risk_assessment.json in {self.target_run_dir}. Run Layer 3 first.")

        project_info = project_data.get("project", {})

        print(f"\n=======================================================")
        print(f"📊 STARTING LAYER 5 REPORT GENERATOR")
        print(f"📌 Project: {self.project_id} | Run ID: {self.run_id}")
        print(f"=======================================================\n")

        # 1. Generate Markdown Report
        md_content = self.build_markdown_report(project_info, findings_data, risk_data)
        md_path = os.path.join(self.target_run_dir, "security_review_report.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"[✓] Markdown Report generated: {md_path}")

        # 2. Generate HTML Report
        html_content = self.build_html_report(project_info, findings_data, risk_data)
        html_path = os.path.join(self.target_run_dir, "security_review_report.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[✓] Executive HTML Dashboard generated: {html_path}")

        print(f"\n=======================================================")
        print(f"🎉 SUCCESS: Reports generated successfully!")
        print(f"📍 HTML Report : {html_path}")
        print(f"📍 MD Report   : {md_path}")
        print(f"=======================================================\n")
        return html_path, md_path


def main():
    parser = argparse.ArgumentParser(description="ASRP Layer 5 Report Generator CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID")
    parser.add_argument("--run-id", default=None, help="Target run ID (defaults to latest)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    generator = ReportGenerator(workspace_root, project_id=args.project, run_id=args.run_id)
    generator.run()


if __name__ == "__main__":
    main()
