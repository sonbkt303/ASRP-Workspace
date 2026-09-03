# Validate Gate — Human Sign-Off (Layer 1)

Human gate between Step 1 (`profiled`) and Step 2 scan (`validated`). Creates or refreshes `registry.manifest.yaml` and syncs lifecycle on `project.yaml`.

> **Lifecycle model:** `project.yaml` mirrors manifest lifecycle. Step 1 sets `profiled`; sign-off sets both to `validated`. Re-profile resets `project.yaml` to `profiled` and flags manifest stale.

## Pre-conditions

- Step 1 complete: 7 profile YAMLs exist
- `python asrp.py validate --project {project_id} --stage profile` passes
- Human reviewed: `scope.yaml`, `context.yaml`, `assessment.yaml`

## Sign-off command

```bash
python asrp.py validate --project {project_id} --sign-off --by "Security Lead"
```

**What it does:**

1. Runs **profile stage** checks (schema + cross-file + `project.yaml` → `profiled`)
2. Syncs `project.yaml` → `lifecycle_status: validated`
3. Computes `profile_hash` (SHA-256 of 7 profile files **after** lifecycle sync)
4. Writes/updates `registry.manifest.yaml` with `lifecycle_status: validated`
5. Runs **gate stage** checks to confirm ready to scan

**Exit 1** if any step fails.

## Gate check (read-only)

After sign-off, or to verify an existing validated project:

```bash
python asrp.py validate --project {project_id}
# equivalent:
python asrp.py validate --project {project_id} --stage gate
```

**Gate checks:**

- JSON Schema pass on 7 profile YAMLs + `registry.manifest.yaml`
- Cross-file linkage (same as profile stage)
- `registry.manifest.yaml` → `lifecycle_status == validated`
- `project.yaml` → `lifecycle_status == validated` (synced with manifest)
- `profile_hash` matches current profile file contents

## Manifest fields

| Field | Source |
|-------|--------|
| `project_id` | `project.yaml` → `project.id` |
| `lifecycle_status` | Always `validated` at sign-off |
| `validated_at` | ISO datetime UTC at sign-off |
| `validated_by` | `--by` argument |
| `profile_files` | Fixed 7-file order (see below) |
| `profile_hash` | `sha256:` + hex of concatenated file bytes |
| `schema_versions` | `"1.0"` per profile schema |

**Profile file order (hash input):**

```
project.yaml → components.yaml → technologies.yaml → architecture.yaml
→ scope.yaml → context.yaml → assessment.yaml
```

## Re-profile → re-sign-off

When Step 1 re-profiles after changes:

1. Agent sets `project.yaml` → `lifecycle_status: profiled`
2. Summary flags: **manifest stale — re-run Validate Gate**
3. Human re-reviews scope/context/assessment if needed
4. Re-run `--sign-off` to refresh manifest hash and lifecycle

Do **not** scan until gate passes after re-profile.

## Definition of Done

- [ ] `--stage profile` pass before sign-off
- [ ] `--sign-off --by "..."` completes with exit 0
- [ ] `--stage gate` pass (default `validate`)
- [ ] `project.yaml` and manifest both `validated`
- [ ] `profile_hash` matches current files

## Abort if

- Profile stage fails (schema, cross-file, or lifecycle not `profiled`)
- `--sign-off` without `--by`
- Gate hash mismatch after sign-off (should not happen — report as bug)

## Summary

Emit gate summary per [summary-format.md](summary-format.md) § Validate Gate.
