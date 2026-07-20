# Role Output Contract (runtime prompt design)

## Goal

Mỗi role tạo output theo đúng vai trò để Mr W (Writer) ghép thành KB topic(s).

**Persona names (SSoT)**: [`role-glossary.md`](role-glossary.md)

**Interactive protocol (SSoT)**: [`interactive-mode.md`](interactive-mode.md)

## Contracts

### Mr A (Analyst) - Theory-first mechanism

- Provide:
  - Definitions/terminology for `#3 Core Concepts`
  - Step-by-step explanation for `#4 How It Works`
- Constraints:
  - Không đi sâu vào controls/mitigations trong phần này
  - Chỉ nhắc brief “security relevance” đủ để nối sang `#7`

### Mr S (Strategist) - Threat summary & trust boundaries

- Provide:
  - Threat summary, trust boundaries, attack surface framing for `#7`
  - What is in-scope/out-of-scope at a high level (can be in `#1` and/or `#7`)

### Mr H (Hazard) - Attack-oriented failure modes

- Provide:
  - Common vulnerabilities/mistakes for `#8`
  - Failure modes that defensive controls must address
- Constraints:
  - Defensive framing only — **no exploit walkthroughs or weaponization**

### Mr R (Realist) - Assumptions & edge cases

- Provide:
  - Assumptions that could be wrong
  - Edge cases and “where defenses fail” bổ sung cho `#7/#8`
- Label outputs with `Assumption:` or `Edge case:` in `#7`/`#8`

### Mr B (Builder) - Hardening + monitoring + verification

- Provide:
  - Concrete mitigations mapped to the mechanism described in `#4`
  - Verification/observability signals mapped into `#9`
  - Actionable best practices in `#10`
- Constraints:
  - `#9` verification signals are **required** when `defensive_scope` is non-empty (at least 2 concrete signals)
  - Do not reduce `#9` to a placeholder when defensive content is in scope
  - Each `#10` item must include `Maps to #8:` or `Maps to edge case:` (Mr R) — `#8` and edge cases exist before Mr B runs

### Mr Q (Qualifier) - Evidence pack

- Provide:
  - Evidence-first references for `#12`
  - Related topic links for `#11` (when known)
  - In interactive mode: optional `Evidence gap:` list for claims from prior stubs

### Mr W (Writer) - Assembly into KB template

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
  - Merge role stubs from `## Role outputs (internal)` into final KB; dedupe and resolve conflicts.

**Reconciliation rule (Mr W)**: Every item in `#10` must address at least one item in `#8` or an edge case from Mr R (Realist); otherwise downgrade to `needs evidence` or remove.

### Mr QA (Query Assistant) - Interactive Q&A

**Interactive-only** — not in the A→W pipeline chain.

- Provide:
  - Plain-language answers about the topic, prior stubs, terminology, tradeoffs
  - Summary of what the last role stub means
  - Suggestions: user should `Proceed`, `Amend`, or narrow scope
- Constraints:
  - Does **not** emit KB sections (`#1–#12`) or pipeline role stubs
  - Does **not** advance `next_role` in interactive state
  - Cite evidence when possible; label uncertain claims `needs evidence`
  - Defensive framing only — no exploit walkthroughs (same as Mr H)
- Output heading: `## Mr QA (Query Assistant)`

## Execution order (normative)

Roles execute **sequentially** Mr A (Analyst) → Mr S (Strategist) → Mr H (Hazard) → Mr R (Realist) → Mr B (Builder) → Mr Q (Qualifier) → Mr W (Writer).

- **Batch mode**: record all roles under `## Role outputs (internal)` before Mr W merges.
- **Interactive mode**: one role per turn + checkpoint — see [`interactive-mode.md`](interactive-mode.md). Do not batch.

## Standalone single-role contract

When `execution_mode: single-role`:

- Required input: `Role: Mr X (Mnemonic)`, `Topic`; optional `Question`
- Emit `## Role outputs (internal)` with **one** `### Mr X (...)` heading only
- Follow the contract for that role above
- No `SecurityResearchJob`, no `## KB topic(s)`
- Mutually exclusive with `interactive` in the same run
