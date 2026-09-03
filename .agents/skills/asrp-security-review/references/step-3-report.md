# Step 3 — Risk Assessment & Executive Reporting (Layer 3.7 & Layer 5)

Calculate risk metrics and generate HTML/MD security reports from scan outputs.

## Paths

| Resource | Path |
|----------|------|
| Run directory | `1. Projects Registry/{project_id}/runs/{run_id}/` |
| Findings | `runs/{run_id}/findings.json` |
| Stage outputs | `runs/{run_id}/stage_outputs/*.json` |
| Risk output | `runs/{run_id}/risk_assessment.json` |
| HTML templates | `1. Projects Registry/1.1 Template/reports/` |
| Template docs | `1.1 Template/reports/README.md` |

## Inputs

1. `findings.json` (from Step 2)
2. All `stage_outputs/*.json` (12 files)
3. Layer 1 context: `context.yaml`, `project.yaml`, `architecture.yaml`, `components.yaml`

## Procedure

### 1. Risk assessment (Layer 3.7)

Prefer deterministic CLI: `risk_assessor.py` from workspace root with `--project` and `--run-id`.

**Health score (0–100):** Start at 100, deduct by severity:

| Severity | Deduction |
|----------|-----------|
| CRITICAL | -25 |
| HIGH | -10 |
| MEDIUM | -5 |
| LOW | -2 |

**Grade assignment:**

| Grade | Score | Status |
|-------|-------|--------|
| A | 90–100 | Pass |
| B | 80–89 | Pass |
| C | 70–79 | Conditional |
| D | 50–69 | Action Required |
| F | < 50 | Fail / Critical Risk |

**Gate status:** `PASSED` or `ACTION REQUIRED`.

**SLA remediation roadmap:**

- **Phase 1 (24–48h):** Critical & High — secrets, RCE, injection
- **Phase 2 (7d):** High — access control, dependency flaws
- **Phase 3 (30d):** Medium — misconfigurations

Save to `runs/{run_id}/risk_assessment.json`.

### 2. Report generation (Layer 5)

Prefer `report_generator.py` from workspace root. **NO INLINE HTML** — read templates from disk and perform placeholder replacement only.

**Templates:**

- `executive_dashboard.html` → project-wide dashboard
- `component_report.html` → per-component detail

**Outputs:**

| Report | Path |
|--------|------|
| Executive dashboard | `security_review_report.html`, `security_review_report.md` |
| Per component | `security_review_report_{component_id}.html`, `.md` |

### 3. Interactive stage pills (all 12 modules)

Reports MUST support click-to-filter for every Layer 2 stage:

- 2.1 Security Standards
- 2.2 Security Domains
- 2.3 Rule Library
- 2.4 Review Checklists
- 2.5 Playbooks
- 2.6 Threat Models
- 2.7 Secure Coding Guidelines
- 2.8 Best Practices
- 2.9 Attack Patterns
- 2.10 Remediation Guides
- 2.11 Case Studies
- 2.12 Decision Logs

Filter pill counts MUST match findings tagged with each `stage_refs` value.

## Definition of Done

- [ ] `risk_assessment.json` exists with health score, grade, gate status, SLA phases
- [ ] `security_review_report.html` and `.md` exist
- [ ] Per-component reports exist for each entry in `components.yaml`
- [ ] All reports use template files (no inline HTML scaffolding)
- [ ] Executive summary table with clickable report links emitted

## Abort if

- `findings.json` missing for target `run_id`
- Stage outputs missing (re-run Step 2 or specify complete run)

## Summary

Emit Step 3 summary per [summary-format.md](summary-format.md).
