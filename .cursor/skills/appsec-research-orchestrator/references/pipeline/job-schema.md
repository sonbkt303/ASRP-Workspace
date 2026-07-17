# SecurityResearchJob Schema (runtime)

## Purpose

Schema chuẩn hóa mỗi lần research thành một job có thể điều phối. **Bắt buộc emit** trước khi viết nội dung KB final (trừ `qa-only` và `single-role`).

Runtime source of truth cho execution: [`../../SKILL.md`](../../SKILL.md) (cursor-agents: `skills/appsec-research-orchestrator/SKILL.md`).

Persona names: [`role-glossary.md`](role-glossary.md).

Interactive protocol: [`interactive-mode.md`](interactive-mode.md).

## Emit contract (mandatory)

1. **When**: Sau pre-flight (dedup + category resolution), **trước** role stubs và KB final.
2. **Where**: Block YAML fenced đầu tiên trong response, heading `## SecurityResearchJob`.
3. **Gate**: Không viết `## Role outputs` hay KB final cho đến khi job plan đã emit.
4. **Confirmation**: Nếu `split_confirmation.required` là `true`, dừng và hỏi user trước khi tiếp tục.
5. **Interactive**: Một pipeline role per turn; emit `## Checkpoint` sau mỗi role — xem [`interactive-mode.md`](interactive-mode.md).

## Execution modes

| `execution_mode` | SecurityResearchJob required? |
|------------------|-------------------------------|
| `batch` (default) | Yes |
| `interactive` | Yes (includes `interactive` state) |
| `qa-only` | No |
| `single-role` | No |

## Job fields

```yaml
job_type: "security_research"
trigger: "chat"

execution_mode: "batch"  # batch | interactive | qa-only | single-role

root_topic: "<topic asked by user>"
category: "<resolved category; e.g. web, application-security>"
difficulty: "<e.g. intermediate>"
status: "draft"
tags: ["<tag1>", "<tag2>"]
prerequisites: "<optional>"
last_updated: "<YYYY-MM-DD>"
output_mode: "propose file path"  # chat-only | propose file path | write to knowledge/

references_requirement:
  - "RFC/standards (priority)"
  - "OWASP"
  - "official/vendor security guidance"

dedup_hits:
  - path: "knowledge/web/HTTP.md"
    overlap: "high|medium|low"
    legacy_format: false  # true if no YAML frontmatter / lifecycle headings
    action: "cross-link|extend|ask-user"

split_confirmation:
  required: false
  reason: "<e.g. user requested single doc but 3 subtopics proposed>"

subtopics:
  - id: "<short-id>"
    subtopic_title: "<KB topic title>"
    proposed_path: "knowledge/web/http-caching-auth.md"
    theory_scope: "<what mechanisms to cover>"
    defensive_scope: "<hardening/monitoring/verification; empty string if N/A>"
    must_include_sections: ["#7", "#8", "#9", "#10"]
    evidence_targets: ["RFC 9111", "OWASP ..."]

evidence_gates:
  rfc_minimum: 2
  rfc_exception_allowed: true
  owasp_minimum: 1
  needs_evidence_cap_percent: 20

reconciliation:
  rule: "Every #10 item must map to #8 or Mr R (Realist) edge case"

# Present when execution_mode: interactive
interactive:
  status: "in_progress"  # in_progress | paused | completed | aborted
  current_subtopic_id: "<short-id>"
  next_role: "A"         # A | S | H | R | B | Q | W
  completed_roles:
    "<short-id>": ["A"]
  invalidated_roles: []
  turn: 1

# Optional: role registry (display names per role-glossary.md)
roles:
  - { id: "P", name: "Professional" }
  - { id: "A", name: "Analyst" }
  - { id: "S", name: "Strategist" }
  - { id: "H", name: "Hazard" }
  - { id: "R", name: "Realist" }
  - { id: "B", name: "Builder" }
  - { id: "Q", name: "Qualifier" }
  - { id: "W", name: "Writer" }
```

## Path resolution

- `proposed_path` = `knowledge/<folder>/<kebab-case>.md`
- `category` frontmatter có thể dùng slash (`networking/http`); **folder** luôn là segment đầu tiên (`networking/`).
- Ví dụ: `category: networking/http` → `knowledge/networking/tcp-overview.md`
- Category taxonomy: target repo `knowledge/README.md` if present; else [`../knowledge-taxonomy.md`](../knowledge-taxonomy.md).

## Section mapping (role -> KB blocks)

Execute **tuần tự** Mr A (Analyst) → Mr S (Strategist) → Mr H (Hazard) → Mr R (Realist) → Mr B (Builder) → Mr Q (Qualifier) → Mr W (Writer) (không gộp song song).

- Mr A (Analyst): `#3`, `#4` (+ minimal `#1–#2`)
- Mr S (Strategist): `#7` (threat summary + trust boundaries), scope in `#1`/`#7`
- Mr H (Hazard): `#8`
- Mr R (Realist): `#7`, `#8` (assumptions + edge cases)
- Mr B (Builder): `#7`, `#9`, `#10` (controls + verification signals; `#10` maps to `#8`/edge cases)
- Mr Q (Qualifier): `#11`, `#12`
- Mr W (Writer): merge, dedupe, reconciliation, final KB

Mr QA (Query Assistant): interactive-only; not in this chain — see [`interactive-mode.md`](interactive-mode.md).

## `#9` gate

- Nếu `defensive_scope` **non-empty** → `#9` bắt buộc, ít nhất 2 verification signals.
- Nếu job plan bị bỏ qua: mặc định `defensive_scope` non-empty cho mọi AppSec research topic (trừ khi user chỉ yêu cầu pure theory).

## Subtopic splitting heuristics

Split khi các trục sau xuất hiện đồng thời và quá rộng:

- Mechanism semantics
- Trust boundaries & threat scenarios
- Defensive verification & observability signals

Confirm split khi user yêu cầu single doc **hoặc** `subtopics.length > 3`.
