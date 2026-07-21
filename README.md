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
│   ├── 1. Projects/
│   │   └── 1.1 Template/
│   │       ├── 1-project.yaml
│   │       ├── 2-components.yaml
│   │       ├── 3-technologies.yaml ⭐ Rule Mapping
│   │       ├── 4-architecture.yaml
│   │       ├── 5-context.yaml
│   │       ├── 6-scope.yaml
│   │       ├── 7-assessment.yaml
│   │       ├── README.md
│   │       └── docs/
│   ├── 2. Security Knowledge Base ⭐ (Core Asset)/
│   │   ├── 2.1 Security Standards/
│   │   │   ├── 2.1.1 OWASP ASVS/
│   │   │   ├── 2.1.2 OWASP Top 10/
│   │   │   ├── 2.1.3 OWASP WSTG/
│   │   │   ├── 2.1.4 OWASP Code Review Guide/
│   │   │   ├── 2.1.5 OWASP Cheat Sheets/
│   │   │   ├── 2.1.6 NIST SSDF/
│   │   │   ├── 2.1.7 CWE/
│   │   │   ├── 2.1.8 CAPEC/
│   │   │   ├── 2.1.9 CIS Benchmarks/
│   │   │   └── 2.1.10 Internal Standards/
│   │   ├── 2.2 Security Domains/
│   │   │   ├── 2.2.1 Authentication/
│   │   │   ├── 2.2.2 Authorization/
│   │   │   ├── 2.2.3 Session Management/
│   │   │   ├── 2.2.4 Input Validation/
│   │   │   ├── 2.2.5 Cryptography/
│   │   │   ├── 2.2.6 Secrets Management/
│   │   │   ├── 2.2.7 Dependency Management/
│   │   │   ├── 2.2.8 API Security/
│   │   │   ├── 2.2.9 Configuration Security/
│   │   │   ├── 2.2.10 Logging & Monitoring/
│   │   │   ├── 2.2.11 File Upload Security/
│   │   │   ├── 2.2.12 Business Logic Security/
│   │   │   └── 2.2.13 Infrastructure Security/
│   │   ├── 2.3 Rule Library/
│   │   ├── 2.4 Review Checklists/
│   │   ├── 2.5 Playbooks/
│   │   ├── 2.6 Threat Models/
│   │   ├── 2.7 Secure Coding Guidelines/
│   │   ├── 2.8 Best Practices/
│   │   ├── 2.9 Attack Patterns/
│   │   ├── 2.10 Remediation Guides/
│   │   ├── 2.11 Case Studies/
│   │   └── 2.12 Decision Logs/
│   ├── 3. Assessment Engine/
│   │   ├── 3.1 Source Acquisition (Clone - Local Workspace)/
│   │   ├── 3.2 Workspace/
│   │   │   ├── 3.2.1 Source Code/
│   │   │   ├── 3.2.2 Architecture/
│   │   │   ├── 3.2.3 Configuration/
│   │   │   ├── 3.2.4 Infrastructure/
│   │   │   ├── 3.2.5 Dependencies/
│   │   │   ├── 3.2.6 Secrets/
│   │   │   ├── 3.2.7 API Specification/
│   │   │   └── 3.2.8 Documentation/
│   │   ├── 3.3 Evidence Collection/
│   │   ├── 3.4 Rule Evaluation/
│   │   ├── 3.5 AI Reviewer/
│   │   ├── 3.6 Findings/
│   │   ├── 3.7 Risk Assessment/
│   │   ├── 3.8 Report Generator/
│   │   └── 3.9 Re-Verification/
│   ├── 4. Reporting/
│   │   ├── 4.1 Executive Report/
│   │   ├── 4.2 Technical Report/
│   │   ├── 4.3 Compliance Report/
│   │   ├── 4.4 Security Score/
│   │   ├── 4.5 Findings Dashboard/
│   │   └── 4.6 Remediation Roadmap/
│   ├── 5. Dashboard & Analytics/
│   │   ├── 5.1 Project Dashboard/
│   │   ├── 5.2 Portfolio Dashboard/
│   │   ├── 5.3 Compliance Dashboard/
│   │   ├── 5.4 Risk Trends/
│   │   ├── 5.5 Rule Coverage/
│   │   └── 5.6 Assessment Metrics/
│   └── 6. Integrations/
│       ├── 6.1 GitHub/
│       ├── 6.2 Bitbucket/
│       ├── 6.3 CI/
│       ├── 6.4 GitLab/
│       ├── 6.5 DAST/
│       ├── 6.6 Container Scanner/
│       ├── 6.7 Dependency Scanner/
│       ├── 6.8 SAST/
│       └── 6.9 Secret Scanner/
│
├── Security Knowledge Base/
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
1. Read [`Security Knowledge Base/knowledge/README.md`](Security%20Knowledge%20Base/knowledge/README.md) for the Knowledge Base taxonomy.
2. Read [`Security Knowledge Base/docs/appsec-research-pipeline/README.md`](Security%20Knowledge%20Base/docs/appsec-research-pipeline/README.md) for the research pipeline reference.
3. Use the ASRP tree as the target architecture when adding new project management, assessment, reporting, analytics, or integration assets.

## One Concept = One Home
The Knowledge Base under `Security Knowledge Base/knowledge/` is the canonical home for AppSec concepts.
When adding or moving content, keep a topic in one place and cross-link related material instead of duplicating it.
