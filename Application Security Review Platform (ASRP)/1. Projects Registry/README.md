# Projects Registry

Layer 1 of ASRP — project profiles and assessment configuration.

**Blueprint:** [PROJECTS-REGISTRY-BLUEPRINT.md](../PROJECTS-REGISTRY-BLUEPRINT.md)  
**Architecture overview:** [ARCHITECTURE-BLUEPRINT.md](../ARCHITECTURE-BLUEPRINT.md)

## Structure

```
1. Projects Registry/
├── 1.1 Template/       # Starter YAML (do not edit for project-specific data)
├── schema/             # JSON Schema Draft 2020-12
├── cleverdent/         # Example validated project instance
└── README.md
```

## Bootstrap a New Project

1. Copy `1.1 Template/` to `{project-id}/` (kebab-case)
2. Fill profile files in bootstrap order (see [1.1 Template/README.md](1.1%20Template/README.md))
3. Validate against schemas in `schema/`
4. Create `registry.manifest.yaml` after human gate review
5. Set `project.lifecycle_status: validated`

See [PROJECTS-REGISTRY-BLUEPRINT.md](../PROJECTS-REGISTRY-BLUEPRINT.md) §8 for full procedure.

## Lifecycle

`draft` → `profiled` → `validated` → `scanning` → `completed`

Assessment Engine must not scan until `lifecycle_status = validated`.

## Documentation

- Template conventions: [1.1 Template/README.md](1.1%20Template/README.md)
- Template docs: [1.1 Template/documentation/](1.1%20Template/documentation/)
