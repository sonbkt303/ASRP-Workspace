# Step 0 — Source Acquisition (Layer 3.1)

Clone or copy source code into the persistent ASRP workspace before profiling or scanning.

## Paths

| Resource | Path |
|----------|------|
| Clone root | `3. Assessment Engine/3.1 Source Acquisition/clones/{project_id}/{component_id}/` |
| Run output | `1. Projects Registry/{project_id}/runs/{run_id}/acquisition.json` |
| Profile registry | `1. Projects Registry/{project_id}/` |

## Procedure

1. **Bootstrap project** — If `1. Projects Registry/{project_id}/` does not exist, copy `1.1 Template/` to `{project_id}/` and set `project.yaml` → `lifecycle_status: draft`.

2. **Resolve components** — Read `components.yaml` or use `--component` flag for a single target.

3. **Acquire source** — For each component:
   - If `clones/{project_id}/{component_id}/` exists → keep and `git pull` latest (idempotent re-acquisition).
   - If missing or deleted → clone from Git URL or copy from local path (`--source` or `components.yaml` repo URL).

4. **Create run folder** — Generate `run_id` (format: `run-YYYYMMDD_HHMMSS`) and write `acquisition.json` with commit SHA, source URL, and component list.

5. **CLI option** — `python asrp.py acquire --project {project_id} [--source URL|path] [--interactive]`

## Definition of Done

- [ ] Every target component has source at `clones/{project_id}/{component_id}/`
- [ ] `runs/{run_id}/acquisition.json` exists
- [ ] Run ID recorded in `ASRPReviewJob`

## Abort if

- No source URL/path available and user did not provide `--source` in interactive mode
- Clone/copy fails for any required component

## Summary

Emit Step 0 summary per [summary-format.md](summary-format.md).
