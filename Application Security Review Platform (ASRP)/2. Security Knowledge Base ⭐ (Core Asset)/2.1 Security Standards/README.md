# Module 2.1: Security Standards Core Kernel

## 📌 Architectural Overview
Module **2.1 Security Standards** serves as the **Unified Security Standard Kernel** of the Application Security Review Platform (ASRP). It consolidates international security frameworks, vulnerability taxonomies, and compliance standards into a single, programmatically accessible lookup kernel.

```text
2.1 Security Standards/
├── index.yaml                              <-- Master Kernel Registry (10 Submodules)
├── unified-standards-matrix.yaml           <-- Central CWE Primary Key Lookup Table
├── 2.1.1 OWASP ASVS/                       <-- Application Security Verification Standard
├── 2.1.2 OWASP Top 10/                     <-- Web & API Top 10 Security Risks
├── 2.1.3 OWASP WSTG/                       <-- Web Security Testing Guide
├── 2.1.4 OWASP Code Review Guide/          <-- Static Code Audit Guidelines
├── 2.1.5 OWASP Cheat Sheets/               <-- Developer Proactive Defense Controls
├── 2.1.6 NIST SSDF/                        <-- Secure Software Development Framework
├── 2.1.7 CWE/                              <-- Common Weakness Enumeration
├── 2.1.8 CAPEC/                            <-- Common Attack Pattern Enumeration
├── 2.1.9 CIS Benchmarks/                   <-- Container & Infrastructure Security
└── 2.1.10 Internal Standards/              <-- Industry Compliance (PCI-DSS, ISO 27001, NĐ 13)
```

---

## 🔑 Single Source of Truth (SSOT) & Primary Key Resolution
All international security standards are bound to a **CWE Primary Key** (`cwe_id`).
When AI Agent or a SAST engine detects a vulnerability, it assigns a single CWE ID (e.g. `CWE-639`). 
The `standard_resolver.py` engine automatically resolves the complete cross-standard matrix:
- **OWASP ASVS v4.0.3:** `V4.1.1`, `V4.2.1`
- **OWASP Top 10 2021:** `A01:2021-Broken Access Control`
- **OWASP API Top 10 2023:** `API1:2023-BOLA`
- **NIST SSDF:** `PW.5`
- **CAPEC:** `CAPEC-122`
- **PCI-DSS v4.0:** `PCI-REQ-6.2`
- **ISO/IEC 27001:** `A.8.25`

---

## ⚙️ Programmatic Resolution API
The `StandardResolver` module located at `Application Security Review Platform (ASRP)/3. Assessment Engine/3.4 Rule Evaluation/standard_resolver.py` provides Python APIs:
```python
from standard_resolver import StandardResolver

resolver = StandardResolver(workspace_root)
matrix = resolver.resolve_cwe("CWE-639")
standards = resolver.get_profile_standards(tech_stack=["nestjs", "graphql", "docker"])
```
