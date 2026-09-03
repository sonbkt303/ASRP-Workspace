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
sys.path.append(os.path.join(asrp_dir, "3. Assessment Engine", "3.1 Source Acquisition"))
sys.path.append(os.path.join(asrp_dir, "3. Assessment Engine", "3.4 Rule Evaluation"))
sys.path.append(os.path.join(asrp_dir, "3. Assessment Engine", "3.6 Findings"))
sys.path.append(os.path.join(asrp_dir, "3. Assessment Engine", "3.7 Risk Assessment"))
sys.path.append(os.path.join(asrp_dir, "5. Reporting"))
sys.path.append(os.path.join(asrp_dir, "1. Projects Registry"))

try:
    from source_acquisition import SourceAcquisition
    from rule_resolver import RuleResolver
    from scanner_orchestrator import ScannerOrchestrator
    from findings_normalizer import FindingsNormalizer
    from risk_assessor import RiskAssessor
    from report_generator import ReportGenerator
    from profile_validator import validate_project, sign_off_project
    from scan_validator import validate_scan
    from report_validator import validate_report
except ImportError as e:
    print(f"[!] Critical Import Error: {e}")
    sys.exit(1)


def load_yaml(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def cmd_scan(args):
    """Run full End-to-End 6-step ASRP Security Review Pipeline."""
    project_id = args.project
    print(f"\n=======================================================")
    print(f"🛡️  ASRP END-TO-END SECURITY REVIEW RUNNER")
    print(f"📌 Target Project: {project_id}")
    print(f"📅 Audit Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=======================================================\n")

    # Validate Gate — abort if profile not validated
    print("👉 [Gate] Validating Layer 1 Profile...")
    validate_project(asrp_dir, project_id, stage="gate", exit_on_fail=True)

    # Step 1: Source Acquisition
    print("👉 [Step 1/6] Running Source Acquisition...")
    acquirer = SourceAcquisition(
        script_dir,
        project_id=project_id,
        source_input=args.source if hasattr(args, "source") else None,
        interactive=args.interactive if hasattr(args, "interactive") else False
    )
    acquirer.run()
    run_id = acquirer.run_id
    project_id = acquirer.project_id  # Update project_id if interactive choice was made

    # Step 2: Rule Resolver
    print("\n👉 [Step 2/6] Running Rule Resolver...")
    resolver = RuleResolver(script_dir, project_id=project_id, run_id=run_id)
    resolver.run()

    # Step 3: Scanner Orchestrator
    print("\n👉 [Step 3/6] Running Scanner Orchestrator...")
    orchestrator = ScannerOrchestrator(script_dir, project_id=project_id, run_id=run_id)
    orchestrator.run()

    # Step 4: Findings Normalizer
    print("\n👉 [Step 4/6] Running Findings Normalizer...")
    normalizer = FindingsNormalizer(script_dir, project_id=project_id, run_id=run_id)
    normalizer.run()

    # Step 5: Risk Assessor
    print("\n👉 [Step 5/6] Running Risk Assessor...")
    assessor = RiskAssessor(script_dir, project_id=project_id, run_id=run_id)
    assessor.run()

    # Step 6: Report Generator
    print("\n👉 [Step 6/6] Running Report Generator...")
    generator = ReportGenerator(script_dir, project_id=project_id, run_id=run_id)
    html_path, md_path = generator.run()

    print(f"\n=======================================================")
    print(f"🏆 ALL 6 PIPELINE STEPS COMPLETED SUCCESSFULLY!")
    print(f"🌐 Executive HTML Dashboard: {html_path}")
    print(f"📄 Markdown Report Export  : {md_path}")
    print(f"=======================================================\n")


def _resolve_run_id(project_id, run_id=None):
    """Return explicit run_id or latest run folder containing findings.json."""
    runs_dir = os.path.join(asrp_dir, "1. Projects Registry", project_id, "runs")
    if run_id:
        return run_id
    if not os.path.exists(runs_dir):
        print(f"[X] FAIL: No runs directory for project '{project_id}'")
        sys.exit(1)
    candidates = sorted(
        [f for f in os.listdir(runs_dir) if f.startswith("run-")],
        reverse=True,
    )
    for folder in candidates:
        if os.path.exists(os.path.join(runs_dir, folder, "findings.json")):
            return folder
    if candidates:
        return candidates[0]
    print(f"[X] FAIL: No run folders under {runs_dir}")
    sys.exit(1)


def cmd_report(args):
    """Run Step 3: normalizer → risk assessor → report generator → validate."""
    project_id = args.project
    run_id = _resolve_run_id(project_id, args.run_id)

    findings_path = os.path.join(
        asrp_dir, "1. Projects Registry", project_id, "runs", run_id, "findings.json"
    )
    if not os.path.exists(findings_path):
        print(f"[X] FAIL: findings.json missing for run '{run_id}'. Complete Step 2 first.")
        sys.exit(1)

    if not getattr(args, "skip_scan_validate", False):
        print("👉 [Gate] Validating Step 2 scan outputs...")
        validate_scan(asrp_dir, project_id, run_id, exit_on_fail=True)

    print(f"\n👉 [Step 3] Report pipeline for {project_id} / {run_id}")
    print("   [1/3] Findings normalizer (merge + components_summary)...")
    FindingsNormalizer(script_dir, project_id=project_id, run_id=run_id).run()

    print("   [2/3] Risk assessor...")
    RiskAssessor(script_dir, project_id=project_id, run_id=run_id).run()

    print("   [3/3] Report generator...")
    ReportGenerator(script_dir, project_id=project_id, run_id=run_id).run()

    print("👉 [DoD] Validating Step 3 report outputs...")
    validate_report(asrp_dir, project_id, run_id, exit_on_fail=True)

    run_dir = os.path.join(asrp_dir, "1. Projects Registry", project_id, "runs", run_id)
    print(f"\n=======================================================")
    print(f"🏆 STEP 3 REPORT COMPLETE")
    print(f"📍 Run folder: {run_dir}")
    print(f"   • HTML: {os.path.join(run_dir, 'security_review_report.html')}")
    print(f"   • MD  : {os.path.join(run_dir, 'security_review_report.md')}")
    print(f"=======================================================\n")


def cmd_acquire(args):
    """Run standalone 3-step Source Acquisition Flow."""
    acquirer = SourceAcquisition(
        script_dir,
        project_id=args.project,
        source_input=args.source,
        interactive=args.interactive
    )
    acquirer.run()


def cmd_validate(args):
    """Validate Layer 1 profile/gate or Step 2 scan outputs."""
    if args.sign_off:
        if not args.by:
            print("[X] FAIL: --sign-off requires --by \"Name or Role\"")
            sys.exit(1)
        sign_off_project(asrp_dir, args.project, args.by, exit_on_fail=True)
    elif args.stage == "scan":
        if not args.run_id:
            print("[X] FAIL: --stage scan requires --run-id {run_id}")
            sys.exit(1)
        validate_scan(asrp_dir, args.project, args.run_id, exit_on_fail=True, strict=getattr(args, "strict", False))
    elif args.stage == "report":
        if not args.run_id:
            print("[X] FAIL: --stage report requires --run-id {run_id}")
            sys.exit(1)
        validate_report(asrp_dir, args.project, args.run_id, exit_on_fail=True)
    else:
        validate_project(asrp_dir, args.project, stage=args.stage, exit_on_fail=True)


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


def cmd_coverage(args):
    """Calculate platform security coverage percentage against international standards."""
    coverage_path = os.path.join(asrp_dir, "3. Assessment Engine", "3.4 Rule Evaluation", "coverage_analyzer.py")
    if os.path.exists(coverage_path):
        sys.path.append(os.path.dirname(coverage_path))
        from coverage_analyzer import CoverageAnalyzer
        analyzer = CoverageAnalyzer(script_dir)
        analyzer.run(standard=args.standard)
    else:
        print("[X] FAIL: coverage_analyzer.py not found.")


def main():
    parser = argparse.ArgumentParser(
        description="ASRP Central CLI Controller",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Examples:\n"
               "  python asrp.py scan --project cleverdent\n"
               "  python asrp.py validate --project cleverdent\n"
               "  python asrp.py validate --project cleverdent --stage profile\n"
               "  python asrp.py validate --project cleverdent --sign-off --by \"Security Lead\"\n"
               "  python asrp.py validate --project cleverdent --stage scan --run-id run-20260903_103000\n"
               "  python asrp.py report --project cleverdent --run-id run-20260903_134200\n"
               "  python asrp.py validate --project cleverdent --stage report --run-id run-20260903_134200\n"
               "  python asrp.py rules list\n"
               "  python asrp.py coverage --standard asvs-v4\n"
               "  python asrp.py status --project cleverdent\n"
    )
    subparsers = parser.add_subparsers(dest="command", help="ASRP CLI Subcommands")

    # Command: scan
    parser_scan = subparsers.add_parser("scan", help="Run full End-to-End 6-step security review pipeline")
    parser_scan.add_argument("--project", default="cleverdent", help="Target project ID in Projects Registry")
    parser_scan.add_argument("--source", default=None, help="Local directory path or Git repository URL")
    parser_scan.add_argument("--interactive", action="store_true", help="Enable interactive project & source prompts")
    parser_scan.set_defaults(func=cmd_scan)

    # Command: acquire
    parser_acq = subparsers.add_parser("acquire", help="Run 3-step Source Acquisition Flow")
    parser_acq.add_argument("--project", default="cleverdent", help="Target project ID")
    parser_acq.add_argument("--source", default=None, help="Local directory path or Git repository URL")
    parser_acq.add_argument("--interactive", action="store_true", help="Enable interactive project & source prompts")
    parser_acq.set_defaults(func=cmd_acquire)

    # Command: validate
    parser_val = subparsers.add_parser(
        "validate",
        help="Validate profile (Step 1) or manifest gate (pre-scan)",
    )
    parser_val.add_argument("--project", default="cleverdent", help="Target project ID")
    parser_val.add_argument(
        "--stage",
        choices=["profile", "gate", "scan", "report"],
        default="gate",
        help="profile = Step 1; gate = pre-scan (default); scan = Step 2; report = Step 3 DoD",
    )
    parser_val.add_argument(
        "--run-id",
        default=None,
        help="Run ID (required when --stage scan or report)",
    )
    parser_val.add_argument(
        "--sign-off",
        action="store_true",
        help="Human gate sign-off: profile check → write manifest → sync lifecycle → gate check",
    )
    parser_val.add_argument(
        "--by",
        default=None,
        help="Sign-off author name/role (required with --sign-off)",
    )
    parser_val.add_argument(
        "--strict",
        action="store_true",
        help="Strict scan validation: fail on stale profile_hash or emulated-only raw outputs",
    )
    parser_val.set_defaults(func=cmd_validate)

    # Command: rules
    parser_rules = subparsers.add_parser("rules", help="Interact with Layer 2 Rule Library")
    rules_sub = parser_rules.add_subparsers(dest="rules_cmd")
    parser_rules_list = rules_sub.add_parser("list", help="List all rules in catalog")
    parser_rules_list.set_defaults(func=cmd_rules_list)

    # Command: coverage
    parser_cov = subparsers.add_parser("coverage", help="Calculate platform security coverage percentage against international standards")
    parser_cov.add_argument("--standard", default="asvs-v4", help="Target security standard (e.g. asvs-v4, cwe-top-25)")
    parser_cov.set_defaults(func=cmd_coverage)

    # Command: status
    parser_status = subparsers.add_parser("status", help="Show project audit status and latest run summary")
    parser_status.add_argument("--project", default="cleverdent", help="Target project ID")
    parser_status.set_defaults(func=cmd_status)

    # Command: report
    parser_report = subparsers.add_parser("report", help="Run Step 3 report pipeline (normalizer → risk → HTML/MD)")
    parser_report.add_argument("--project", default="cleverdent", help="Target project ID")
    parser_report.add_argument("--run-id", default=None, help="Target run ID (defaults to latest with findings.json)")
    parser_report.add_argument(
        "--skip-scan-validate",
        action="store_true",
        help="Skip Step 2 scan validation pre-check",
    )
    parser_report.set_defaults(func=cmd_report)

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

