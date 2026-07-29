# Module 2.2: Security Domains Taxonomy Registry

## 📌 Architectural Overview
Module **2.2 Security Domains** serves as the **Technical Security Taxonomy & Category Registry** of the ASRP platform. It organizes and tags all remaining Layer 2 assets (`2.1 Standards`, `2.3 Rules`, `2.4 Checklists`, `2.7 Guidelines`, `2.10 Remediation`) across 13 standardized security domains.

```text
2.2 Security Domains/
├── index.yaml                                  <-- Master Domain Registry
├── 2.2.1 Authentication/                       <-- User Identity & Password Hashing
├── 2.2.2 Authorization/                        <-- Access Control, BOLA/IDOR & BFLA
├── 2.2.3 Session Management/                   <-- Cookies, JWT Tokens & Sessions
├── 2.2.4 Input Validation/                     <-- SQLi, XSS, Cmd Injection & Deserialization
├── 2.2.5 Cryptography/                         <-- Data Encryption at Rest & Transit
├── 2.2.6 Secrets Management/                   <-- Hardcoded Secrets, Vault & KMS
├── 2.2.7 Dependency Management/                <-- SCA & Supply Chain Vulnerabilities
├── 2.2.8 API Security/                         <-- REST & GraphQL Endpoint Security
├── 2.2.9 Configuration Security/               <-- Security Headers & Debug Flags
├── 2.2.10 Logging & Monitoring/                <-- Audit Trail & PII Log Scrubbing
├── 2.2.11 File Upload Security/                <-- Extension Whitelist & Storage Isolation
├── 2.2.12 Business Logic Security/             <-- Workflow State Transitions & Rate Limits
└── 2.2.13 Infrastructure Security/             <-- Non-Root Containers & K8s Security Context
```

---

## ⚙️ Programmatic Resolution API
The `DomainResolver` module located at `Application Security Review Platform (ASRP)/3. Assessment Engine/3.4 Rule Evaluation/domain_resolver.py` provides Python APIs:
```python
from domain_resolver import DomainResolver

resolver = DomainResolver(workspace_root)
domain_info = resolver.get_domain("authorization")
all_domains = resolver.list_domains()
```
