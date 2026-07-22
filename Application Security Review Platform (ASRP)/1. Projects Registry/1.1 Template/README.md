# Template

Starter project configuration files for ASRP projects.

**Do not edit this folder for project-specific data.** Copy to `{project-id}/` instead.

## Files (bootstrap order)

Thứ tự ưu tiên khi điền profile — **không nằm trong tên file**, xem bảng và [PROJECTS-REGISTRY-BLUEPRINT.md](../../PROJECTS-REGISTRY-BLUEPRINT.md) §3.1.

| Step | File | Purpose | Depends on |
|------|------|---------|------------|
| 1 | `project.yaml` | Project identity and lifecycle | — |
| 2 | `components.yaml` | Repository inventory | `project.id` |
| 3 | `technologies.yaml` | Tech stack and rule set mapping | `components[].id` |
| 4 | `architecture.yaml` | Architecture profile | `project.id` |
| 5 | `scope.yaml` | Assessment scope (human-reviewed) | `components[].id` |
| 6 | `context.yaml` | Business and security context (human-reviewed) | `project.id` |
| 7 | `assessment.yaml` | Assessment lens configuration (human-reviewed) | `project.id` |
| 8 | `registry.manifest.yaml` | Validation gate output (after human review) | all profile files |

Steps 5–7 có thể làm song song sau khi có components và technologies.

## Conventions

- Semantic filenames (no numeric prefix): `project.yaml`, `components.yaml`, …
- One root wrapper per file (`project:`, `components:`, `scope:`, etc.)
- IDs use kebab-case (`cleverdent`, `cleverdent-api`)
- Cross-file linkage via `project_id` and `component_id`
- Canonical file order for hash/manifest: `profile_files` in `registry.manifest.yaml`
- Documentation and examples: `documentation/` (not `docs/`)

## Schema Validation

JSON Schemas: [`../schema/`](../schema/)

```bash
check-jsonschema --schemafile "../schema/project.schema.json" "project.yaml"
```

## Reference

- Layer blueprint: [PROJECTS-REGISTRY-BLUEPRINT.md](../../PROJECTS-REGISTRY-BLUEPRINT.md)
- Example instance: [../cleverdent/](../cleverdent/)
