# Layer 2.3 — Rule Library Engine Directory (`by-engine/`)

Thư mục `by-engine/` lưu trữ toàn bộ các **Quy tắc Kiểm tra Thực thi (Executable Rules)** được phân loại theo từng **Scanner Engine** cụ thể. 

Mỗi thư mục con đại diện cho một công cụ quét chuyên biệt trong hệ thống ASRP.

> **Thiết kế Đa ngôn ngữ (Multi-Language Rule Design):**  
> Mỗi Rule ID trong `semgrep/` đại diện cho **1 Khái niệm Lỗ hổng Bảo mật Chuẩn hóa** (ví dụ `sql-injection.yaml`, `cors-wildcard.yaml`). Bên trong file rule khai báo các khối pattern quét song song cho nhiều ngôn ngữ lập trình khác nhau (`python`, `javascript`, `typescript`, `go`, `java`).

---

## 🏗️ Cấu trúc & Danh mục Engine (6 Scanner Engines)

```
by-engine/
├── README.md                           # Tài liệu hướng dẫn thư mục (file này)
├── semgrep/                            # SAST — Multi-Language Static Code Rules (9 rules)
├── gitleaks/                           # Secret Scanner — Bí mật & Credentials Leak (4 rules)
├── trivy/                              # SCA & Container Scanner (3 rules)
├── checkov/                            # IaC — Infrastructure as Code Security (2 rules)
├── cicd/                               # CI/CD Pipeline & Supply Chain Security (2 rules)
└── custom-ai/                          # AI Reviewer — Business Logic & Auth Flow (1 rule)
```

---

## 🎯 Chức năng & Danh mục Rules theo từng Engine

### 1. `by-engine/semgrep/` (SAST — Multi-Language Static Code Analysis)
* **Nhiệm vụ:** Phân tích mã nguồn tĩnh (AST) đa ngôn ngữ (`python`, `javascript`, `typescript`, `go`, `java`).
* **Danh mục Rules Đa Ngôn Ngữ hiện tại (9 rules):**
  - [`sql-injection.yaml`](semgrep/sql-injection.yaml) (`ASRP-INJ-001`): SQL Injection via string formatting/concatenation.
  - [`command-injection.yaml`](semgrep/command-injection.yaml) (`ASRP-INJ-002`): OS Command Injection via system calls.
  - [`path-traversal.yaml`](semgrep/path-traversal.yaml) (`ASRP-PATH-001`): Unsafe file path operations.
  - [`insecure-deserialization.yaml`](semgrep/insecure-deserialization.yaml) (`ASRP-DESER-001`): Unsafe binary/object deserialization RCE.
  - [`weak-crypto-hash.yaml`](semgrep/weak-crypto-hash.yaml) (`ASRP-CRYPTO-001`): Weak MD5/SHA1 hashing algorithms.
  - [`ssrf-request.yaml`](semgrep/ssrf-request.yaml) (`ASRP-SSRF-001`): Server-Side Request Forgery via HTTP clients.
  - [`reflected-xss.yaml`](semgrep/reflected-xss.yaml) (`ASRP-XSS-001`): Reflected XSS without output escaping.
  - [`debug-mode-enabled.yaml`](semgrep/debug-mode-enabled.yaml) (`ASRP-MISCFG-001`): Application Debug Mode Enabled in production.
  - [`cors-wildcard.yaml`](semgrep/cors-wildcard.yaml) (`ASRP-MISCFG-002`): Permissive CORS Wildcard Origin (`*`).

---

