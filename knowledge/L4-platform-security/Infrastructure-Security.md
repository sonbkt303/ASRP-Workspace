# Chapter 6 — Infrastructure Security for Developers

## Mục tiêu học
Bạn biết cách tránh security misconfiguration và quản trị secrets/config cho môi trường dev/staging/prod.

## Khái niệm cốt lõi
Security misconfiguration, secrets/config hygiene, network boundary khái niệm, và logging/audit trails.

## Checklist “làm được gì” (security controls)
- [ ] Evidence cần có cho mỗi checklist item (test method/artifact) theo chuẩn chung
- TLS/headers/network baseline: cấu hình enforce HTTPS, security headers, và giảm attack surface.  
  Evidence/test: config review + automated scan output (artifact).
- Secrets hygiene: không commit secrets; dùng biến môi trường/secret manager.  
  Evidence/test: repo search + CI secret scan report (artifact).
- CI/CD deploy permission & audit trail: service account tối thiểu quyền và có audit evidence.  
  Evidence/test: CI/CD logs + IAM policy evidence (artifact).

## Ví dụ threat / scenario

## Bài tập nhỏ

## Cross-module links
- Tới: [module-8-security-review](../../knowledge/L0-foundations/Security-Review.md) (review infra/config)


## Build
- (TODO) Xây một mini-lab hoặc mô hình nhỏ để hiểu rõ assumptions + boundaries.

## Break
- (TODO) Thử các case khai thác hợp pháp để kiểm chứng các rủi ro.

## Fix
- (TODO) Harden theo controls/checklists và ghi lại remediation.

## Automate
- (TODO) Viết tool/script hoặc test workflow để lặp lại kiểm chứng.

## Share
- (TODO) Viết writeup/notes theo template vòng đời topic.
