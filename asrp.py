#!/usr/bin/env python3
"""
ASRP Central CLI Controller (asrp.py)
=====================================
Unified entry point for the Application Security Review Platform.
Provides easy single-command execution for full End-to-End security reviews,
profile validation, rule listing, and status tracking.
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

# Dynamically import ASRP submodules
script_dir = os.path.dirname(os.path.abspath(__file__))
asrp_dir = os.path.join(script_dir, "Application Security Review Platform (ASRP)")

# Add module paths to sys.path
sys.path.append(os.path.join(asrp_dir, "3. Assessment Engine", "3.4 Rule Evaluation"))
sys.path.append(os.path.join(asrp_dir, "3. Assessment Engine", "3.6 Findings"))
sys.path.append(os.path.join(asrp_dir, "3. Assessment Engine", "3.7 Risk Assessment"))
sys.path.append(os.path.join(asrp_dir, "5. Reporting"))

try:
    from rule_resolver import RuleResolver
    from scanner_orchestrator import ScannerOrchestrator
    from findings_normalizer import FindingsNormalizer
    from risk_assessor import RiskAssessor
    from report_generator import ReportGenerator
except ImportError as e:
    print(f"[!] Critical Import Error: {e}")
    sys.exit(1)


def load_yaml(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def cmd_scan(args):
    """Run full End-to-End 5-step ASRP Security Review Pipeline."""
    project_id = args.project
    print(f"\n=======================================================")
    print(f"🛡️  ASRP END-TO-END SECURITY REVIEW RUNNER")
    print(f"📌 Target Project: {project_id}")
    print(f"📅 Audit Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=======================================================\n")

    # Step 1: Rule Resolver
    print("👉 [Step 1/5] Running Rule Resolver...")
    resolver = RuleResolver(script_dir, project_id=project_id)
    run_output = resolver.run()
    run_id = resolver.run_id

    # Step 2: Scanner Orchestrator
    print("\n👉 [Step 2/5] Running Scanner Orchestrator...")
    orchestrator = ScannerOrchestrator(script_dir, project_id=project_id, run_id=run_id)
    orchestrator.run()

    # Step 3: Findings Normalizer
    print("\n👉 [Step 3/5] Running Findings Normalizer...")
    normalizer = FindingsNormalizer(script_dir, project_id=project_id, run_id=run_id)
    normalizer.run()

    # Step 4: Risk Assessor
    print("\n👉 [Step 4/5] Running Risk Assessor...")
    assessor = RiskAssessor(script_dir, project_id=project_id, run_id=run_id)
    assessor.run()

    # Step 5: Report Generator
    print("\n👉 [Step 5/5] Running Report Generator...")
    generator = ReportGenerator(script_dir, project_id=project_id, run_id=run_id)
    html_path, md_path = generator.run()

    print(f"\n=======================================================")
    print(f"🏆 ALL 5 PIPELINE STEPS COMPLETED SUCCESSFULLY!")
    print(f"🌐 Executive HTML Dashboard: {html_path}")
    print(f"📄 Markdown Report Export  : {md_path}")
    print(f"=======================================================\n")


def cmd_validate(args):
    """Validate Layer 1 Project Profile & Manifest Gate."""
    project_id = args.project
    project_dir = os.path.join(asrp_dir, "1. Projects Registry", project_id)
    manifest_path = os.path.join(project_dir, "registry.manifest.yaml")

    print(f"\n=======================================================")
    print(f"🔎 VALIDATING LAYER 1 PROJECT PROFILE: {project_id}")
    print(f"=======================================================\n")

    if not os.path.exists(manifest_path):
        print(f"[X] FAIL: registry.manifest.yaml not found for project '{project_id}'.")
        sys.exit(1)

    manifest_data = load_yaml(manifest_path).get("registry_manifest", {})
    status = manifest_data.get("lifecycle_status")
    profile_hash = manifest_data.get("profile_hash")

    required_files = [
        "project.yaml", "context.yaml", "scope.yaml",
        "architecture.yaml", "technologies.yaml", "components.yaml", "assessment.yaml"
    ]

    all_exist = True
    for fname in required_files:
        fpath = os.path.join(project_dir, fname)
        if os.path.exists(fpath):
            print(f"  [✓] Found profile file: {fname}")
        else:
            print(f"  [X] Missing profile file: {fname}")
            all_exist = False

    print("\n-------------------------------------------------------")
    print(f"• Human Gate Status : {status}")
    print(f"• Manifest Hash     : {profile_hash}")
    print("-------------------------------------------------------")

    if status == "validated" and all_exist:
        print(f"🎉 PROJECT PROFILE IS VALIDATED AND READY TO SCAN!\n")
    else:
        print(f"[!] WARNING: Project profile is NOT ready. Lifecycle status must be 'validated'.\n")


def cmd_rules_list(args):
    """List all executable rules in Layer 2 Rule Library."""
    rule_lib_dir = os.path.join(asrp_dir, "2. Security Knowledge Base ⭐ (Core Asset)", "2.3 Rule Library")
    index_path = os.path.join(rule_lib_dir, "index.yaml")
    
    if not os.path.exists(index_path):
        print(f"[X] FAIL: Rule Library index.yaml not found at {index_path}")
        sys.exit(1)

    catalog = load_yaml(index_path).get("rule_library", {})
    rules = catalog.get("rules", [])

    print(f"\n=======================================================")
    print(f"📚 ASRP RULE LIBRARY CATALOG ({len(rules)} Executable Rules)")
    print(f"=======================================================\n")

    print(f"{'RULE ID':<16} | {'ENGINE':<10} | {'ENABLED':<8} | {'PATH'}")
    print("-" * 75)

    for r in rules:
        rule_id = r.get("id", "N/A")
        rel_path = r.get("path", "N/A")
        enabled = "Yes" if r.get("enabled", True) else "No"
        
        # Determine engine from path
        engine = rel_path.split("/")[1] if "/" in rel_path else "unknown"
        print(f"{rule_id:<16} | {engine:<10} | {enabled:<8} | {rel_path}")

    print(f"\nTotal Enabled Rules: {len([r for r in rules if r.get('enabled', True)])} / {len(rules)}\n")


def cmd_status(args):
    """Show quick status and summary of latest run."""
    project_id = args.project
    project_dir = os.path.join(asrp_dir, "1. Projects Registry", project_id)
    runs_dir = os.path.join(project_dir, "runs")

    print(f"\n=======================================================")
    print(f"📊 ASRP PROJECT STATUS: {project_id}")
    print(f"=======================================================\n")

    if not os.path.exists(runs_dir):
        print(f"[!] No run history found for project '{project_id}'. Run 'python asrp.py scan --project {project_id}' first.\n")
        return

    run_folders = [f for f in os.listdir(runs_dir) if f.startswith("run-")]
    if not run_folders:
        print(f"[!] No run folders found under {runs_dir}.\n")
        return

    run_folders.sort(reverse=True)
    latest_run = run_folders[0]
    latest_run_dir = os.path.join(runs_dir, latest_run)

    risk_file = os.path.join(latest_run_dir, "risk_assessment.json")
    if os.path.exists(risk_file):
        with open(risk_file, 'r', encoding='utf-8') as f:
            risk_data = json.load(f)
        scoring = risk_data.get("risk_scoring", {})
        print(f"📌 Latest Run ID  : {latest_run}")
        print(f"🎯 Health Score   : {scoring.get('security_score')}/100 (GRADE {scoring.get('grade')})")
        print(f"🏷️  Security Rating: {scoring.get('rating')}")
        print(f"🚨 Gate Status    : {scoring.get('status')}")
        print(f"\n📄 Reports Available:")
        print(f"   • HTML: {os.path.join(latest_run_dir, 'security_review_report.html')}")
        print(f"   • MD  : {os.path.join(latest_run_dir, 'security_review_report.md')}\n")
    else:
        print(f"📌 Latest Run ID: {latest_run} (Incomplete / In progress)\n")


def main():
    parser = argparse.ArgumentParser(
        description="ASRP Central CLI Controller",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Examples:\n"
               "  python asrp.py scan --project cleverdent\n"
               "  python asrp.py validate --project cleverdent\n"
               "  python asrp.py rules list\n"
               "  python asrp.py status --project cleverdent\n"
    )
    subparsers = parser.add_subparsers(dest="command", help="ASRP CLI Subcommands")

    # Command: scan
    parser_scan = subparsers.add_parser("scan", help="Run full End-to-End 5-step security review pipeline")
    parser_scan.add_argument("--project", default="cleverdent", help="Target project ID in Projects Registry")
    parser_scan.set_defaults(func=cmd_scan)

    # Command: validate
    parser_val = subparsers.add_parser("validate", help="Validate project profile YAML files and human gate")
    parser_val.add_argument("--project", default="cleverdent", help="Target project ID")
    parser_val.set_defaults(func=cmd_validate)

    # Command: rules
    parser_rules = subparsers.add_parser("rules", help="Interact with Layer 2 Rule Library")
    rules_sub = parser_rules.add_subparsers(dest="rules_cmd")
    parser_rules_list = rules_sub.add_parser("list", help="List all rules in catalog")
    parser_rules_list.set_defaults(func=cmd_rules_list)

    # Command: status
    parser_status = subparsers.add_parser("status", help="Show project audit status and latest run summary")
    parser_status.add_argument("--project", default="cleverdent", help="Target project ID")
    parser_status.set_defaults(func=cmd_status)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
