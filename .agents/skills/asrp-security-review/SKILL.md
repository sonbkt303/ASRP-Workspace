---
name: asrp-security-review
description: >-
  Runs ASRP security review (acquire → profile → validate → scan → report)
  for a Projects Registry project_id. Use when auditing, scanning, profiling,
  or generating findings.json / executive HTML security reports; or when the
  user mentions /asrp-security-review, Layer 1 registry, or ASRP assessment.
---

# ASRP Security Review

## What this skill does

End-to-end Application Security Review for ASRP: clone source → auto-profile Layer 1 YAML → validate gate → AI-primary scan with 12 Layer 2 stage outputs → risk score → executive HTML/MD reports.

Project invariants: [`.agents/AGENTS.md`](../../AGENTS.md). This skill is the operational runbook.

## How to invoke

- `@asrp-security-review` in Cursor chat, or
- `/asrp-security-review [subcommand] [project_id]`

Optional prompt fields: `--component`, `--run-id`, `--source`, `execution_mode: interactive`.

Full routing: [`references/routing.md`](references/routing.md).

## Skill routing

| Subcommand | Step | Pre-condition |
|------------|------|---------------|
| `acquire` | 0 | Project exists or bootstrap from `1.1 Template/` |
| `profile` | 1 | Clones exist |
| `validate` | Gate | 7 profile YAMLs schema-valid |
| `scan` | 2 | `lifecycle_status == validated` |
| `report` | 3 | `findings.json` exists for run |
| `review` | 0→3 | Full pipeline |

Legacy: `step 0`–`step 3`, `full` / default → `review`.

## Global invariants

1. **AI-Primary audit** — Do not run `python asrp.py scan` alone as the sole audit; AI must read clones and write stage JSON.
2. **Multi-component safe merge** — Never wipe unrelated entries in `components.yaml` / `technologies.yaml`.
3. **Exclude non-source paths** — See [`references/exclusion-paths.md`](references/exclusion-paths.md).
4. **12-stage traceability** — Every finding maps to `rule_id`, `security_domain`, `standard_mapping`, `review_checklist_ref`, `stage_refs[]`.
5. **Template-based reports** — Use `1.1 Template/reports/`; no inline HTML scaffolding.

## Pre-flight

Before Step 0 or Step 1, emit **`## ASRPReviewJob`** fenced YAML per [`references/job-schema.md`](references/job-schema.md).

Required: `project_id`, `subcommand`, `execution_mode` (`batch` default).

## Step 0 — Source Acquisition

Clone/copy source to `3. Assessment Engine/3.1 Source Acquisition/clones/{project_id}/{component_id}/`. Create `runs/{run_id}/acquisition.json`.

Details: [`references/step-0-acquire.md`](references/step-0-acquire.md)

**DoD:** All target components have clones. **Abort if:** no source and no `--source`.

## Gate — Validate Profile

Details: [`references/step-gate-validate.md`](references/step-gate-validate.md)

**Step 1 check (after profile):**
```bash
python asrp.py validate --project {project_id} --stage profile
```

**Human sign-off (creates manifest + syncs lifecycle):**
```bash
python asrp.py validate --project {project_id} --sign-off --by "Security Lead"
```

**Pre-scan gate check (default):**
```bash
python asrp.py validate --project {project_id}   # --stage gate
```

**Lifecycle model:** Step 1 → `project.yaml: profiled`. Sign-off → manifest + `project.yaml: validated`. Gate is authoritative for scan; `project.yaml` mirrors manifest.

**Gate checks (exit 1 on fail):** schema (7 + manifest), cross-file, lifecycle sync, `profile_hash` match.

**Require:** gate PASS before scan. **`asrp.py scan` enforces gate automatically.**

**Abort scan if:** validation fails.

## Step 1 — AI Auto-Profiling (Layer 1)

Inspect clones; update **7 schema-valid profile YAMLs** with safe merge; map `rule_set_ids`; set `exclude_paths` / `scope.exclude`; set `lifecycle_status: profiled`.

Do **not** set `registry.manifest.yaml` → `validated` (Validate Gate only).

Details: [`references/step-1-profile.md`](references/step-1-profile.md) · Snippets: [`references/examples/profile-snippets.yaml`](references/examples/profile-snippets.yaml)

**DoD:** 7 YAMLs pass JSON schema + cross-file checks; `lifecycle_status: profiled`. **Abort if:** clone missing or schema fail after 2 fixes.

## Step 2 — AI-Primary Scan (Layer 3.4 & 3.6)

Phased: **2A** pre-flight → **2B** per-component audit → **2C** 12 stage JSON → **2D** consolidate `findings.json`.

Details: [`references/step-2-scan.md`](references/step-2-scan.md)

Schemas: [`stage-output.schema.json`](references/stage-output.schema.json), [`findings.schema.json`](references/findings.schema.json)

**DoD:** 12/12 stage files; findings with 100% non-PASS coverage. **Abort if:** validate gate fails.

## Step 3 — Risk & Report (Layer 3.7 & 5)

Risk score + HTML/MD reports via `risk_assessor.py` and `report_generator.py`. All 12 stage pills in reports.

Details: [`references/step-3-report.md`](references/step-3-report.md)

**DoD:** `risk_assessment.json` + all report files. **Abort if:** `findings.json` missing.

## Response structure

### Batch (`execution_mode: batch` or omitted)

1. `## ASRPReviewJob` — fenced YAML
2. Execute steps per subcommand (full order: acquire → profile → validate → scan → report)
3. `## Summary` — table per [`references/summary-format.md`](references/summary-format.md)

**Gate:** No step execution until `## ASRPReviewJob` is emitted.

### Interactive (`execution_mode: interactive`)

One phase per turn. After each phase emit:

```markdown
## Checkpoint — Phase {id}
- [x] ...
Proceed? (yes / amend / abort)
```

Resume via updated `phases_completed` in job YAML.

## Tooling matrix

| Task | Owner | Reference |
|------|-------|-----------|
| Clone / pull | CLI optional | step-0-acquire.md |
| Profile YAML | AI | step-1-profile.md |
| Static scan evidence | CLI optional | step-2-scan.md |
| Stage JSON + audit | **AI mandatory** | step-2-scan.md |
| Findings | AI (+ normalizer assist) | findings.schema.json |
| Risk + HTML | CLI preferred | step-3-report.md |
| Full pipeline shortcut | **Forbidden** | `asrp.py scan` as sole audit |

## Canonical references

- [`references/routing.md`](references/routing.md) — subcommands, flags, CLI map
- [`references/job-schema.md`](references/job-schema.md) — ASRPReviewJob YAML
- [`references/step-gate-validate.md`](references/step-gate-validate.md) — Validate Gate sign-off
- [`references/step-0-acquire.md`](references/step-0-acquire.md) through [`step-3-report.md`](references/step-3-report.md)
- [`references/exclusion-paths.md`](references/exclusion-paths.md)
- [`references/summary-format.md`](references/summary-format.md)
- [`references/examples/`](references/examples/) — golden stage, finding JSON, profile snippets
