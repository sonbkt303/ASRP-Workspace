# Layer 2.3 — Rule Library

Thư mục `2.3 Rule Library` chứa toàn bộ các **Executable Rules** và dữ liệu ánh xạ cho hệ thống Application Security Review Platform (ASRP).

---

## 📚 Tài liệu Kiến trúc

- **Layer Blueprint:** Chi tiết thiết kế kiến trúc, hợp đồng schema và spec của Rule Resolver nằm tại [`BLUEPRINT.md`](BLUEPRINT.md).

---

## 🏗️ Cấu trúc Thư mục

- [`index.yaml`](index.yaml): Master catalog liệt kê và quản lý 12 quy tắc thực thi.
- [`by-engine/`](by-engine/): Lưu trữ các file rules theo Scanner Engine ([Xem hướng dẫn `by-engine/README.md`](by-engine/README.md)).
  - `semgrep/`: SAST Static Code Rules (SQLi, Command Inj, Path Traversal, Deserialization, SSRF...)
  - `gitleaks/`: Secret Scanner Rules (API Keys, AWS Credentials, Private RSA Keys...)
  - `trivy/`: Container & Dependency SCA Rules (Docker root user, CVEs...)
  - `custom-ai/`: AI Reviewer Rules (BOLA/IDOR Logic...)
- [`mappings/`](mappings/): Lưu trữ các file ánh xạ dữ liệu ([Xem hướng dẫn `mappings/README.md`](mappings/README.md)).
  - `tech-stack-map.yaml`: Ánh xạ Công nghệ -> Rule Sets.
  - `owasp-top10-2021.yaml`: Ánh xạ OWASP Top 10 A01-A10 -> Rule IDs.
