# Step 2 — AI-Primary Security Scan (Layer 3.4 & 3.6)

AI-driven contextual audit with 12 Layer 2 stage outputs and consolidated findings.

## Paths

| Resource | Path |
|----------|------|
| Source | `clones/{project_id}/{component_id}/` |
| Stage outputs | `runs/{run_id}/stage_outputs/` |
| Findings | `runs/{run_id}/findings.json` |
| Raw tool output | `runs/{run_id}/raw_outputs/` |
| Resolved rules | `runs/{run_id}/resolved-rules.json` |
| Stage schema | [stage-output.schema.json](stage-output.schema.json) |
| Findings schema | [findings.schema.json](findings.schema.json) |
| Example stage | [examples/stage_2_3_rules.example.json](examples/stage_2_3_rules.example.json) |

## CRITICAL INVARIANT

AI Agent MUST act as the Primary Security Audit Engine — direct contextual code analysis on actual clones. AI MUST NOT use `python asrp.py scan` alone as the sole audit. AI writes all 12 stage JSON files; CLI tools are auxiliary only.

## Phased protocol

Execute in order. In `execution_mode: interactive`, one phase per turn with checkpoint.

### Phase 2A — Pre-flight

1. **Validate gate** — Confirm `registry.manifest.yaml` → `lifecycle_status == validated`. Run `python asrp.py validate --project {project_id}`. Abort if not validated.
2. **Load Layer 1 matrix** — `assessment.yaml`, `technologies.yaml`, `scope.yaml`, `components.yaml`.
3. **Verify Layer 2 minimum** — Confirm catalogs exist for modules 2.1 (Standards), 2.2 (Domains), 2.3 (Rule Library), 2.4 (Checklists). Do not scan empty without checklist/standard references.
4. **Optional CLI** — Run `rule_resolver.py` → `resolved-rules.json`.

### Phase 2B — Per-component audit

For each component in scope (from `components.yaml` or `--component`):

1. Scope to `clones/{project_id}/{component_id}/` with exclusions from [exclusion-paths.md](exclusion-paths.md).
2. Deep discovery: `src/`, `apps/`, `libs/`, `packages/`, `services/`, `controllers/`, `dockerfiles/`, `k8s/`.
3. Read stack-aligned source (`.ts`, `.js`, `.py`, config YAML, framework decorators).
4. **Optional auxiliary** — Run `scanner_orchestrator.py` → `raw_outputs/` for semgrep, gitleaks, trivy evidence.

### Phase 2C — Stage JSON generation

Write 12 files to `runs/{run_id}/stage_outputs/` complying with [stage-output.schema.json](stage-output.schema.json):

| File | Module | Tier |
|------|--------|------|
| `stage_2_3_rules.json` | 2.3 Rule Library | P0 |
| `stage_2_4_checklists.json` | 2.4 Review Checklists | P0 |
| `stage_2_1_standards.json` | 2.1 Security Standards | P0 |
| `stage_2_2_domains.json` | 2.2 Security Domains | P0 |
| `stage_2_6_threats.json` | 2.6 Threat Models | P1 |
| `stage_2_7_guidelines.json` | 2.7 Secure Coding Guidelines | P1 |
| `stage_2_9_attack_patterns.json` | 2.9 Attack Patterns | P1 |
| `stage_2_10_remediations.json` | 2.10 Remediation Guides | P1 |
| `stage_2_5_playbooks.json` | 2.5 Playbooks | P2 |
| `stage_2_8_best_practices.json` | 2.8 Best Practices | P2 |
| `stage_2_11_case_studies.json` | 2.11 Case Studies | P2 |
| `stage_2_12_decision_logs.json` | 2.12 Decision Logs | P2 |

Generate P0 before P1/P2. Each file: `stage_id`, `layer_module_ref`, `summary`, `results[]` with `item_id`, `status`, `evidence`, `standard_mappings`, `remediation`.

### Phase 2D — Consolidation

1. Cross-verify raw tool findings against AI contextual analysis.
2. Eliminate false positives and duplicates.
3. Consolidate **100%** of non-PASS items (`FAIL`, `WARNING`, `TRIGGERED`, `CONFIRMED`, `REQUIRES_FIX`) from all 12 stages into `findings.json`.
4. Every finding MUST include:
   - `rule_id` (Layer 2.3)
   - `security_domain` (Layer 2.2)
   - `standard_mapping` with CWE, OWASP Top 10 2021, ASVS v4 where applicable
   - `review_checklist_ref` (Layer 2.4)
   - `stage_refs[]` and `stage_item_ids[]` for traceability
5. Optional CLI assist — `findings_normalizer.py` after AI enrichment (AI remains primary for logic findings).

Self-audit: count non-PASS in stage files vs findings mapped — zero omission.

## Tooling matrix

| Task | Owner | Module |
|------|-------|--------|
| Rule resolution | CLI recommended | `rule_resolver.py` |
| Static scan evidence | CLI optional | `scanner_orchestrator.py` |
| Contextual code audit | **AI mandatory** | Read clones |
| 12 stage JSON | **AI mandatory** | Write `stage_outputs/` |
| Findings normalize | AI primary; CLI assist | `findings_normalizer.py` |
| Full pipeline shortcut | **Forbidden** | `python asrp.py scan` as sole audit |

## Definition of Done

- [ ] 12/12 `stage_outputs/stage_2_*.json` exist and match schema
- [ ] `findings.json` exists with full traceability fields
- [ ] 100% non-PASS stage items consolidated (zero omission)
- [ ] Summary table emitted per [summary-format.md](summary-format.md)

## Abort if

- Validate gate fails (`lifecycle_status != validated`)
- Layer 2 minimum catalogs (2.1–2.4) missing
- No clone source for target component

## Summary

Emit Step 2 summary per [summary-format.md](summary-format.md).
