# Chapter 2 — Authentication & Authorization

## Mục tiêu học
Trong module này, bạn có thể thiết kế được AuthN/AuthZ phù hợp cho web/backend APIs và tạo checklist để test access control.

## Khái niệm cốt lõi
AuthN (session/token), AuthZ (RBAC/ABAC), least privilege, object-level authorization, phòng chống các lỗi access control phổ biến (IDOR/broken access control).

## Checklist “làm được gì” (security controls)
- Xác định rõ ranh giới AuthN vs AuthZ và loại authorization cần thiết (endpoint-level vs object-level).  
  Evidence/test: bảng “role/object ownership” hoặc sơ đồ flow (artifact).
- Xây dựng checklist kiểm thử access control theo positive/negative cases (ít nhất 3 role × 3 object cases).  
  Evidence/test: test plan doc hoặc ma trận case (artifact).
- Đảm bảo cơ chế chống lạm dụng ở mức transport/thực thi (ví dụ rate limiting, anti-automation cho endpoint nhạy).  
  Evidence/test: mô tả policy và cách đo/kiểm tra (artifact + cách kiểm).

## Ví dụ threat / scenario
IDOR: endpoint `GET /api/orders/{id}` trả về dữ liệu của user khác nếu thiếu object-level check.

## Bài tập nhỏ
Viết “Access control test matrix” cho 1 use case: tạo/mở/sửa/xóa một tài nguyên theo 3 role và 3 kiểu ownership.

## Cross-module links
- Tới: [module-3-owasp-top10](../../knowledge/application-security/owasp-top10.md) (Broken Access Control)
- Tới: [module-4-secure-coding](../../knowledge/secure-engineering/secure-coding.md) (write auth-safe code)
- Tới: [module-5-api-security](../../knowledge/application-security/api-security.md) (object-level API auth)


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
