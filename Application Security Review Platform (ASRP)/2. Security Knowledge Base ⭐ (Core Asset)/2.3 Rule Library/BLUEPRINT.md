# Rule Library & Rule Resolver Blueprint

> **Status:** Active — Layer 2 canonical reference.  
> **Last updated:** 2026-07-24  
> **Parent:** [ARCHITECTURE-BLUEPRINT.md](../../ARCHITECTURE-BLUEPRINT.md) §Layer 2  
> **Previous Layer:** [1. Projects Registry/BLUEPRINT.md](../../1.%20Projects%20Registry/BLUEPRINT.md)  
> **Scope:** Executable rules format, index catalog, technology/standard mappings, and Rule Resolver contract.

---

## 1. Role

**Rule Library** (`2.3 Rule Library`) là trái tim của **Security Review as Code** trong ASRP — lưu trữ và quản lý toàn bộ các quy tắc kiểm tra bảo mật thực thi (executable rules) của các công cụ SAST, SCA, Secret Scanner, IaC và Custom AI Checks.

**Trách nhiệm:**

- Lưu trữ các quy tắc kiểm tra dạng YAML chuẩn hóa theo từng công cụ (`semgrep`, `gitleaks`, `trivy`, `custom`) hoặc từng Security Domain.
- Cung cấp catalog trung tâm `index.yaml` để quản lý danh mục quy tắc, phiên bản, trạng thái (enabled/disabled).
- Duy trì các file ánh xạ (mappings): công nghệ → bộ luật (`tech-stack-map.yaml`) và tiêu chuẩn → bộ luật (`owasp-top10-2021.yaml`).
- Cung cấp cơ chế **Rule Resolver** hợp nhất profile dự án Layer 1 với Rule Library để sinh file cấu hình thực thi `resolved-rules.json` cho Assessment Engine (Layer 3).

---

## 2. Folder Structure

```
2.3 Rule Library/
├── BLUEPRINT.md                        # Layer 2 canonical blueprint (file này)
├── index.yaml                          # Master catalog quản lý tất cả rules
├── by-engine/                          # Phân loại rules theo tool/scanner
│   ├── semgrep/
│   ├── gitleaks/
│   └── trivy/
├── by-domain/                          # Phân loại rules theo Security Domain
│   ├── secrets/
│   ├── injection/
│   ├── auth/
│   └── dependencies/
└── mappings/                           # Ánh xạ công nghệ & tiêu chuẩn
    ├── tech-stack-map.yaml             # Tech stack -> Rule set IDs
    └── owasp-top10-2021.yaml           # OWASP Category -> Rule IDs
```

---

## 3. Executable Rule Format (YAML Contract)

Mỗi file rule độc lập tuân theo cấu trúc chuẩn hóa dưới đây:

```yaml
rule:
  id: "ASRP-SEC-001"
  name: "Hardcoded Generic API Key"
  description: "Phát hiện API key hoặc secret token bị hardcode trong source code."
  severity: "high"             # critical | high | medium | low | info
  engine: "gitleaks"            # gitleaks | semgrep | trivy | custom_ai
  category: "secrets"
  
  applicable_technologies:
    languages: ["all"]
    frameworks: ["all"]
  
  standard_mapping:
    owasp_top10_2021: ["A07:2021-Identification and Authentication Failures"]
    cwe: ["CWE-798"]
    asvs_v4: ["V14.2.1"]

  knowledge_ref: "knowledge/domains/secrets-management.md"
  
  engine_config:
    gitleaks_rule_id: "generic-api-key"
    regex: '(?i)(api_key|apikey|secret_key)\s*[:=]\s*["''][A-Za-z0-9_\-]{16,}["'']'
    
  remediation:
    summary: "Đưa secret vào biến môi trường (Environment Variable) hoặc Secret Manager."
    reference_url: "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"
```

---

## 4. Master Index (`index.yaml`)

Catalog trung tâm liệt kê và quản lý trạng thái của mọi rule trong hệ thống:

