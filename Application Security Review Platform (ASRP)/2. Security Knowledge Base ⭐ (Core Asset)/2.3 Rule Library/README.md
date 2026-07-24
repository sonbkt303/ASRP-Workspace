# Layer 2.3 — Rule Library

Thư mục `2.3 Rule Library` chứa toàn bộ các **Executable Rules** và dữ liệu ánh xạ cho hệ thống Application Security Review Platform (ASRP).

---

## 📚 Tài liệu Kiến trúc

- **Layer Blueprint:** Chi tiết thiết kế kiến trúc, hợp đồng schema và spec của Rule Resolver nằm tại [`BLUEPRINT.md`](BLUEPRINT.md).

---

## 🏗️ Cấu trúc Thư mục

- [`index.yaml`](index.yaml): Master catalog liệt kê và quản lý 19 quy tắc thực thi.
- [`by-engine/`](by-engine/): Quản lý Executable Rules theo **Công cụ Quét Thực thi** ([Xem `by-engine/README.md`](by-engine/README.md)).
  - `semgrep/`: SAST Static Code Rules Đa Ngôn Ngữ (`sql-injection.yaml`, `cors-wildcard.yaml`...)
  - `gitleaks/`: Secret Scanner Rules (`gitleaks-aws-access-key.yaml`...)
  - `trivy/`: Container & Dependency SCA Rules (`trivy-docker-user-root.yaml`...)
  - `checkov/`: IaC Infrastructure Rules (`iac-s3-bucket-public.yaml`...)
  - `cicd/`: CI/CD Pipeline Rules (`cicd-unpinned-github-action.yaml`...)
  - `custom-ai/`: AI Reviewer Rules (`ai-bola-idor-check.yaml`...)
- [`by-domain/`](by-domain/): Quản lý Executable Rules theo **Lĩnh vực Bảo mật Nghiệp vụ** ([Xem `by-domain/README.md`](by-domain/README.md)).
  - `secrets/`, `injection/`, `access-control/`, `cryptography/`, `misconfiguration/`, `dependencies/`, `infrastructure/`, `ssrf/`
- [`mappings/`](mappings/): Lưu trữ các file ánh xạ dữ liệu ([Xem `mappings/README.md`](mappings/README.md)).
  - `tech-stack-map.yaml`: Ánh xạ Công nghệ -> Rule Sets.
  - `owasp-top10-2021.yaml`: Ánh xạ OWASP Top 10 A01-A10 -> Rule IDs.
