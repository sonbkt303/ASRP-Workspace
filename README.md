# ASRP Workspace

Workspace chứa **Application Security Review Platform (ASRP)** và **Security Knowledge Base** — nền tảng Security Review as Code và kho tri thức bảo mật hỗ trợ.

Tài liệu hướng dẫn sử dụng nhanh CLI: [`USAGE-GUIDE.md`](USAGE-GUIDE.md)  
Tài liệu kiến trúc chính: [`Application Security Review Platform (ASRP)/ARCHITECTURE-BLUEPRINT.md`](Application%20Security%20Review%20Platform%20(ASRP)/ARCHITECTURE-BLUEPRINT.md)

---

## Folder Tree

```
ASRP Workspace/
├── Application Security Review Platform (ASRP)/
│   ├── ARCHITECTURE-BLUEPRINT.md          # Canonical overview — 6 layers
│   ├── HANDOFF.md                         # Next-layer deliverables (Handoff to Layer 3)
│   │
│   ├── 1. Projects Registry/              # Layer 1 — project profiles
│   │   ├── BLUEPRINT.md                   # Layer 1 blueprint (done)
│   │   ├── README.md
│   │   ├── 1.1 Template/                  # Template cho mọi project instance
│   │   │   ├── README.md
│   │   │   ├── registry.manifest.yaml
│   │   │   ├── project.yaml
│   │   │   ├── context.yaml
│   │   │   ├── scope.yaml
│   │   │   ├── architecture.yaml
│   │   │   ├── technologies.yaml
│   │   │   ├── components.yaml
│   │   │   ├── assessment.yaml
│   │   │   └── documentation/
│   │   │       └── readme.md
│   │   ├── cleverdent/                    # Example project (validated)
│   │   │   ├── registry.manifest.yaml
│   │   │   ├── project.yaml
│   │   │   ├── context.yaml
│   │   │   ├── scope.yaml
│   │   │   ├── architecture.yaml
│   │   │   ├── technologies.yaml
│   │   │   ├── components.yaml
│   │   │   ├── assessment.yaml
│   │   │   └── runs/
│   │   └── schema/                        # JSON Schema validation
│   │       ├── _definitions.json
│   │       ├── registry-manifest.schema.json
│   │       ├── project.schema.json
│   │       ├── context.schema.json
│   │       ├── scope.schema.json
│   │       ├── architecture.schema.json
│   │       ├── technologies.schema.json
│   │       ├── components.schema.json
│   │       └── assessment.schema.json
│   │
│   ├── 2. Security Knowledge Base ⭐ (Core Asset)/   # Layer 2 — standards, domains, rules
│   │   ├── 2.1 Security Standards/
│   │   │   ├── 2.1.1 OWASP ASVS
│   │   │   ├── 2.1.2 OWASP Top 10
│   │   │   ├── 2.1.3 OWASP WSTG
│   │   │   ├── 2.1.4 OWASP Code Review Guide
│   │   │   ├── 2.1.5 OWASP Cheat Sheets
│   │   │   ├── 2.1.6 NIST SSDF
│   │   │   ├── 2.1.7 CWE
│   │   │   ├── 2.1.8 CAPEC
│   │   │   ├── 2.1.9 CIS Benchmarks
│   │   │   └── 2.1.10 Internal Standards
│   │   ├── 2.2 Security Domains/
│   │   │   ├── 2.2.1 Authentication
│   │   │   ├── 2.2.2 Authorization
│   │   │   ├── 2.2.3 Session Management
│   │   │   ├── 2.2.4 Input Validation
│   │   │   ├── 2.2.5 Cryptography
│   │   │   ├── 2.2.6 Secrets Management
│   │   │   ├── 2.2.7 Dependency Management
│   │   │   ├── 2.2.8 API Security
│   │   │   ├── 2.2.9 Configuration Security
│   │   │   ├── 2.2.10 Logging & Monitoring
│   │   │   ├── 2.2.11 File Upload Security
│   │   │   ├── 2.2.12 Business Logic Security
│   │   │   └── 2.2.13 Infrastructure Security
│   │   ├── 2.3 Rule Library/              # Layer 2 — Executable Rules & Resolver (done)
│   │   │   ├── BLUEPRINT.md               # Layer 2 blueprint (done)
│   │   │   ├── README.md
│   │   │   ├── index.yaml                 # Master catalog (19 rules)
│   │   │   ├── by-engine/                 # 6 Scanner Engines (semgrep, gitleaks, trivy, checkov, cicd, custom_ai)
│   │   │   ├── by-domain/                 # 8 Security Domains
│   │   │   └── mappings/                  # Tech Stack & OWASP Top 10 A01–A10
│   │   ├── 2.4 Review Checklists/             # Human Review Checklists
│   │   │   ├── README.md
│   │   │   └── architecture-security-checklist.yaml
│   │   ├── 2.5 Playbooks
│   │   ├── 2.6 Threat Models
│   │   ├── 2.7 Secure Coding Guidelines
│   │   ├── 2.8 Best Practices
│   │   ├── 2.9 Attack Patterns
│   │   ├── 2.10 Remediation Guides
│   │   ├── 2.11 Case Studies
│   │   └── 2.12 Decision Logs
│   │
│   ├── 3. Assessment Engine/              # Layer 3 — clone → scan → findings (in progress)
│   │   ├── BLUEPRINT.md                   # Layer 3 blueprint (done)
│   │   ├── 3.1 Source Acquisition (Clone - Local Workspace)
│   │   ├── 3.2 Workspace/
│   │   │   ├── 3.2.1 Source Code
│   │   │   ├── 3.2.2 Architecture
│   │   │   ├── 3.2.3 Configuration
│   │   │   ├── 3.2.4 Infrastructure
│   │   │   ├── 3.2.5 Dependencies
│   │   │   ├── 3.2.6 Secrets
│   │   │   ├── 3.2.7 API Specification
│   │   │   └── 3.2.8 Documentation
│   │   ├── 3.3 Evidence Collection
│   │   ├── 3.4 Rule Evaluation/
│   │   │   └── rule_resolver.py           # Core Rule Resolver CLI Tool (done)
│   │   ├── 3.5 AI Reviewer
│   │   ├── 3.6 Findings
│   │   ├── 3.7 Risk Assessment
│   │   ├── 3.8 Report Generator
│   │   └── 3.9 Re-Verification
│   │
│   ├── 4. Reporting/                        # Layer 5 — audit outputs
│   │   ├── 4.1 Executive Report
│   │   ├── 4.2 Technical Report
│   │   ├── 4.3 Compliance Report
│   │   ├── 4.4 Security Score
│   │   ├── 4.5 Findings Dashboard
│   │   └── 4.6 Remediation Roadmap
│   │
│   ├── 5. Dashboard & Analytics/            # Layer 6 — portfolio views
│   │   ├── 5.1 Project Dashboard
│   │   ├── 5.2 Portfolio Dashboard
│   │   ├── 5.3 Compliance Dashboard
│   │   ├── 5.4 Risk Trends
│   │   ├── 5.5 Rule Coverage
│   │   └── 5.6 Assessment Metrics
│   │
│   └── 6. Integrations/                     # Layer 4 — external tools & CI/CD
│       ├── 6.1 GitHub
│       ├── 6.2 Bitbucket
│       ├── 6.3 CI
│       ├── 6.4 GitLab
│       ├── 6.5 DAST
│       ├── 6.6 Container Scanner
│       ├── 6.7 Dependency Scanner
│       ├── 6.8 SAST
│       ├── 6.9 Secret Scanner
│       └── AI Reviewer
│
└── Security Knowledge Base/                 # Concept KB — lý thuyết & nghiên cứu
    ├── apps/
    ├── automation/
    ├── datasets/
    ├── docs/
    │   ├── appsec-research-pipeline/
    │   │   ├── README.md
    │   │   ├── USER-GUIDE.md
    │   │   ├── interactive-mode.md
    │   │   ├── job-schema.md
    │   │   ├── prompt-template.md
    │   │   ├── role-glossary.md
    │   │   └── role-output-contract.md
    │   ├── knowledge-base-document-rules.md
    │   └── knowledge-base-topic-template.md
    ├── infrastructure/
    ├── knowledge/
    │   ├── README.md
    │   ├── 1. foundations/
    │   │   ├── 1. core/
    │   │   │   ├── 1. computer-science/
    │   │   │   ├── 2. cryptography/
    │   │   │   ├── 3. programming/
    │   │   │   └── 4. linux/
    │   │   └── 2. supporting/
    │   │       ├── 1. data/
    │   │       ├── 2. architecture/
    │   │       └── 3. mathematics/
    │   ├── foundations/                     # Legacy mirror structure
    │   │   ├── core/
    │   │   ├── supporting/
    │   │   └── references/
    │   ├── application-security/
    │   ├── ai-security/
    │   ├── cloud-security/
    │   ├── networking/
    │   ├── offensive-security/
    │   ├── platform-security/
    │   ├── secure-engineering/
    │   ├── web/
    │   ├── glossary/
    │   ├── learning-path/
    │   └── research/
    ├── labs/
    ├── packages/
    ├── scripts/
    └── tools/
```

---

## Quick Reference

| Path | Mô tả |
|------|-------|
| `Application Security Review Platform (ASRP)/` | Platform chính — 6 layers, Security Review as Code |
| `Application Security Review Platform (ASRP)/1. Projects Registry/` | Layer 1 — project profiles (template + instances + schema) |
| `Application Security Review Platform (ASRP)/2. Security Knowledge Base ⭐ (Core Asset)/` | Layer 2 — standards, domains, rule library |
| `Security Knowledge Base/` | Concept knowledge base — tách biệt với Rule Library executable |
