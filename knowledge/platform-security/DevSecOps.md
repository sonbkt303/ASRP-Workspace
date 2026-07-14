# Chapter 9 — DevSecOps

## Mục tiêu học
Bạn đưa security vào vòng đời: CI/CD gates, scan, secret detection và runtime signals.

## Khái niệm cốt lõi
Security gates: build/deploy/runtime; shift-left + shift-right; evidence-based policies.

## Checklist “làm được gì” (security controls)
- [ ] Evidence cần có cho mỗi checklist item (test method/artifact) theo chuẩn chung
- Thiết kế CI step cho SAST/dependency scan/secret scan + tiêu chí fail/threshold.  
  Evidence/test: scan report + policy/threshold artifact.
- Thiết kế gating cho security tests (integration) và quy trình triage.  
  Evidence/test: test results + triage workflow artifact.
- Định nghĩa runtime alerts cho auth errors/anomaly và response workflow.  
  Evidence/test: dashboard/alert definitions artifact.

## Ví dụ threat / scenario

## Bài tập nhỏ

## Cross-module links
- Tới: [module-8-security-review](../../knowledge/foundations/Security-Review.md) (chuyển findings thành CI/CD gates)

# Chapter 9 — DevSecOps

## Mục tiêu học

## Khái niệm cốt lõi

## Checklist “làm được gì” (security controls)
- [ ] Evidence cần có cho mỗi checklist item (test method/artifact) theo chuẩn chung

## Ví dụ threat / scenario

## Bài tập nhỏ

## Cross-module links


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
