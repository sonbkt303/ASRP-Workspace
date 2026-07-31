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

### 1. Multi-Module Knowledge Base Scope Loading
1. Load Layer 1 Security Matrix (`standards`, `security_domains`, `rule_set_ids`, `checklists`).
2. Load Layer 2 knowledge base artifacts from:
   - `2.1 Security Standards` (OWASP ASVS v4.0, OWASP Top 10 2021, NIST SSDF, CWE Top 25, CIS Benchmarks)
   - `2.2 Security Domains` (11 core security domains)
   - `2.3 Rule Library/index.yaml` (currently 19 core executable rules)
   - `2.4 Review Checklists` (Domain & architecture review checklists)
   - `2.9 Attack Patterns` (CAPEC attack scenarios)
### 2. Multi-Dimensional AI Code Audit & Modular Stage JSON Generation (AI-Primary Engine)
AI Agent acts as the Primary Security Audit Engine to perform direct code analysis against the full Layer 2 Security Knowledge Matrix in `clones/{project_id}/{component_id}/` and generate individual stage output files in `runs/{run_id}/stage_outputs/` complying with the **Common Stage JSON Schema**:

- **Stage 2.1 Standards Audit:** Generate `stage_2_1_standards.json` verifying compliance against OWASP ASVS v4.0, CWE Top 25.
- **Stage 2.2 Security Domains:** Generate `stage_2_2_domains.json` evaluating the 13 Security Domains.
- **Stage 2.3 Executable Rules:** Generate `stage_2_3_rules.json` running static & AI rules across engines.
- **Stage 2.4 Review Checklists:** Generate `stage_2_4_checklists.json` systematically evaluating domain checklist items (`verification_requirement`).
- **Stage 2.6 Threat Models:** Generate `stage_2_6_threats.json` evaluating STRIDE architectural threat scenarios.
- **Stage 2.10 Remediation Guides:** Generate `stage_2_10_remediations.json` containing actionable code diff patches.

### 3. Auxiliary Python CLI Tooling Integration (Auxiliary Data)
Optionally invoke Python CLI runner `python asrp.py scan --project {project_id}` or individual engine modules (`rule_resolver.py`, `scanner_orchestrator.py`) as auxiliary helper tools to gather supplementary static tool findings (`raw_outputs/`).

### 4. Verification, Deduplication & Aggregated Normalization (Layer 3.6)
1. Cross-verify raw tool findings against AI contextual code analysis and Review Checklists.
2. Eliminate False Positives and duplicate findings across engines.
3. Aggregate all `stage_outputs/*.json` into a master `findings.json`.
4. **STRICT MULTI-MODULE TRACEABILITY REQUIREMENT:** Every finding in `findings.json` MUST strictly reference:
   - Valid `rule_id` from Layer 2.3 (e.g. `ASRP-AI-001`, `ASRP-SEC-004`).
   - `security_domain` from Layer 2.2 (e.g. `access_control`, `secrets`).
   - Standard mappings from Layer 2.1 (CWE ID, OWASP Top 10 2021, OWASP ASVS v4.0).
   - Corresponding Review Checklist item reference from Layer 2.4 (`review_checklist_ref`).
5. Save normalized findings to `1. Projects Registry/{project_id}/runs/{run_id}/findings.json`.

### 5. Summary Output
Output a clean, professional summary table of discovered vulnerabilities categorized by severity, engine source, and target component.


---

## Step 3: Risk Assessment & Executive Reporting (Layer 3.7 & Layer 5)

### 1. Input Data Loading
1. Access target run directory: `1. Projects Registry/{project_id}/runs/{run_id}/`.
2. Load verified findings: `findings.json` (from Step 2).
3. Load project context: `context.yaml`, `project.yaml`, `architecture.yaml` (from Step 1).

### 2. Layer 3.7 Risk Assessment Engine Execution
Calculate Security Health Score and Risk Metrics:
- **Health Score Calculation (0 - 100):** Deduct severity weights from 100 base score (`CRITICAL`: -25, `HIGH`: -10, `MEDIUM`: -5, `LOW`: -2).
- **Security Grade Assignment:**
  - `Grade A`: 90 - 100 (Pass)
  - `Grade B`: 80 - 89 (Pass)
  - `Grade C`: 70 - 79 (Conditional)
  - `Grade D`: 50 - 69 (Action Required)
  - `Grade F`: < 50 (Fail / Critical Risk)
- **Gate Status Evaluation:** Mark status as `PASSED` or `ACTION REQUIRED`.
- **SLA Remediation Roadmap Creation:**
  - `Phase 1 (Immediate SLA 24-48h)`: Critical & High secrets / RCE / Injection flaws.
  - `Phase 2 (Short-term SLA 7d)`: High severity access control & dependency flaws.
  - `Phase 3 (Maintenance SLA 30d)`: Medium severity misconfigurations.
- Save output to: `1. Projects Registry/{project_id}/runs/{run_id}/risk_assessment.json`.

### 3. Layer 5 Report Generation Execution
Invoke Report Generator to build multi-level reports using stage outputs from the designated run directory (e.g., `run-20260730_171130`):
1. **Mandatory Report Template Usage:** AI Agent MUST load the standard HTML templates from `1. Projects Registry/1.1 Template/reports/`:
   - `1.1 Template/reports/executive_dashboard.html` for project-wide dashboard reports.
   - `1.1 Template/reports/component_report.html` for component-specific reports.
2. **Interactive Stage Output Mapping:** Each report includes interactive stage pills (2.1 Standards, 2.2 Security Domains, 2.3 Rule Library, 2.4 Review Checklists, 2.6 Threat Models, 2.10 Remediation Guides). Clicking a stage pill filters and lists only the findings mapped to that specific module.
3. **Component-Specific Reports:** Generate independent reports for each repository defined in `components.yaml` using `component_report.html` as the baseline design:
   - `security_review_report_{component_id}.html`
   - `security_review_report_{component_id}.md`
4. **Executive Project Dashboard:** Generate consolidated project dashboard showing side-by-side health scores & grade comparisons across all components using `executive_dashboard.html` as the baseline design:
   - `security_review_report.html`
   - `security_review_report.md`

### 4. Summary Output
Output a clean, professional executive summary table including Security Health Score, Grade, Rating, Gate Status, SLA Roadmap breakdown, and clickable links to all generated HTML & Markdown reports (both component-level and project-level).




