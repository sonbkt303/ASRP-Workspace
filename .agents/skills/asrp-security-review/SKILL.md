---
name: asrp-security-review
description: Execute the full 4-step AI End-to-End Security Review workflow for a target project (Source Acquisition -> AI Auto-Profiling -> AI Orchestrated Scan -> Executive HTML Report). Trigger whenever the user wants to audit a project or run a full security assessment.
---

# ASRP AI Security Review Skill Workflow

When the user asks to run review or profile a project or specific component (e.g. `cleverdent` or sub-repo `dent-api-nestjs` of project `cleverdent`), the AI Agent executes the workflow sequentially:

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

## Step 2: AI-Orchestrated Security Scanning & Verification (Layer 3.4 & 3.6)
*(To be executed when scan phase is triggered)*

---

## Step 3: Risk Assessment & Executive Reporting (Layer 3.7 & Layer 5)
*(To be executed when report generation is triggered)*

---

### Summary Output
Output a clean, highly professional summary table of the profiled component(s), auto-discovered tech stack, selected security standards, and updated Layer 1 YAML files.
