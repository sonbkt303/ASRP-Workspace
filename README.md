# ASRP Workspace

This repository is organized into two root-level work areas:

- `ASRP Workspace/`: the workspace root for the ASRP initiative.
- `Application Security Review Platform (ASRP)/`: the platform taxonomy and canonical ASRP structure.
- `Repository Content/`: the current working content moved from the old root folders.
- `.cursor/`: local Cursor assets and skill mirrors kept at the repository root.

## Root layout
```text
ASRP Workspace/
├── Application Security Review Platform (ASRP)/
│   ├── 1. Project Management/
│   ├── 2. Security Knowledge Base ⭐ (Core Asset)/
│   ├── 3. Assessment Engine/
│   ├── 4. Reporting/
│   ├── 5. Dashboard & Analytics/
│   └── 6. Integrations/
│
├── Repository Content/
│   ├── apps/
│   ├── automation/
│   ├── datasets/
│   ├── docs/
│   ├── infrastructure/
│   ├── knowledge/
│   ├── labs/
│   ├── packages/
│   ├── scripts/
│   └── tools/
│
├── .cursor/
├── .git/
└── README.md
```

## Start here
1. Read [`Repository Content/knowledge/README.md`](Repository%20Content/knowledge/README.md) for the Knowledge Base taxonomy.
2. Read [`Repository Content/docs/appsec-research-pipeline/README.md`](Repository%20Content/docs/appsec-research-pipeline/README.md) for the research pipeline reference.
3. Use the ASRP tree as the target architecture when adding new project management, assessment, reporting, analytics, or integration assets.

## One Concept = One Home
The Knowledge Base under `Repository Content/knowledge/` is the canonical home for AppSec concepts.
When adding or moving content, keep a topic in one place and cross-link related material instead of duplicating it.