### 2. `by-engine/gitleaks/` (Secret Scanner — All Languages)
* **Nhiệm vụ:** Phân tích Regex & Entropy để phát hiện mật khẩu, API keys và tokens bị rò rỉ trong mã nguồn.
* **Danh mục Rules hiện tại (4 rules):**
  - [`gitleaks-generic-api-key.yaml`](gitleaks/gitleaks-generic-api-key.yaml) (`ASRP-SEC-001`): Generic API Secret Token.
  - [`gitleaks-aws-access-key.yaml`](gitleaks/gitleaks-aws-access-key.yaml) (`ASRP-SEC-002`): AWS Access Key ID & Secret Access Key.
  - [`gitleaks-private-rsa-key.yaml`](gitleaks/gitleaks-private-rsa-key.yaml) (`ASRP-SEC-003`): Private RSA/SSH PEM Key.
  - [`gitleaks-database-connection-string.yaml`](gitleaks/gitleaks-database-connection-string.yaml) (`ASRP-SEC-004`): Database URI Connection String with Passwords.

---

### 3. `by-engine/trivy/` (SCA & Container Scanner)
* **Nhiệm vụ:** Quét lỗ hổng phụ thuộc (SCA CVEs) và cấu hình Dockerfile.
* **Danh mục Rules hiện tại (3 rules):**
  - [`trivy-docker-user-root.yaml`](trivy/trivy-docker-user-root.yaml) (`ASRP-TRIVY-001`): Container running as root user.
  - [`trivy-docker-latest-tag.yaml`](trivy/trivy-docker-latest-tag.yaml) (`ASRP-TRIVY-002`): Base image using unpinned `:latest` tag.
  - [`trivy-sca-vulnerable-dependency.yaml`](trivy/trivy-sca-vulnerable-dependency.yaml) (`ASRP-SCA-001`): High/Critical CVE in package dependencies.

---

### 4. `by-engine/checkov/` (IaC Infrastructure Scanner)
* **Nhiệm vụ:** Quét tệp hạ tầng dạng mã (Terraform, Kubernetes manifest, CloudFormation).
* **Danh mục Rules hiện tại (2 rules):**
  - [`iac-s3-bucket-public.yaml`](checkov/iac-s3-bucket-public.yaml) (`ASRP-IAC-001`): AWS S3 Bucket Public Read/Write Access.
  - [`iac-k8s-privileged-container.yaml`](checkov/iac-k8s-privileged-container.yaml) (`ASRP-IAC-002`): Kubernetes Privileged Container Execution.

---

### 5. `by-engine/cicd/` (CI/CD Pipeline Security Scanner)
* **Nhiệm vụ:** Quét đường ống CI/CD và rủi ro chuỗi cung ứng phần mềm (`.github/workflows/`).
* **Danh mục Rules hiện tại (2 rules):**
  - [`cicd-unpinned-github-action.yaml`](cicd/cicd-unpinned-github-action.yaml) (`ASRP-CICD-001`): GitHub Action not pinned to full commit SHA.
  - [`cicd-github-token-write-perm.yaml`](cicd/cicd-github-token-write-perm.yaml) (`ASRP-CICD-002`): Overly permissive GITHUB_TOKEN write permissions.

---

### 6. `by-engine/custom-ai/` (AI Reviewer Logic Checks)
* **Nhiệm vụ:** Dùng LLM/AI Agent kiểm tra các lỗi logic nghiệp vụ và luồng xác thực/phân quyền.
* **Danh mục Rules hiện tại (1 rule):**
  - [`ai-bola-idor-check.yaml`](custom-ai/ai-bola-idor-check.yaml) (`ASRP-AI-001`): BOLA/IDOR resource ownership check.

---

## 📝 Hướng dẫn Thêm Pattern Ngôn ngữ mới vào Rule có sẵn

Khi cần bổ sung quét thêm 1 ngôn ngữ mới (ví dụ `Go` hoặc `Java`) cho một lỗi bảo mật có sẵn (ví dụ SQL Injection):
1. Mở file rule tương ứng trong `by-engine/semgrep/` (ví dụ `sql-injection.yaml`).
2. Thêm ngôn ngữ vào `applicable_technologies.languages: ["python", "javascript", "typescript", "go", "java"]`.
3. Thêm khối `pattern` mới dưới `engine_config.semgrep_patterns` tương ứng với cú pháp ngôn ngữ mới.
