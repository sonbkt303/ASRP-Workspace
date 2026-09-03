# ASRP Review Job Schema

Emit `## ASRPReviewJob` as fenced YAML before executing any subcommand (except read-only status checks).

## Required fields

| Field | Type | Description |
|-------|------|-------------|
| `project_id` | string | Kebab-case project folder under `1. Projects Registry/` |
| `subcommand` | enum | `acquire` \| `profile` \| `validate` \| `scan` \| `report` \| `review` |
| `execution_mode` | enum | `batch` (default) \| `interactive` |

## Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `component_id` | string | Scope to one component; omit for all components |
| `run_id` | string | Target run folder; omit to create (acquire/scan) or use latest (report) |
| `source` | string | Git URL or local path for `acquire` when not in components.yaml |
| `phases_completed` | string[] | Interactive resume state, e.g. `["2A", "2B"]` |
| `interactive` | object | `{ next_phase, awaiting_confirmation }` when `execution_mode: interactive` |

## Example

```yaml
project_id: cleverdent
subcommand: scan
execution_mode: batch
component_id: dent-api-nestjs
run_id: run-20260731_145000
phases_completed: []
```

## Gate

Do not execute step work until `## ASRPReviewJob` is emitted (batch and interactive modes).
