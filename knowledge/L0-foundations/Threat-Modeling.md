# Chapter 7 — Threat Modeling

## Mục tiêu học
Bạn có thể làm threat modeling có cấu trúc để ưu tiên mitigations và tạo backlog control.

## Khái niệm cốt lõi
Scope → assets/data → data flows → trust boundaries → threats → mitigations → prioritization.

## Checklist “làm được gì” (security controls)
- [ ] Evidence cần có cho mỗi checklist item (test method/artifact) theo chuẩn chung
- DFD ở mức vừa đủ (client/app/services/data store) và xác định trust boundary.  
  Evidence/test: DFD artifact.
- Threat list có mapping boundary + impact + likelihood (hoặc scoring).  
  Evidence/test: threat list artifact.
- Mitigation backlog gắn với control theme (Module 2/4/5/6).  
  Evidence/test: mitigation backlog format artifact.

## Ví dụ threat / scenario

## Bài tập nhỏ

## Cross-module links
- Tới: [module-8-security-review](../../knowledge/L0-foundations/Security-Review.md) (turn threats into review checklist)
- Tới: [module-9-devsecops](../../knowledge/L4-platform-security/DevSecOps.md) (mitigations into CI gates)


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
