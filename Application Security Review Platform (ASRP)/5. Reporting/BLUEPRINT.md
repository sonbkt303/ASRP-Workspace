# Reporting Layer Blueprint

> **Status:** Active — Layer 5 canonical reference.  
> **Last updated:** 2026-07-27  
> **Parent:** [ARCHITECTURE-BLUEPRINT.md](../ARCHITECTURE-BLUEPRINT.md) §Layer 5  
> **Previous Layer:** [3. Assessment Engine/BLUEPRINT.md](../3.%20Assessment%20Engine/BLUEPRINT.md)  
> **Scope:** Executive reports, technical finding breakdowns, HTML dashboards, and Markdown exports.

---

## 1. Role

**Reporting** (`5. Reporting`) là Layer 5 của ASRP — chịu trách nhiệm chuyển đổi toàn bộ dữ liệu kiểm tra bảo mật (Layer 1 Profile, Layer 2 Standards, Layer 3 Findings & Risk Score) thành các **Báo cáo An toàn Thông tin Chuyên nghiệp** dành cho CISO, Tech Lead, Dev Team và Security Auditor.

**Trách nhiệm:**

- Tổng hợp thông tin từ Layer 1, Layer 2 và Layer 3.
- Tự động sinh báo cáo HTML Executive Dashboard độc lập (`security_review_report.html`).
- Tự động sinh báo cáo Markdown hỗ trợ CI/CD & Git Pull Request (`security_review_report.md`).
- Cung cấp giao diện trực quan với Scorecard, Severity breakdown, SLA Roadmap và Remediation code snippets.

---

## 2. Folder Structure

```
5. Reporting/
├── BLUEPRINT.md                        # Layer 5 canonical blueprint (file này)
├── README.md                           # Hướng dẫn Layer 5
├── report_generator.py                 # Core Report Generator CLI Tool
└── templates/                          # Report templates (nếu có)
```

---

## 3. Report Artifact Outputs

Báo cáo được tự động sinh tại thư mục run của dự án `1. Projects Registry/{project_id}/runs/{run_id}/`:

| Format | Artifact | Mục đích sử dụng |
|---|---|---|
| **HTML** | `security_review_report.html` | Báo cáo Executive Dashboard trực quan cho Ban giám đốc, CISO & Tech Lead |
| **Markdown** | `security_review_report.md` | Báo cáo gắn vào Git PR, Issue Tracker, Confluence, Wiki |
