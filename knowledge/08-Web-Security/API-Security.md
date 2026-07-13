# Chapter 5 — API Security

## Mục tiêu học
Bạn có thể harden REST/GraphQL APIs chống IDOR, mass assignment, abuse/rate limit và làm security checks nhất quán.

## Khái niệm cốt lõi
API threat surface: endpoints + parameters + filters + batch ops; auth middleware và object-level authorization.

## Checklist “làm được gì” (security controls)
- [ ] Evidence cần có cho mỗi checklist item (test method/artifact) theo chuẩn chung
- Checklist API contract: endpoint có auth yêu cầu, object-level auth đúng, và field filter/response không leak.  
  Evidence/test: contract doc + test plan (artifact).
- Schema validation: request payload/query param được validate đúng type/shape và giới hạn kích thước.  
  Evidence/test: schema + tests (artifact).
- Anti-abuse: rate limiting + uniform error handling cho enumeration.  
  Evidence/test: policy doc + load test or abuse test evidence (artifact).

## Ví dụ threat / scenario
Mass assignment: PATCH user có thể set `role` nếu binding/DTO sai.

## Bài tập nhỏ
Thiết kế “API security checklist” cho 5 endpoint phổ biến + role matrix (để test nhanh).

## Cross-module links
- Tới: [module-8-security-review](../../knowledge/18-Architecture/Security-Review.md) (review API findings)


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
