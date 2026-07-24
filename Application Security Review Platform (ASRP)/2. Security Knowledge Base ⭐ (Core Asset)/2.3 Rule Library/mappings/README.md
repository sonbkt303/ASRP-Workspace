# Layer 2.3 — Rule Library Mappings Directory (`mappings/`)

Thư mục `mappings/` lưu trữ các file ánh xạ dữ liệu (Data Mappings) kết nối giữa **Hồ sơ dự án Layer 1** và **Danh mục Quy tắc Layer 2**.

Các file trong thư mục này được công cụ **Rule Resolver** đọc để tự động xác định tập luật cần thực thi cho từng dự án.

---

## 🏗️ Cấu trúc Các Tệp Ánh Xạ

```
mappings/
├── README.md                           # Tài liệu hướng dẫn thư mục (file này)
├── tech-stack-map.yaml                 # Ánh xạ Công nghệ -> Rule Set IDs
└── owasp-top10-2021.yaml               # Ánh xạ Tiêu chuẩn OWASP Top 10 -> Rule IDs
```

---

## 📄 Chi tiết Từng File Mapping

### 1. `tech-stack-map.yaml` (Technology to Rule Set Mapping)
* **Nhiệm vụ:** Ánh xạ các công nghệ lập trình, framework, và hạ tầng (khai báo tại `technologies.yaml` trong Layer 1) thành các bộ luật mặc định (`default_rule_sets`).
* **Cấu trúc mẫu:**
  ```yaml
  tech_stack_map:
    languages:
      python:
        default_rule_sets: ["python-secure-coding", "secrets-basic", "owasp-top10-2021"]
    frameworks:
      fastapi:
        default_rule_sets: ["python-secure-coding", "fastapi-security"]
  ```

---

### 2. `owasp-top10-2021.yaml` (Standard to Rule ID Mapping)
* **Nhiệm vụ:** Phân loại toàn bộ các Rule IDs theo 10 hạng mục tiêu chuẩn quốc tế **OWASP Top 10 (2021)** từ A01 đến A10.
* **Cấu trúc mẫu:**
  ```yaml
  owasp_top10_2021_mapping:
    "A01:2021-Broken Access Control":
      description: "Lỗi kiểm soát truy cập"
      rule_ids: ["ASRP-AUTH-001", "ASRP-PATH-001", "ASRP-AI-001"]
    "A03:2021-Injection":
      description: "Lỗi chèn dữ liệu độc hại"
      rule_ids: ["ASRP-INJ-001", "ASRP-INJ-002", "ASRP-XSS-001"]
  ```

---

## 🔄 Luồng Sử dụng trong Rule Resolver

```
[Layer 1: technologies.yaml + assessment.yaml]
                      ↓
[mappings/tech-stack-map.yaml & owasp-top10-2021.yaml]
                      ↓
[Rule Resolver lọc các Rule IDs từ index.yaml]
                      ↓
[Xuất file thực thi: runs/{run_id}/resolved-rules.json]
```
