# Chapter 4 — Secure Coding

## Mục tiêu học
Bạn có thể viết/sửa code an toàn để giảm injection/XSS/authZ bypass và xử lý lỗi không leak thông tin.

## Khái niệm cốt lõi
Input validation, output encoding theo ngữ cảnh, chống injection bằng safe APIs, data-flow (trusted→untrusted), và error handling.

## Checklist “làm được gì” (security controls)
- [ ] Evidence cần có cho mỗi checklist item (test method/artifact) theo chuẩn chung
- Cho mỗi điểm entry (request/body/query/header), nêu rõ validation/allowlist và cách kiểm chứng.  
  Evidence/test: unit tests hoặc validation review (artifact).
- Với mỗi điểm output (render/response/log), nêu encoding theo ngữ cảnh (HTML/JSON/SQL) và verify.  
  Evidence/test: XSS/encoding test cases (artifact).
- Với lỗi/exception, đảm bảo client không nhận stack trace; log có correlation nhưng không lộ secrets.  
  Evidence/test: kiểm mẫu response & log (artifact).

## Ví dụ threat / scenario

## Bài tập nhỏ

## Cross-module links
- Tới: [module-5-api-security](../../knowledge/application-security/api-security.md) (secure patterns cho API)


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
