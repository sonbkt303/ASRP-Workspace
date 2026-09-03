"""
Shared risk scoring utilities (Layer 3.7).
Canonical deductions and grades per step-3-report.md.
"""

from __future__ import annotations

SEVERITY_DEDUCTIONS = {
    "CRITICAL": 25,
    "HIGH": 10,
    "MEDIUM": 5,
    "LOW": 2,
    "INFO": 0,
}

RISK_TIER_MULTIPLIERS = {
    "critical": 1.3,
    "high": 1.2,
    "medium": 1.0,
    "low": 0.8,
}


def severity_counts_from_findings(findings: list) -> dict[str, int]:
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    for f in findings:
        sev = str(f.get("severity", "")).upper()
        if sev in counts:
            counts[sev] += 1
    return counts


def calculate_security_score(
    severity_counts: dict,
    risk_tier: str = "high",
    *,
    apply_multiplier: bool = True,
) -> dict:
    """Return score, grade, rating, status, and deduction metadata."""
    multiplier = RISK_TIER_MULTIPLIERS.get(str(risk_tier).lower(), 1.0) if apply_multiplier else 1.0

    deduction = sum(
        severity_counts.get(sev, 0) * pts for sev, pts in SEVERITY_DEDUCTIONS.items()
    )
    if apply_multiplier:
        deduction *= multiplier

    final_score = max(0, min(100, round(100 - deduction)))

    if final_score >= 90:
        grade, rating, status = "A", "EXCELLENT / LOW RISK", "PASS"
    elif final_score >= 80:
        grade, rating, status = "B", "GOOD / MEDIUM RISK", "PASS WITH WARNINGS"
    elif final_score >= 70:
        grade, rating, status = "C", "NEEDS IMPROVEMENT / HIGH RISK", "CONDITIONAL APPROVAL"
    elif final_score >= 50:
        grade, rating, status = "D", "ACTION REQUIRED / HIGH RISK", "ACTION REQUIRED"
    else:
        grade, rating, status = "F", "FAIL / CRITICAL RISK", "ACTION REQUIRED"

    return {
        "security_score": final_score,
        "grade": grade,
        "rating": rating,
        "status": status,
        "total_deduction": round(deduction, 1),
        "multiplier_applied": multiplier if apply_multiplier else 1.0,
        "severity_counts": dict(severity_counts),
    }
