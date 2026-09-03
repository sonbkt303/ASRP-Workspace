# Step 3 — Risk Assessment & Executive Reporting (Layer 3.7 & Layer 5)

Calculate risk metrics and generate HTML/MD security reports from scan outputs.

## Paths

| Resource | Path |
|----------|------|
| Run directory | `1. Projects Registry/{project_id}/runs/{run_id}/` |
| Findings | `runs/{run_id}/findings.json` |
| Stage outputs | `runs/{run_id}/stage_outputs/*.json` (reference; unified view uses `findings[].stage_refs`) |
| Risk output | `runs/{run_id}/risk_assessment.json` |
| HTML templates | `1. Projects Registry/1.1 Template/reports/` |

## CLI (preferred)

```bash
python asrp.py report --project {project_id} --run-id {run_id}
python asrp.py validate --project {project_id} --stage report --run-id {run_id}
```

Pipeline: `findings_normalizer.py` → `risk_assessor.py` → `report_generator.py` → report validation.

Pre-check: Step 2 `validate --stage scan` (skip with `--skip-scan-validate` on `asrp.py report`).

## Inputs

1. `findings.json` (from Step 2; enriched with `components_summary` after normalizer + risk assessor)
2. Layer 1: `context.yaml`, `project.yaml`, `technologies.yaml`, `components.yaml`

## Procedure

### 1. Risk assessment (Layer 3.7)

`risk_assessor.py` uses shared `risk_scoring.py`:

| Severity | Deduction |
|----------|-----------|
| CRITICAL | -25 |
| HIGH | -10 |
| MEDIUM | -5 |
| LOW | -2 |

Risk tier multiplier: critical 1.3, high 1.2, medium 1.0, low 0.8.

**Grades:** A 90–100, B 80–89, C 70–79, D 50–69, F <50.

Outputs: `risk_assessment.json` (project + `component_scores`); syncs `findings.json` `components_summary`.

### 2. Report generation (Layer 5)

`report_generator.py` — template placeholder replacement only.

**Outputs:** executive + per-component `.html` / `.md`.

### 3. Interactive stage pills (all 12 modules)

Pill counts = findings with matching `stage_refs`. Cards use `data-stages="{space-separated stage_refs}"`.

## Definition of Done

- [ ] `risk_assessment.json` with project + per-component scores
- [ ] `components_summary` has `health_score`, `grade`, `findings_count`, `tech_stack`
- [ ] All report files exist; no unresolved `{{PLACEHOLDER}}` in HTML
- [ ] `validate --stage report` PASS

## Abort if

- `findings.json` missing
- Step 2 scan validation fails (unless `--skip-scan-validate`)
- Report validation fails

## Summary

Emit Step 3 summary per [summary-format.md](summary-format.md).
