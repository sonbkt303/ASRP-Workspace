# AppSec Research Pipeline (Professor P)

## Goal
Khi bạn chat một AppSec topic (ví dụ: `HTTP caching`, `OAuth token validation`, `SSRF defense`), pipeline sẽ điều phối “team security” theo vai trò, và hệ thống hóa thành **Knowledge Base topic(s)** trong `knowledge/`.

**Runtime source of truth**: `.cursor/skills/appsec-research-orchestrator/SKILL.md`. Các file trong `docs/appsec-research-pipeline/` là reference thiết kế.

## Workflow (mỗi subtopic = 1 KB topic)

### 0. Pre-flight (bắt buộc)
1. KB dedup search trong `knowledge/` (xem `knowledge/README.md`)
2. Resolve `category` từ domain taxonomy
3. Emit `SecurityResearchJob` YAML fenced (`## SecurityResearchJob`) theo `job-schema.md`
4. Confirm split plan nếu `split_confirmation.required` hoặc user yêu cầu single doc

### 1. Role execution (tuần tự — không gộp song song)
Cho mỗi subtopic, ghi `## Role outputs (internal)` với heading `### Mr A` … `### Mr W` **trước** KB final:

1. **Mr A** → theory (`#3`, `#4`, minimal `#1–#2`)
2. **Mr S** → threat model, trust boundaries (`#7`, scope)
3. **Mr B** → mitigations + verification signals (`#7`, `#9`, `#10`)
4. **Mr H** → failure modes (`#8`)
5. **Mr R** → assumptions, edge cases (`#7`, `#8`)
6. **Mr Q** → evidence pack (`#11`, `#12`)
7. **Mr W** → merge thành KB final + reconciliation + quality gates

### 2. Final output
- KB topic(s) theo template 12 section
- `proposed_path` per file (default output mode)
- Role stubs có thể giữ trong response để traceability hoặc collapse sau khi merge

## When to split subtopic
Split nếu topic chứa nhiều “mechanism axis” khác nhau:
- `cơ chế semantics` vs `trust boundaries/threat scenarios` vs `verification/observability signals`

## One Concept = One Home (cross-link guideline)
Trước khi tạo KB topic mới, kiểm tra `knowledge/` (ví dụ `knowledge/web/HTTP.md`).
Nếu overlap đáng kể:
- không viết lại nội dung cốt lõi
- cross-link ở `#11 Related Topics`
- ghi rõ in-scope/out-of-scope trong `#1` và/hoặc `#7`

## Template prompt bạn dùng

```text
Research Topic: <topic>.
Category: <category>. Difficulty: <level>. Tags: <tags>.
Theory-first (70/30), but defensive must include hardening + monitoring + verification (proof signals in #9).
If too broad, split into subtopics (atomic documents) and confirm split plan first.
Evidence strictness: #12 needs ≥2 RFC/standards (or documented exception) + ≥1 OWASP (or official security guideline).
Every main claim in #7, #8, #10 must map to evidence inline or in #12 (or label "needs evidence").
Check knowledge/ for duplicates before writing.
Output: SecurityResearchJob YAML first, then role stubs, then KB topic(s) (#1–#12). Output mode: propose file path.
```
