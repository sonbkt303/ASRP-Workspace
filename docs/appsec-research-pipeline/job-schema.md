# SecurityResearchJob Schema (runtime)

## Purpose
Schema chuẩn hóa mỗi lần research thành một job có thể điều phối. **Bắt buộc emit** trước khi viết nội dung KB final.

Runtime source of truth cho execution: `.cursor/skills/appsec-research-orchestrator/SKILL.md`.

## Emit contract (mandatory)

1. **When**: Sau pre-flight (dedup + category resolution), **trước** role stubs và KB final.
2. **Where**: Block YAML fenced đầu tiên trong response, heading `## SecurityResearchJob`.
3. **Gate**: Không viết `## Role outputs` hay KB final cho đến khi job plan đã emit.
4. **Confirmation**: Nếu `split_confirmation.required` là `true`, dừng và hỏi user trước khi tiếp tục.

## Job fields
```yaml
job_type: "security_research"
trigger: "chat"

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
  rule: "Every #10 item must map to #8 or Mr R edge case"
```

## Path resolution

- `proposed_path` = `knowledge/<folder>/<kebab-case>.md`
- `category` frontmatter có thể dùng slash (`networking/http`); **folder** luôn là segment đầu tiên (`networking/`).
- Ví dụ: `category: networking/http` → `knowledge/networking/tcp-overview.md`

## Section mapping (role -> KB blocks)
Execute **tuần tự** Mr A → Mr S → Mr B → Mr H → Mr R → Mr Q → Mr W (không gộp song song).

- Mr A: `#3`, `#4` (+ minimal `#1–#2`)
- Mr S: `#7` (threat summary + trust boundaries), scope in `#1`/`#7`
- Mr B: `#7`, `#9`, `#10` (controls + verification signals)
- Mr H: `#8`
- Mr R: `#7`, `#8` (assumptions + edge cases)
- Mr Q: `#11`, `#12`
- Mr W: merge, dedupe, reconciliation, final KB

## `#9` gate

- Nếu `defensive_scope` **non-empty** → `#9` bắt buộc, ít nhất 2 verification signals.
- Nếu job plan bị bỏ qua: mặc định `defensive_scope` non-empty cho mọi AppSec research topic (trừ khi user chỉ yêu cầu pure theory).

## Subtopic splitting heuristics
Split khi các trục sau xuất hiện đồng thời và quá rộng:
- Mechanism semantics
- Trust boundaries & threat scenarios
- Defensive verification & observability signals

Confirm split khi user yêu cầu single doc **hoặc** `subtopics.length > 3`.
