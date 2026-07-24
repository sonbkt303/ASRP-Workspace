# Layer 2.3 — Rule Library Domain View Directory (`by-domain/`)

Thư mục `by-domain/` cung cấp **Góc nhìn theo Lĩnh vực Bảo mật Nghiệp vụ (Domain View)** cho toàn bộ các Executable Rules trong Rule Library.

Trong khi `by-engine/` nhóm quy tắc theo **Công cụ quét thực thi** (cho máy đọc), `by-domain/` nhóm quy tắc theo **Phân loại An toàn Thông tin** (cho Con người & Báo cáo Audit).

---

## 🏗️ Cấu trúc Các Thư mục Domain

```
by-domain/
├── README.md                           # Tài liệu hướng dẫn thư mục (file này)
├── secrets/                            # Quản lý Mật khẩu, API Keys & Secret Tokens
├── injection/                          # Chèn dữ liệu độc hại (SQLi, Command Inj, XSS)
├── access-control/                     # Kiểm soát truy cập (Path Traversal, BOLA/IDOR)
├── cryptography/                       # Mã hóa & Hàm băm an toàn
├── misconfiguration/                   # Cấu hình sai bảo mật (Debug mode, CORS)
├── dependencies/                       # Quản lý phụ thuộc & Lỗ hổng CVEs (SCA)
├── infrastructure/                     # Bảo mật Container, Dockerfile & IaC
└── ssrf/                               # Giả mạo yêu cầu máy chủ (SSRF)
```

---

## 📊 Ánh xạ Rules theo Domain (`by-domain/`)

| Domain | Thư mục | Danh sách Rule IDs | Đường dẫn File Rule gốc (`by-engine/`) |
|---|---|---|---|
| **Secrets** | `secrets/` | `ASRP-SEC-001`<br/>`ASRP-SEC-002`<br/>`ASRP-SEC-003`<br/>`ASRP-SEC-004` | [`by-engine/gitleaks/gitleaks-generic-api-key.yaml`](../by-engine/gitleaks/gitleaks-generic-api-key.yaml)<br/>[`by-engine/gitleaks/gitleaks-aws-access-key.yaml`](../by-engine/gitleaks/gitleaks-aws-access-key.yaml)<br/>[`by-engine/gitleaks/gitleaks-private-rsa-key.yaml`](../by-engine/gitleaks/gitleaks-private-rsa-key.yaml)<br/>[`by-engine/gitleaks/gitleaks-database-connection-string.yaml`](../by-engine/gitleaks/gitleaks-database-connection-string.yaml) |
| **Injection** | `injection/` | `ASRP-INJ-001`<br/>`ASRP-INJ-002`<br/>`ASRP-XSS-001` | [`by-engine/semgrep/sql-injection.yaml`](../by-engine/semgrep/sql-injection.yaml)<br/>[`by-engine/semgrep/command-injection.yaml`](../by-engine/semgrep/command-injection.yaml)<br/>[`by-engine/semgrep/reflected-xss.yaml`](../by-engine/semgrep/reflected-xss.yaml) |
| **Access Control** | `access-control/` | `ASRP-PATH-001`<br/>`ASRP-AI-001` | [`by-engine/semgrep/path-traversal.yaml`](../by-engine/semgrep/path-traversal.yaml)<br/>[`by-engine/custom-ai/ai-bola-idor-check.yaml`](../by-engine/custom-ai/ai-bola-idor-check.yaml) |
| **Cryptography** | `cryptography/` | `ASRP-CRYPTO-001` | [`by-engine/semgrep/weak-crypto-hash.yaml`](../by-engine/semgrep/weak-crypto-hash.yaml) |
| **Misconfiguration** | `misconfiguration/` | `ASRP-MISCFG-001`<br/>`ASRP-MISCFG-002` | [`by-engine/semgrep/debug-mode-enabled.yaml`](../by-engine/semgrep/debug-mode-enabled.yaml)<br/>[`by-engine/semgrep/cors-wildcard.yaml`](../by-engine/semgrep/cors-wildcard.yaml) |
| **Dependencies (SCA)** | `dependencies/` | `ASRP-SCA-001` | [`by-engine/trivy/trivy-sca-vulnerable-dependency.yaml`](../by-engine/trivy/trivy-sca-vulnerable-dependency.yaml) |
| **Infrastructure & IaC** | `infrastructure/` | `ASRP-TRIVY-001`<br/>`ASRP-TRIVY-002`<br/>`ASRP-IAC-001`<br/>`ASRP-IAC-002` | [`by-engine/trivy/trivy-docker-user-root.yaml`](../by-engine/trivy/trivy-docker-user-root.yaml)<br/>[`by-engine/trivy/trivy-docker-latest-tag.yaml`](../by-engine/trivy/trivy-docker-latest-tag.yaml)<br/>[`by-engine/checkov/iac-s3-bucket-public.yaml`](../by-engine/checkov/iac-s3-bucket-public.yaml)<br/>[`by-engine/checkov/iac-k8s-privileged-container.yaml`](../by-engine/checkov/iac-k8s-privileged-container.yaml) |
| **SSRF** | `ssrf/` | `ASRP-SSRF-001` | [`by-engine/semgrep/ssrf-request.yaml`](../by-engine/semgrep/ssrf-request.yaml) |
