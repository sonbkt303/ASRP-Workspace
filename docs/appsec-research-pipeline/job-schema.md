# SecurityResearchJob Schema (design-time)

## Purpose
Đây là schema dùng để chuẩn hóa “mỗi lần research” thành một job có thể điều phối.
Trong phiên bản hiện tại, schema này chủ yếu phục vụ cho việc viết prompt/skill output contract.

## Job fields
```yaml
job_type: "security_research"
trigger: "chat"

root_topic: "<topic asked by user>"
category: "<repo taxonomy category; optional if inferable>"
difficulty: "<default intermediate>"
status: "<draft by default>"
tags: ["<optional>"]
prerequisites: "<optional>"

references_requirement: 
  - "RFC/standards (priority)"
  - "OWASP"
  - "official/vendor security guidance"

subtopics: 
  - id: "<short id>"
    subtopic_title: "<KB topic title>"
    theory_scope: "<what mechanisms to cover>"
    defensive_scope: "<what hardening/monitoring/verification to cover>"
    must_include_sections: ["#7", "#8", "#9", "#10"]
    evidence_targets: ["<RFC/OWASP keys if known>"]
```

## Section mapping (role -> KB blocks)
- Mr A (Security Researcher): `#3 Core Concepts`, `#4 How It Works` (+ minimal `#1-#2`)
- Mr S (Security Architect): `#7 Security Considerations` (threat summary + trust boundaries)
- Mr B (Defensive Security Engineer): `#7/#8/#9/#10` (controls + verification/observability)
- Mr H (Adversarial Security Engineer): `#8 Common Vulnerabilities / Mistakes`
- Mr R (Devil’s Advocate): `#7/#8` (assumptions + edge cases invalidate defenses)
- Mr Q (Knowledge Librarian): `#11/#12` (evidence-first links/refs)
- Mr W (Technical Writer): ensure template contract order and coherence

## Subtopic splitting heuristics
Split nếu thấy các trục sau xuất hiện đồng thời và quá rộng để giữ atomic:
- Mechanism semantics (what it is / how it works)
- Trust boundaries & threat scenarios (who can attack what)
- Defensive verification & observability signals (how to know it's correct)

