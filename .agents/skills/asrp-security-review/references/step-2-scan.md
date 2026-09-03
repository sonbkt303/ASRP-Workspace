# Step 2 — AI-Primary Security Scan (Layer 3.4 & 3.6)

AI-driven contextual audit with 12 Layer 2 stage outputs and consolidated findings.

## Paths

| Resource | Path |
|----------|------|
| Source | `clones/{project_id}/{component_id}/` |
| Stage outputs | `runs/{run_id}/stage_outputs/` |
| Findings | `runs/{run_id}/findings.json` |
| Raw tool output | `runs/{run_id}/raw_outputs/{component_id}/` |
| Resolved rules | `runs/{run_id}/resolved-rules.json` |
| Scan context | `runs/{run_id}/scan_context.json` |
| Stage schema | [stage-output.schema.json](stage-output.schema.json) |
| Findings schema | [findings.schema.json](findings.schema.json) |
| Example stage | [examples/stage_2_3_rules.example.json](examples/stage_2_3_rules.example.json) |

## CRITICAL INVARIANT

AI Agent MUST act as the Primary Security Audit Engine — direct contextual code analysis on actual clones. AI MUST NOT use `python asrp.py scan` alone as the sole audit. AI writes all 12 stage JSON files; CLI tools are auxiliary only.

## Stage overlap vs consolidation

Two data layers with different duplicate policies:

| Artifact | Role | Duplicate policy |
|----------|------|------------------|
| `stage_outputs/stage_2_*.json` | Catalog evaluation per Layer 2 module | Same vuln **may** FAIL in multiple stages with **different catalog `item_id`** |
| `findings.json` | Consolidated unique issues | One real vuln = one finding; dedupe via `finding_id` + `stage_refs[]` / `stage_item_ids[]` |

**Legitimate cross-mapping** — same hardcoded secret FAIL at:

- 2.1 → `item_id: V2.10.3` (ASVS)
- 2.2 → `item_id: secrets_management` (domain)
- 2.3 → `item_id: ASRP-SEC-001` (rule)
- 2.4 → `item_id: CHK-AUTH-004` (checklist)

→ One entry in `findings.json` with `stage_refs: ["2.1","2.2","2.3","2.4"]` and matching `stage_item_ids`.

**Anti-pattern (FAIL validator):** Copy 7 findings with `FND-*` item_ids into all 12 stage files with identical `results[]` blobs.

**Do NOT** copy `findings.json` entries into stage files. Evaluate catalogs first, then consolidate.

## Phased protocol

Execute in order. In `execution_mode: interactive`, one phase per turn with checkpoint.

### Phase 2A — Pre-flight

1. **Validate gate** — Confirm `registry.manifest.yaml` → `lifecycle_status == validated`. Run `python asrp.py validate --project {project_id}`. Abort if not validated.
2. **Load Layer 1 matrix** — Read `scan_context.json` (preferred). It aggregates:
   - `components[]` — scan_paths, exclude_paths, clone_path
   - `technologies[]` — per-component language, framework, rule_set_ids
   - `context` — risk_tier, business, compliance, PII
   - `assessment` — standards, security_domains, tools_enabled, ai.focus_domains, severity_threshold
   - `resolved_rules_by_component` — rule IDs for stage 2.3
3. **Verify Layer 2 minimum** — Confirm catalogs exist for modules 2.1 (Standards), 2.2 (Domains), 2.3 (Rule Library), 2.4 (Checklists).
4. **Optional CLI** — Run `rule_resolver.py` → `resolved-rules.json` + `scan_context.json`; optionally `scanner_orchestrator.py` → `raw_outputs/` (native tools preferred; `--allow-emulated` for dev only).

### Phase 2B — Per-component audit

For each component in scope (from `components.yaml` or `--component`):

1. Scope to `clones/{project_id}/{component_id}/` with exclusions from [exclusion-paths.md](exclusion-paths.md).
2. Use `scan_context.json` components block for `scan_paths`, `exclude_paths`, `clone_path`.
3. Weight findings using `context.yaml` — e.g. HIPAA/PII when `risk_tier: critical`.
4. Deep discovery: `src/`, `apps/`, `libs/`, `packages/`, `services/`, `controllers/`, `dockerfiles/`, `k8s/`.
5. Read stack-aligned source (`.ts`, `.js`, `.py`, config YAML, framework decorators).
6. **Optional auxiliary** — Cross-verify raw tool hits from `raw_outputs/{component_id}/` against contextual analysis.

### Phase 2C — Stage JSON generation (catalog-driven)

Write 12 files to `runs/{run_id}/stage_outputs/` complying with [stage-output.schema.json](stage-output.schema.json):