```yaml
rule_library:
  version: "1.0"
  updated_at: "2026-07-24T00:00:00Z"
  rules:
    - id: "ASRP-SEC-001"
      path: "by-engine/gitleaks/gitleaks-generic-api-key.yaml"
      enabled: true
      engine: "gitleaks"
      severity: "high"
      rule_set_ids: ["secrets-basic", "owasp-top10-2021"]
    
    - id: "ASRP-INJ-001"
      path: "by-engine/semgrep/python-sql-injection.yaml"
      enabled: true
      engine: "semgrep"
      severity: "critical"
      rule_set_ids: ["python-secure-coding", "owasp-top10-2021"]
```

---

## 5. Technology & Standard Mappings

### 5.1 Technology Mapping (`mappings/tech-stack-map.yaml`)

Dùng để tự động gợi ý bộ rule khi Layer 1 khai báo công nghệ:

```yaml
tech_stack_map:
  languages:
    python:
      default_rule_sets: ["python-secure-coding", "secrets-basic"]
    javascript:
      default_rule_sets: ["nodejs-secure-coding", "secrets-basic"]
  frameworks:
    fastapi:
      default_rule_sets: ["fastapi-security"]
    react:
      default_rule_sets: ["react-xss-prevention"]
```

### 5.2 Standard Mapping (`mappings/owasp-top10-2021.yaml`)

```yaml
owasp_top10_2021_mapping:
  "A01:2021-Broken Access Control":
    rule_ids: ["ASRP-AUTH-001", "ASRP-AUTH-002"]
  "A03:2021-Injection":
    rule_ids: ["ASRP-INJ-001", "ASRP-INJ-002"]
  "A07:2021-Identification and Authentication Failures":
    rule_ids: ["ASRP-SEC-001"]
```

---

## 6. Rule Resolver Contract (`resolved-rules.json`)

**Rule Resolver** là module kết nối giữa Layer 1 và Layer 2 để chuẩn bị dữ liệu thực thi cho Layer 3:

```
[Layer 1 Profile: assessment.yaml + technologies.yaml + scope.yaml] 
                             +
             [Layer 2 Rule Library: index.yaml]
                             ↓
                     [Rule Resolver]
                             ↓
              [runs/{run_id}/resolved-rules.json]
```

### Output Schema Spec (`resolved-rules.json`):

```json
{
  "run_id": "run-20260724-001",
  "project_id": "cleverdent",
  "resolved_at": "2026-07-24T10:00:00Z",
  "rules_count": 2,
  "engines_summary": {
    "gitleaks": 1,
    "semgrep": 1
  },
  "rules": [
    {
      "id": "ASRP-SEC-001",
      "engine": "gitleaks",
      "severity": "high",
      "target_components": ["cleverdent-api"],
      "config": {
        "rule_id": "generic-api-key"
      }
    },
    {
      "id": "ASRP-INJ-001",
      "engine": "semgrep",
      "severity": "critical",
      "target_components": ["cleverdent-api"],
      "config": {
        "pattern": "db.execute(f'SELECT * FROM users WHERE id = {user_input}')"
      }
    }
  ]
}
```

---

## 7. Next Steps & Implementation Roadmap

| Milestone | Deliverable | Status |
|-----------|-------------|--------|
| **M1** | Ban hành `2.3 Rule Library/BLUEPRINT.md` | **Done** |
| **M2** | Khởi tạo `index.yaml` (19 rules) và các file `mappings/` (OWASP Top 10 A01–A10) | **Done** |
| **M3** | Bộ luật Executable 6 Engines (`semgrep`, `gitleaks`, `trivy`, `checkov`, `cicd`, `custom_ai`) | **Done** |
| **M4** | Multi-Language Rule Design Standard ([`.agents/AGENTS.md`](../../../.agents/AGENTS.md)) | **Done** |
| **M5** | Handoff sang Layer 3 — Hiện thực Rule Resolver Engine & Assessment Engine | Next Layer |
