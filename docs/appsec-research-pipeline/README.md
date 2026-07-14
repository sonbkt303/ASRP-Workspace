# AppSec Research Pipeline (Professor P)

## Goal
Khi bạn chat một AppSec topic (ví dụ: `HTTP caching`, `OAuth token validation`, `SSRF defense`), pipeline sẽ điều phối “team security” theo vai trò, và hệ thống hóa thành **Knowledge Base topic(s)** trong `knowledge/`.

**Runtime source of truth**: `.cursor/skills/appsec-research-orchestrator/SKILL.md`. Các file trong `docs/appsec-research-pipeline/` là reference thiết kế.

## Workflow (mỗi subtopic = 1 KB topic)

### 0. Pre-flight (bắt buộc)
1. KB dedup search trong `knowledge/` (xem `knowledge/README.md`)
2. Resolve `category` từ domain taxonomy
3. Emit `SecurityResearchJob` plan theo `job-schema.md` (subtopics, evidence_targets)
4. Confirm split plan nếu user yêu cầu single doc hoặc split > 3

### 1–4. Role execution
1. Mr A + Mr S: theory-first mechanism (70/30)
2. Mr B + Mr H + Mr R: defensive (hardening + monitoring + verification) và common mistakes
3. Mr Q: evidence pack (RFC/standards/OWASP links)
4. Mr W: assemble thành KB topic đúng output contract + reconciliation

## When to split subtopic
Split nếu bạn thấy topic chứa nhiều “mechanism axis” khác nhau mà không thể gói chung hợp lý trong 1 tài liệu:
- `cơ chế semantics` vs `trust boundaries/threat scenarios` vs `verification/observability signals`

## One Concept = One Home (cross-link guideline)
Trước khi tạo KB topic mới, cố gắng kiểm tra trong `knowledge/` xem có topic gần trùng không (ví dụ `knowledge/web/HTTP.md`).
Nếu overlap đáng kể:
- không viết lại nội dung cốt lõi
- đặt cross-link ở `# 11. Related Topics`
- ghi rõ ranh giới in-scope/out-of-scope trong `# 1` và/hoặc `# 7`

## Template prompt bạn dùng

```text
Research Topic: <topic>.
Category: <category>. Difficulty: <level>. Tags: <tags>.
Theory-first (70/30), but defensive must include hardening + monitoring + verification (proof signals in #9).
If too broad, split into subtopics (atomic documents) and confirm split plan first.
Evidence strictness: #12 needs ≥2 RFC/standards (or documented exception) + ≥1 OWASP (or official security guideline).
Every main claim in #7, #8, #10 must map to evidence inline or in #12 (or label "needs evidence").
Check knowledge/ for duplicates before writing.
Output: KB topic(s) per kb-write-topic template (#1–#12). Output mode: propose file path.
```
