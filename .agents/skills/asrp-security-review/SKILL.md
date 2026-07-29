---
name: asrp-security-review
description: Execute the full 4-step AI End-to-End Security Review workflow for a target project (Source Acquisition -> AI Auto-Profiling -> AI Orchestrated Scan -> Executive HTML Report). Trigger whenever the user wants to audit a project or run a full security assessment.
---

# ASRP AI Security Review Skill Workflow

## Step Invocation & Routing
AI Agent supports running steps independently or as a complete workflow:
- **Command `/asrp-security-review profile [project_id]`** (or `step 1`): Runs **Step 1 ONLY** (Layer 1 AI Auto-Profiling & Registry Generation).
- **Command `/asrp-security-review scan [project_id]`** (or `step 2`): Runs **Step 2 ONLY** (AI-Primary Security Scanning & Verification using Layer 1 profiles as input).
- **Command `/asrp-security-review report [project_id]`** (or `step 3`): Runs **Step 3 ONLY** (Risk Assessment & Executive HTML/MD Report Generation using `findings.json` as input).
- **Command `/asrp-security-review review [project_id]`** (or `full` / default): Runs **Full Workflow (Step 1 -> Step 2 -> Step 3)**.

---

## Step 1: AI Auto-Profiling & Selective Registry Generation (Layer 1)

### 1. Target Component Isolation & Discovery
1. Access `Application Security Review Platform (ASRP)/3. Assessment Engine/3.1 Source Acquisition/clones/{project_id}/`.
2. Check if a specific target component/sub-repo is specified (e.g., `dent-api-nestjs`):
   - **If specific component requested:** Focus inspection ONLY on `clones/{project_id}/{target_component_id}/`.
   - **If entire project requested:** Discover and inspect all component subdirectories under `clones/{project_id}/`.
3. **RESOURCE OPTIMIZATION EXCLUSION RULE:**
   - Always exclude non-essential folders and files that do not contain project source code: `node_modules`, `.devcontainer`, `.husky`, `.vscode`, `.idea`, `.github`, `.agents`, `dist`, `build`, `coverage`, `.pnpm-store`, `yarn-error.log`, `.git`, `tmp`, `temp`.
   - Populating `exclude_paths` in `components.yaml` and `out_of_scope_paths` in `scope.yaml` is MANDATORY to prevent AI orchestrator and SAST tools from wasting CPU, memory, and LLM context resources on non-project artifacts.


### 2. Deep Component Code & Stack Inspection
Deep-dive into the target component's repository and inspect structural configuration files:
- Node.js / TypeScript: `package.json`, `nest-cli.json`, `tsconfig.json`, `pnpm-workspace.yaml`, `biome.json`
- Python: `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`
- Docker & Infrastructure: `docker-compose.yaml`, `Dockerfile`, `k8s/`, `helm/`, `envs/`
- DB & Storage: MongoDB schemas, Prisma, TypeORM, Mongoose, Redis connections

### 3. AI Intelligent Security Standards & Compliance Selection (Layer 2.1)
Analyze the discovered code, tech stack, and business domain to select optimal security standards from all 10 subdirectories in `2. Security Knowledge Base ⭐ (Core Asset)/2.1 Security Standards/`:
- **OWASP ASVS** (Application Security Verification Standard v4.0)
- **OWASP Top 10** (Web & API Security Vulnerability Risks)
- **OWASP WSTG** (Web Security Testing Guide v4.2)
- **OWASP Code Review Guide** (Secure Code Review & Architecture Inspection)
- **OWASP Cheat Sheets** (Proactive Security Controls & Defensive Design)
- **NIST SSDF** (NIST SP 800-218 Secure Software Development Framework)
- **CWE** (Common Weakness Enumeration & CWE Top 25)
- **CAPEC** (Common Attack Pattern Enumeration and Classification)
- **CIS Benchmarks** (Kubernetes, Docker & Container Hardening)
- **Internal Standards** (HIPAA, GDPR, PCI-DSS, ISO 27001 Domain Compliance)