| File | Module | Tier | Catalog source | `item_id` namespace |
|------|--------|------|----------------|---------------------|
| `stage_2_3_rules.json` | 2.3 Rule Library | P0 | `resolved-rules.json` | `ASRP-*` |
| `stage_2_4_checklists.json` | 2.4 Review Checklists | P0 | 2.4 index + checklist YAMLs | `CHK-*` |
| `stage_2_1_standards.json` | 2.1 Security Standards | P0 | `assessment.standards` modules | `V*`, CWE refs |
| `stage_2_2_domains.json` | 2.2 Security Domains | P0 | `assessment.security_domains` | domain codes |
| `stage_2_6_threats.json` | 2.6 Threat Models | P1 | 2.6 index | module IDs |
| `stage_2_7_guidelines.json` | 2.7 Secure Coding Guidelines | P1 | 2.7 index | module IDs |
| `stage_2_9_attack_patterns.json` | 2.9 Attack Patterns | P1 | 2.9 index | module IDs |
| `stage_2_10_remediations.json` | 2.10 Remediation Guides | P1 | 2.10 index | `REM-*` |
| `stage_2_5_playbooks.json` | 2.5 Playbooks | P2 | 2.5 index | module IDs |
| `stage_2_8_best_practices.json` | 2.8 Best Practices | P2 | 2.8 index | module IDs |
| `stage_2_11_case_studies.json` | 2.11 Case Studies | P2 | 2.11 index | module IDs |
| `stage_2_12_decision_logs.json` | 2.12 Decision Logs | P2 | 2.12 index | decision IDs |

**Workflow per vulnerability:**
1. Discover issue once during Phase 2B audit.
2. For each applicable stage catalog, emit FAIL/PASS with **that stage's catalog `item_id`**.
3. Include PASS items — P0 stages must not be FAIL-only (incomplete catalog run).

Generate P0 before P1/P2. Each file: `stage_id`, `layer_module_ref`, `summary`, `results[]` with `item_id`, `status`, `evidence`, `standard_mappings`, `remediation`.

Golden examples: [examples/stage_2_1_standards.example.json](examples/stage_2_1_standards.example.json), [examples/stage_2_2_domains.example.json](examples/stage_2_2_domains.example.json), [examples/stage_2_4_checklists.example.json](examples/stage_2_4_checklists.example.json).

### Phase 2D — Consolidation

1. Cross-verify raw tool findings against AI contextual analysis.
2. Eliminate false positives and **deduplicate into `findings.json`** (not by copying stages).
3. Consolidate **100%** of non-PASS items (`FAIL`, `WARNING`, `TRIGGERED`, `CONFIRMED`, `REQUIRES_FIX`) from all 12 stages into `findings.json`.
4. Every finding MUST include:
   - `rule_id` (Layer 2.3)
   - `security_domain` (Layer 2.2)
   - `standard_mapping` with CWE, OWASP Top 10 2021, ASVS v4 where applicable
   - `review_checklist_ref` (Layer 2.4)
   - `stage_refs[]` and `stage_item_ids[]` for traceability (catalog IDs from each mapped stage)
5. Optional CLI assist — `findings_normalizer.py` merges **supplementary** raw tool hits into existing AI `findings.json` (dedupe by rule_id+location; respects `severity_threshold`; adds `components_summary`).

Self-audit: count non-PASS in stage files vs findings mapped — zero omission.

**Mandatory validation:**
```bash
python asrp.py validate --project {project_id} --stage scan --run-id {run_id}
# Production / CI strict gate (fail on stale profile or emulated-only raw outputs):
python asrp.py validate --project {project_id} --stage scan --run-id {run_id} --strict
```

## Tooling matrix

| Task | Owner | Module |
|------|-------|--------|
| Rule resolution | CLI recommended | `rule_resolver.py` → `resolved-rules.json`, `scan_context.json` |
| Static scan evidence | CLI optional | `scanner_orchestrator.py` (per-component clone root; `--allow-emulated` dev only) |
| Contextual code audit | **AI mandatory** | Read clones |
| 12 stage JSON | **AI mandatory** | Write `stage_outputs/` |
| Scan validation | CLI mandatory | `scan_validator.py` via `asrp.py validate --stage scan` |
| Findings normalize | AI primary; CLI assist | `findings_normalizer.py` (supplementary raw hits only) |
| Full pipeline shortcut | **Forbidden** | `python asrp.py scan` as sole audit |

## Definition of Done

- [ ] 12/12 `stage_outputs/stage_2_*.json` exist and match schema
- [ ] `findings.json` exists with full traceability fields
- [ ] 100% non-PASS stage items consolidated (zero omission)
- [ ] `python asrp.py validate --stage scan --run-id {run_id}` PASS
- [ ] Summary table emitted per [summary-format.md](summary-format.md)

## Abort if

- Validate gate fails (`lifecycle_status != validated`)
- Layer 2 minimum catalogs (2.1–2.4) missing
- No clone source for target component
- Scan validation fails (copy-paste stages, `FND-*` in stage item_ids, consolidation gaps)

## Summary

Emit Step 2 summary per [summary-format.md](summary-format.md).

## Re-scan path (fix failed validation)

When `validate --stage scan` FAILs on an existing run (e.g. copy-paste stages):

1. Keep the run folder or create a new `run_id`.
2. Re-run Phase 2B audit on clones (do not copy old stage files).
3. Regenerate stage JSON **catalog-driven** — use golden examples in `references/examples/` as templates.
4. Consolidate into `findings.json` with proper `stage_refs` / `stage_item_ids` (catalog IDs, not `FND-*` in stages).
5. Validate: `python asrp.py validate --project {project_id} --stage scan --run-id {run_id}`

Optional CLI refresh before re-scan:

```bash
python rule_resolver.py --project {project_id} --run-id {run_id}
python scanner_orchestrator.py --project {project_id} --run-id {run_id}
```

