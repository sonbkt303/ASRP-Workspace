# Step 1 — AI Auto-Profiling (Layer 1)

Read cloned source and generate or update **7 schema-valid profile YAML files** in the Projects Registry.

> **Gate boundary:** Step 1 ends at `lifecycle_status: profiled`. Do **not** set `registry.manifest.yaml` → `lifecycle_status: validated` — that is the **Validate Gate** (human sign-off).

## Paths

| Resource | Path |
|----------|------|
| Clone root | `3. Assessment Engine/3.1 Source Acquisition/clones/{project_id}/` |
| Profile output | `1. Projects Registry/{project_id}/` |
| Template | `1. Projects Registry/1.1 Template/` |
| JSON Schemas | `1. Projects Registry/schema/*.schema.json` |
| Rule set mapping | `2. Security Knowledge Base ⭐ (Core Asset)/2.3 Rule Library/mappings/tech-stack-map.yaml` |
| Standards catalog | `2. Security Knowledge Base ⭐ (Core Asset)/2.1 Security Standards/` |
| Golden snippets | [`examples/profile-snippets.yaml`](examples/profile-snippets.yaml) |

## Output files (7 profile YAMLs)

| Order | File | Schema | Primary owner |
|-------|------|--------|---------------|
| 1 | `project.yaml` | `project.schema.json` | AI |
| 2 | `components.yaml` | `components.schema.json` | AI |
| 3 | `technologies.yaml` | `technologies.schema.json` | AI |
| 4 | `architecture.yaml` | `architecture.schema.json` | AI |
| 5 | `scope.yaml` | `scope.schema.json` | AI draft → **human review** |
| 6 | `context.yaml` | `context.schema.json` | AI draft → **human review** |
| 7 | `assessment.yaml` | `assessment.schema.json` | AI draft → **human review** |

`registry.manifest.yaml` is **not** a Step 1 output — it is created at the Validate Gate after human sign-off.

## Field name contract (canonical)

Use **only** field names defined in `1.1 Template/` and `schema/*.schema.json`. Legacy names are forbidden:

| Forbidden (legacy) | Canonical (schema) | File |
|--------------------|--------------------|------|
| `in_scope_paths` | `include` | `scope.yaml` |
| `out_of_scope_paths` | `exclude` | `scope.yaml` |
| `rule_sets` | `rule_set_ids` | `assessment.yaml` |
| `business_criticality` | — (not in schema) | — |

Exclusions: write to `components[].exclude_paths` **and** mirror in `scope.exclude`.

## Procedure

### Phase 1A — Component discovery

1. Access `clones/{project_id}/`.
2. If `--component` specified → inspect only `clones/{project_id}/{component_id}/`.
3. If entire project → discover all component subdirectories (each maps to one `components[].id`).
4. Derive `scan_paths` per component:
   - **Monorepo:** `apps/*`, `packages/*`, `libs/*` with `package.json` or entrypoint
   - **Single app:** `src/`, `app/`
   - **Skip:** test-only, generated, and vendor dirs (see [exclusion-paths.md](exclusion-paths.md))
5. Populate `exclude_paths` in `components.yaml` and mirror in `scope.exclude`.

### Phase 1B — Deep stack inspection

Inspect structural configuration per stack:

- **Node.js / TypeScript:** `package.json`, `nest-cli.json`, `tsconfig.json`, `pnpm-workspace.yaml`, `biome.json`
- **Python:** `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`
- **Go / Java:** `go.mod`, `pom.xml`, `build.gradle`
- **Docker / Infra:** `docker-compose.yaml`, `Dockerfile`, `k8s/`, `helm/`
- **DB / Storage:** Prisma, TypeORM, Mongoose schemas, Redis connections
- **CI/CD:** `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`

Write results to `technologies.yaml` (per component) and `architecture.yaml` (project-wide).

### Phase 1C — Rule set resolution