**STRICT COMPLIANCE MANDATE:**
AI Agent MUST automatically write and map the selected standard IDs into:
1. `technologies.yaml` -> `technologies[].rule_set_ids` (mapped specifically per component tech stack).
2. `assessment.yaml` -> `assessment.rule_sets` (aggregated project-wide security standards).


### 4. Non-Destructive Merging into Layer 1 Profiles
Update profile YAML files in `1. Projects Registry/{project_id}/` following template schemas from `1. Projects Registry/1.1 Template`:
- **CRITICAL SAFE MERGE RULE:** When updating a specific sub-repo/component (e.g. `dent-api-nestjs`), update or append ONLY its entry in `components.yaml` and `technologies.yaml`. **DO NOT overwrite, wipe, or affect existing other components** (e.g., preserve `dent-monorepo` intact).
- Update files:
  - `project.yaml`
  - `components.yaml` (safely merged per component)
  - `technologies.yaml` (safely merged per component)
  - `architecture.yaml`
  - `context.yaml`
  - `scope.yaml`
  - `assessment.yaml`
  - `registry.manifest.yaml`

---

## Step 2: AI-Driven Security Scanning & Verification (Layer 3.4 & 3.6)

### 1. Context & Scope Loading & Rule Resolution
1. Access Layer 1 profiles in `1. Projects Registry/{project_id}/`:
   - Read `components.yaml` and `scope.yaml` to identify target component directories, `scan_paths`, and mandatory `exclude_paths`.
   - Read `technologies.yaml` and `assessment.yaml` to load resolved `rule_set_ids` and security standards.
   - Read Layer 2 Rule Library catalog from `2. Security Knowledge Base ⭐ (Core Asset)/2.3 Rule Library/index.yaml` (currently 19 core executable rules).
2. Resolve enabled `rule_id` entries matching project `rule_set_ids`.

### 2. Primary AI Contextual Code Audit
AI Agent performs direct contextual security analysis on in-scope source code in `clones/{project_id}/{component_id}/`:
- **Business Logic & Access Control:** BOLA / IDOR, broken object-level authorization, authentication bypass.
- **Injection & Input Validation:** SQL/NoSQL Injection, Command Injection, Path Traversal, SSRF, XSS.
- **Data Protection & Cryptography:** Hardcoded secrets/tokens, weak hashing/encryption, unsafe deserialization.
- **Security Misconfigurations:** Debug modes enabled, CORS wildcards, permissive CORS, insecure defaults.
- **Container & IaC Security:** Dockerfile root execution, unpinned base images, permissive K8s securityContext.

### 3. Auxiliary Python CLI Tooling Integration
Optionally invoke Python CLI runner `python asrp.py scan --project {project_id}` or individual engine modules (`rule_resolver.py`, `scanner_orchestrator.py`) to gather supplementary static tool findings (`raw_outputs/`).

### 4. Verification, Deduplication & Normalization (Layer 3.6)
1. Cross-verify raw tool findings against AI contextual code analysis.
2. Eliminate False Positives and duplicate findings across engines.
3. **STRICT RULE TRACEABILITY REQUIREMENT:** Every finding in `findings.json` MUST strictly reference a valid `rule_id` from Layer 2.3 (e.g. `ASRP-SEC-001`, `ASRP-INJ-001`, `ASRP-AI-001`) and inherit its standard severity, CWE, and OWASP mappings.
4. Enrich verified findings with:
   - Severity (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`)
   - Mandatory standard mappings: CWE ID, OWASP Top 10 2021, OWASP ASVS v4.0.
   - Precise file path, line numbers, and code snippet.
   - Root cause description and actionable code remediation guidance.
5. Save normalized findings to:
   `1. Projects Registry/{project_id}/runs/{run_id}/findings.json`


### 5. Summary Output
Output a clean, professional summary table of discovered vulnerabilities categorized by severity, engine source, and target component.

---

## Step 3: Risk Assessment & Executive Reporting (Layer 3.7 & Layer 5)
*(To be executed when report generation is triggered)*

---

### Summary Output
Output a clean, highly professional summary table of the executed step results, auto-discovered tech stack, selected security standards, and updated output files.

