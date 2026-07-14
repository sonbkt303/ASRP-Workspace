# Role Output Contract (runtime prompt design)

## Goal
Mỗi “role” tạo output theo đúng vai trò để Technical Writer (Mr W) ghép thành KB topic(s).

## Contracts

### Mr A (Security Researcher) - Theory-first mechanism
- Provide:
  - Definitions/terminology for `#3 Core Concepts`
  - Step-by-step explanation for `#4 How It Works`
- Constraints:
  - Không đi sâu vào controls/mitigations trong phần này
  - Chỉ nhắc brief “security relevance” đủ để nối sang `#7`

### Mr S (Security Architect) - Threat summary & trust boundaries
- Provide:
  - Threat summary, trust boundaries, attack surface framing for `#7`
  - What is in-scope/out-of-scope at a high level (can be in `#1` and/or `#7`)

### Mr B (Defensive Security Engineer) - Hardening + monitoring + verification
- Provide:
  - Concrete mitigations mapped to the mechanism described in `#4`
  - Verification/observability signals mapped into `#9`
  - Actionable best practices in `#10`

### Mr H (Adversarial Security Engineer) - Attack-oriented failure modes
- Provide:
  - Common vulnerabilities/mistakes for `#8`
  - Failure modes that defensive controls must address

### Mr R (Devil's Advocate) - Assumptions & edge cases
- Provide:
  - Assumptions that could be wrong
  - Edge cases and “where defenses fail” bổ sung cho `#7/#8`

### Mr Q (Knowledge Librarian) - Evidence pack
- Provide:
  - Evidence-first references for `#12`
  - Related topic links for `#11` (when known)

### Mr W (Technical Writer) - Assembly into KB template
- Provide:
  - Final KB topic(s) that strictly follow:
    - YAML frontmatter fields
    - Section order:
      `#1 Overview` → `#2 Motivation` → `#3 Core Concepts` → `#4 How It Works` →
      `#5 Internal Architecture` (optional/shorten) → `#6 Implementation` →
      `#7 Security Considerations` → `#8 Common Vulnerabilities / Mistakes` →
      `#9 Debugging & Observability` → `#10 Best Practices` →
      `#11 Related Topics` → `#12 References`
  - Ensure theory-first 70/30 balance in narrative.

