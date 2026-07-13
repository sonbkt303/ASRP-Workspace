# Chapter 3 — OWASP Top 10

## Mục tiêu học
Bạn biết cách đọc OWASP theo “cơ chế phòng vệ” và biến thành checklist kiểm tra áp dụng cho web/backend.

## Khái niệm cốt lõi
Mỗi hạng mục OWASP nên được quy về: trigger condition, impact, control cần có, cách verify/evidence.

## Checklist “làm được gì” (security controls)
- Với mỗi mục rủi ro bạn chọn, ghi được control cần có và cách verify tối thiểu (unit/integration/static scan hoặc review artifact).
  Evidence/test: link tới test plan hoặc scan report (artifact).
- Mapping OWASP → module/control theme (ví dụ Broken Access Control → Module 2; Injection → Module 4).
  Evidence/test: bảng mapping OWASP mục ↔ kiểm soát ↔ nơi kiểm trong code/API (artifact).
- Xác định “what to check” cho security review (các dấu hiệu trong code/config/log).
  Evidence/test: checklist câu hỏi review (artifact).

## Ví dụ threat / scenario
Injection: query/command concatenation trong endpoint tạo data leak nếu không dùng safe APIs/parameterized queries.

## Bài tập nhỏ
Chọn 3 hạng mục OWASP rủi ro cao và viết 1 trang “controls + verify evidence” (theo template evidence).

## Cross-module links
- Tới: [module-4-secure-coding](../../knowledge/17-Secure-Coding/Secure-Coding.md) (turn OWASP into secure code)
- Tới: [module-8-security-review](../../knowledge/18-Architecture/Security-Review.md) (review findings)


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
