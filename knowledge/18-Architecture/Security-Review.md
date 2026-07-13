# Chapter 8 — Security Review

## Mục tiêu học
Bạn có thể review code/API/config theo checklist và viết findings “actionable” kèm evidence plan.

## Khái niệm cốt lõi
Finding quality: evidence, affected scope, severity rationale, remediation và verification plan.

## Checklist “làm được gì” (security controls)
- [ ] Evidence cần có cho mỗi checklist item (test method/artifact) theo chuẩn chung
- Phát hiện authZ gaps (đặc biệt object-level) và nêu rõ ảnh hưởng + cơ chế sai.  
  Evidence/test: dẫn tới endpoint/path + case reproduction plan (artifact).
- Kiểm input/output: validation thiếu, encoding sai, error leak.  
  Evidence/test: checklist review notes + links tới mẫu code/config (artifact).
- Viết evidence plan để verify fix (unit/integration/security test).  
  Evidence/test: “Verification Plan” artifact theo template findings.

## Ví dụ threat / scenario

## Bài tập nhỏ

## Cross-module links
- Tới: [module-9-devsecops](../../knowledge/09-System-Security/DevSecOps.md) (biến findings thành CI gates)


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