1. Detect `language`, `framework`, and infrastructure from clone inspection.
2. Lookup defaults in `2.3 Rule Library/mappings/tech-stack-map.yaml` → `default_rule_sets`.
3. Add domain-specific sets (e.g. REST API → `owasp-api-security-top10`, React → `react-xss-prevention`, Docker → `container-security`).
4. Deduplicate and write:
   - `technologies[].rule_set_ids` — per component
   - `assessment.rule_set_ids` — project-wide union
5. Map human-readable names to `assessment.standards` and OWASP domains to `assessment.security_domains`.

### Phase 1D — Non-destructive merge

Update files in `1. Projects Registry/{project_id}/` following `1.1 Template/` structure.

**CRITICAL SAFE MERGE RULE:** When updating one component (e.g. `dent-api-nestjs`), update or append ONLY its entry in `components.yaml` and `technologies.yaml`. Do not overwrite or wipe other components.

Required fields per file — see [`examples/profile-snippets.yaml`](examples/profile-snippets.yaml).

### Phase 1E — Schema validation and lifecycle

1. Validate all **7 profile files** (manifest is **not** validated in Step 1):

```bash
python asrp.py validate --project {project_id} --stage profile
```

This runs JSON Schema (`check-jsonschema`) on 7 YAMLs, cross-file linkage checks, and verifies `project.yaml` → `lifecycle_status: profiled`. **Exit 1** on any failure.

Manual alternative (requires `pip install check-jsonschema pyyaml`; run from `schema/` so `$ref` resolves):

```bash
PROJECT="cleverdent"
SCHEMA_DIR="Application Security Review Platform (ASRP)/1. Projects Registry/schema"
cd "${SCHEMA_DIR}"
for f in project components technologies architecture scope context assessment; do
  python -m check_jsonschema --schemafile "${f}.schema.json" "../${PROJECT}/${f}.yaml"
done
```

**Date format:** `project.created_at` and `project.updated_at` use `YYYY-MM-DD` (not ISO datetime).

2. Cross-file linkage is enforced automatically by `--stage profile` (same checks as [step-gate-validate.md](step-gate-validate.md)).

3. Set `project.yaml` → `lifecycle_status: profiled` and update `updated_at`.

4. **Do not** create or update `registry.manifest.yaml` — use Validate Gate sign-off: [`step-gate-validate.md`](step-gate-validate.md).

## Re-profile

When re-profiling after `completed` or stack changes:

1. Safe-merge only affected components if `--component` is set.
2. Set `project.yaml` → `lifecycle_status: profiled`.
3. If manifest exists with `validated`, flag in summary: **manifest stale — re-run Validate Gate**.

## Definition of Done

- [ ] All 7 profile YAML files exist and pass JSON schema validation
- [ ] Cross-file linkage checks pass
- [ ] `exclude_paths` (components) and `exclude` (scope) populated
- [ ] `technologies[].rule_set_ids` and `assessment.rule_set_ids` mapped (non-empty)
- [ ] `scope.review_level` set
- [ ] `assessment.tools_enabled` and `severity_threshold` populated
- [ ] Multi-component safe merge verified (no unrelated entries wiped)
- [ ] `project.yaml` → `lifecycle_status: profiled` (not `validated`)

## Abort if

- Clone source missing for target component (run Step 0 first)
- JSON schema validation fails after 2 correction attempts
- No valid `rule_set_id` can be mapped from `tech-stack-map.yaml`
- Cross-file linkage check fails and cannot be corrected

## Interactive mode checkpoints

| Phase | Checkpoint |
|-------|------------|
| 1A | Components discovered, `scan_paths` / `exclude_paths` set |
| 1B | Stack + architecture written |
| 1C | `rule_set_ids` mapped from tech-stack-map |
| 1D | 7 YAML files merged (safe merge verified) |
| 1E | Schema validation pass, `lifecycle_status: profiled` |

## Summary

Emit Step 1 summary per [summary-format.md](summary-format.md).
