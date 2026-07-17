# AppSec Research Pipeline (Mr P — Professional)

**User guide (tiếng Việt)**: [`USER-GUIDE.md`](USER-GUIDE.md) — đội ngũ Mr, kịch bản sử dụng, cách invoke.

## Goal

Khi bạn chat một AppSec topic (ví dụ: `HTTP caching`, `OAuth token validation`, `SSRF defense`), pipeline sẽ điều phối “team security” theo vai trò, và hệ thống hóa thành **Knowledge Base topic(s)** trong `knowledge/`.

**Runtime source of truth**: [`../../SKILL.md`](../../SKILL.md) (cursor-agents: `skills/appsec-research-orchestrator/SKILL.md`). Các file trong `references/pipeline/` là reference thiết kế.

**Persona names**: [`role-glossary.md`](role-glossary.md)

**Interactive mode**: [`interactive-mode.md`](interactive-mode.md)

## Execution modes

| Mode | Mô tả |
|------|--------|
| `batch` (default) | Full pipeline một lần |
| `interactive` | Một Mr mỗi turn + checkpoint; gọi Mr QA giữa các bước |
| `qa-only` | Chỉ Mr QA (Query Assistant) |
| `single-role` | Một Mr pipeline, không KB final |

## Workflow (mỗi subtopic = 1 KB topic)

### 0. Pre-flight (batch / interactive)

1. KB dedup search trong `knowledge/` nếu repo đích có thư mục này (xem target repo `knowledge/README.md` hoặc [`../knowledge-taxonomy.md`](../knowledge-taxonomy.md))
2. Resolve `category` từ domain taxonomy
3. Emit `SecurityResearchJob` YAML fenced (`## SecurityResearchJob`) theo `job-schema.md`
4. Confirm split plan nếu `split_confirmation.required` hoặc user yêu cầu single doc

### 1. Role execution (tuần tự)

Cho mỗi subtopic, ghi role stubs **trước** KB final:

1. **Mr A (Analyst)** → theory (`#3`, `#4`, minimal `#1–#2`)
2. **Mr S (Strategist)** → threat model, trust boundaries (`#7`, scope)
3. **Mr H (Hazard)** → failure modes (`#8`)
4. **Mr R (Realist)** → assumptions, edge cases (`#7`, `#8`)
5. **Mr B (Builder)** → mitigations + verification (`#7`, `#9`, `#10`)
6. **Mr Q (Qualifier)** → evidence pack (`#11`, `#12`)
7. **Mr W (Writer)** → merge thành KB final + reconciliation + quality gates

**Mr QA (Query Assistant)**: interactive-only — Q&A tại checkpoint, không trong chuỗi trên.

**Interactive**: một role per turn + `## Checkpoint` — xem [`interactive-mode.md`](interactive-mode.md).

### 2. Final output

- KB topic(s) theo template 12 section
- `proposed_path` per file (default output mode)

## Batch vs interactive

```text
Batch:     Job → [split?] → all stubs → KB
Interactive: Job → [split?] → Mr A → Checkpoint → … → Mr W → Checkpoint → KB
```

## When to split subtopic

Split nếu topic chứa nhiều “mechanism axis” khác nhau:

- `cơ chế semantics` vs `trust boundaries/threat scenarios` vs `verification/observability signals`

## One Concept = One Home (cross-link guideline)

Trước khi tạo KB topic mới, kiểm tra `knowledge/` trong repo đích (ví dụ `knowledge/web/HTTP.md`).
Nếu overlap đáng kể:

- không viết lại nội dung cốt lõi
- cross-link ở `#11 Related Topics`
- ghi rõ in-scope/out-of-scope trong `#1` và/hoặc `#7`
- legacy files: set `legacy_format: true` trong `dedup_hits`

## Template prompt

Xem [`prompt-template.md`](prompt-template.md).
