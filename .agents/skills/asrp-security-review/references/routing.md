# ASRP Skill Routing

Base path prefix: `Application Security Review Platform (ASRP)/`

## Subcommands

| Subcommand | Step | Pre-condition | Primary outputs |
|------------|------|---------------|-----------------|
| `acquire [project_id]` | 0 | Project folder exists or bootstrap from `1.1 Template/` | `clones/{project_id}/{component_id}/`, `runs/{run_id}/acquisition.json` |
| `profile [project_id]` | 1 | Clones exist for target component(s) | 7 schema-valid profile YAMLs; `lifecycle_status: profiled` |
| `validate [project_id]` | Gate | `--stage profile` pass | `--sign-off` → manifest + `lifecycle_status: validated` |
| `scan [project_id]` | 2 | Validate gate PASS | `stage_outputs/*.json`, `findings.json`, `scan_context.json` |
| `report [project_id]` | 3 | `findings.json` exists for run | `risk_assessment.json`, `security_review_report*.html` |
| `review [project_id]` | 0→3 | — | Full pipeline outputs |

## Flags

| Flag | Applies to | Description |
|------|------------|-------------|
| `--component {id}` | profile, scan, report | Limit to one `component_id` from `components.yaml` |
| `--run-id {id}` | scan, report, validate | Use specific run folder |
| `--source {url\|path}` | acquire | Override clone source when not in profile |
| `--stage profile\|gate\|scan\|report` | validate | Step 1 / gate / Step 2 / Step 3 DoD |
| `--strict` | validate (--stage scan) | Fail on stale `manifest_hash` or emulated-only raw outputs |
| `--sign-off --by {name}` | validate | Human gate: write manifest + sync lifecycle |
| `execution_mode: interactive` | all | One phase per turn + `## Checkpoint` |

## CLI equivalents

| Skill subcommand | CLI |
|------------------|-----|
| acquire | `python asrp.py acquire --project {id} [--source URL\|path]` |
| validate (Step 1) | `python asrp.py validate --project {id} --stage profile` |
| validate (sign-off) | `python asrp.py validate --project {id} --sign-off --by "Security Lead"` |
| validate (gate) | `python asrp.py validate --project {id}` |
| validate (Step 2) | `python asrp.py validate --project {id} --stage scan --run-id {run_id} [--strict]` |
| report (Step 3) | `python asrp.py report --project {id} --run-id {run_id}` |
| validate (Step 3) | `python asrp.py validate --project {id} --stage report --run-id {run_id}` |
| scanner | `python scanner_orchestrator.py --project {id} --run-id {run_id} [--allow-emulated]` |
| findings merge | `python findings_normalizer.py --project {id} --run-id {run_id}` |
| rule resolver | `python rule_resolver.py --project {id}` → `resolved-rules.json`, `scan_context.json` |
| report (risk + HTML) | `risk_assessor.py` + `report_generator.py` via workspace root |
| full pipeline shortcut | **Forbidden as sole audit** — `python asrp.py scan` alone |

## Legacy aliases

| Alias | Maps to |
|-------|---------|
| `step 0` | acquire |
| `step 1` / `profile` | profile |
| `step 2` / `scan` | scan |
| `step 3` / `report` | report |
| `full` / `review` (default) | review (0→validate→1→2→3) |

## Full workflow order

```
acquire → profile → validate (gate) → scan → report
```

Do not run `scan` before validate gate passes.
