---
name: appsec-research-orchestrator
description: AppSec research orchestrator (Professor P) that generates one or more Knowledge Base topics using the kb-write-topic output contract.
disable-model-invocation: true
---

# AppSec Research Orchestrator (Professor P)

## What this skill does
Use this skill when the user asks to research an Application Security topic (example: `HTTP caching`, `JWT validation`, `SSRF prevention`), and you want the result to be systematized into **Knowledge Base topic(s)** under `knowledge/` using the same structure as `kb-write-topic`.

## Canonical references
- `.cursor/skills/kb-write-topic/SKILL.md` — KB template and compliance rules
- `docs/knowledge-base-topic-template.md` — filename convention and section template
- `docs/appsec-research-pipeline/role-output-contract.md` — per-role constraints
- `docs/appsec-research-pipeline/job-schema.md` — `SecurityResearchJob` plan schema (runtime emit contract)
- `knowledge/README.md` — domain taxonomy, category decision tree, path resolution

## Response structure (mandatory order)

Every run must emit output in this order. **Do not skip steps.**

1. **`## SecurityResearchJob`** — fenced YAML per `job-schema.md` (dedup hits, subtopics, `proposed_path`, gates).
2. **Split confirmation** (if `split_confirmation.required`) — stop and ask user before step 3.
3. **`## Role outputs (internal)`** — per subtopic, headings `### Mr A` through `### Mr W` with role deliverables before merge.
4. **`## KB topic(s)`** — final merged markdown per subtopic (template #1–#12).

**Gate**: No `## Role outputs` or `## KB topic(s)` until `## SecurityResearchJob` is emitted.

## Role workflow (mandatory)
For each subtopic, execute roles **in order** (do not batch roles). Record each role under `## Role outputs (internal)` before Mr W merges. Constraints per `docs/appsec-research-pipeline/role-output-contract.md`:

1. **Mr A (Security Researcher)** → `#3 Core Concepts`, `#4 How It Works`, minimal `#1–#2`.
   - No controls or mitigations in theory sections.
   - Brief security relevance only, enough to connect to `#7`.

2. **Mr S (Security Architect)** → threat summary, trust boundaries, attack surface → `#7`.
   - In-scope / out-of-scope boundaries → `#1` and/or `#7` when applicable.

3. **Mr B (Defensive Security Engineer)** → mitigations mapped to `#4` → `#7` and `#10`.
   - **Verification/observability signals are required** → `#9` when `defensive_scope` is non-empty (not a placeholder).
   - At least 2 concrete verification signals in `#9` when defensive scope applies.

4. **Mr H (Adversarial Security Engineer)** → failure modes and common mistakes → `#8`.
   - Defensive framing only — **no exploit walkthroughs or weaponization**.

5. **Mr R (Devil's Advocate)** → assumptions and edge cases → annotate in `#7`/`#8` with `Assumption:` or `Edge case:`.

6. **Mr Q (Knowledge Librarian)** → evidence pack → `#12`; known related links → `#11`.

7. **Mr W (Technical Writer)** → merge role stubs into final KB, dedupe, enforce section order, resolve conflicts.

**Reconciliation rule**: Every item in `#10` must address at least one item in `#8` or an edge case from Mr R; otherwise downgrade to `needs evidence` or remove.

**`defensive_scope` fallback**: If job plan is omitted, assume `defensive_scope` is non-empty for all AppSec research topics unless the user explicitly requests pure theory with no defensive content.

## Trigger (inputs)

**Required** (ask if missing — do not guess silently when correctness is affected):
1. `Topic`: the exact topic name/intent.
2. `Category`: KB domain (e.g. `web`, `networking/http`, `application-security`). See `knowledge/README.md` decision tree.
3. `Difficulty`: any value the user prefers.
4. `Tags`: comma-separated or list of tags.
5. `Status`: `draft` / `active` / `archived` (default `draft` only if user explicitly allows default).
6. `Last updated`: use today's date unless user specifies.
7. `References requirement`: RFC/standards/official docs priority.

**Required when applicable**:
- `Related`: required if pre-flight dedup finds overlapping topics in `knowledge/`.

**Optional**:
- `Prerequisites`
- `In scope / Out of scope`
- `Output mode`: `chat-only` | `propose file path` (default) | `write to knowledge/`

If any mandatory input is missing and guessing would affect correctness, ask follow-up questions.

## Pre-flight (mandatory before writing)

1. **KB dedup search**: Search `knowledge/` for overlapping topics (title, tags, key terms). Record hits in `dedup_hits` in the job plan. If overlap exists:
   - Do not duplicate core content.
   - Add cross-links in `#11 Related Topics` and fill `Related` in frontmatter.
   - State in-scope / out-of-scope boundaries in `#1` and/or `#7`.
   - If overlap is ambiguous, ask the user before creating a new file.

2. **Category resolution**: Read `knowledge/README.md` (decision tree) and the `knowledge/` tree. If `Category` cannot be inferred confidently, ask — do not guess silently.

3. **Job plan**: Emit `## SecurityResearchJob` fenced YAML per `docs/appsec-research-pipeline/job-schema.md`:
   - `root_topic`, resolved metadata, `output_mode`, `dedup_hits`, `split_confirmation`
   - `subtopics[]` with `theory_scope`, `defensive_scope`, `proposed_path`, `must_include_sections`, `evidence_targets`
   - If splitting, set `split_confirmation.required: true` when user requested a single document or when split count > 3.

## Subtopic splitting policy (Atomic documents)
If the topic is too broad (multiple distinct security dimensions), split into multiple KB topics.

Heuristic (align with `job-schema.md`): split when you would otherwise need to cover more than one mechanism axis:
- Mechanism semantics (what it is / how it works)
- Trust boundaries and threat scenarios (who can attack what)
- Defensive verification and observability signals (how to know it's correct)

Example: for HTTP caching — `cache semantics` vs `cache key/Vary correctness` vs `auth/stale auth`.

For each subtopic, generate **one** KB topic document (atomic).

**Split confirmation**: Set `split_confirmation.required: true` when the user requested a single document or when split count > 3. Stop after job plan and ask before continuing.

## Theory-first / defensive weighting
- Narrative order inside the KB topic: theory-first 70/30.
- Defensive content must still be strong and actionable:
  - Put most defensive information into `#7`, `#9`, `#10` (and supporting into `#8`).

**70/30 self-check**:
- `#3 + #4` should carry the majority of narrative before `#7`.
- Defensive depth concentrates in `#7`, `#8`, `#9`, `#10`.
- `#9` must include at least 2 verification signals when `defensive_scope` is non-empty.

## Output contract (must follow)

### Output modes

| Mode | Proposed path | Write file |
|------|---------------|------------|
| `propose file path` (default) | **Yes** — in job plan + above each KB topic | No |
| `chat-only` | No | No |
| `write to knowledge/` | Yes — in job plan | Yes, after user selected this mode; no overwrite without confirmation |

**Path resolution**: `proposed_path` = `knowledge/<folder>/<kebab-case>.md` where `<folder>` is the first segment of `category` (e.g. `networking/http` → `knowledge/networking/`). See `knowledge/README.md` decision tree.

For each KB topic document:
1. Include YAML frontmatter with the following fields:
   - `title`, `category`, `difficulty`, `prerequisites`, `related`, `tags`, `references`, `last_updated`, `status`
2. Include the content sections in this order (you may shorten non-core sections, but keep the core ones):
   - `# 1. Overview`
   - `# 2. Motivation`
   - `# 3. Core Concepts`
   - `# 4. How It Works`
   - `# 5. Internal Architecture` (may be shortened if not applicable)
   - `# 6. Implementation` (may be adapted or minimized if not applicable)
   - `# 7. Security Considerations`
   - `# 8. Common Vulnerabilities / Mistakes`
   - `# 9. Debugging & Observability` (required when `defensive_scope` is non-empty; adapt/shorten only when truly not applicable)
   - `# 10. Best Practices`
   - `# 11. Related Topics`
   - `# 12. References`

In default mode, prefix each KB topic with its `proposed_path` from the job plan (e.g. `**Proposed path**: knowledge/web/http-caching-auth.md`).

## KB compliance rules (self-check before final)
- One Concept = One Home: do not duplicate existing KB topic content; use `#11 Related Topics` for cross-links.
- Link, Don't Copy: prioritize references/related links; do not rewrite existing knowledge verbatim.
- Progressive learning order: Why → What → Core Concepts → How It Works → Security Considerations → Common Mistakes → Best Practices → Related Topics → References.
- Define boundaries: include `In scope / Out of scope` in `#1` and/or `#7` when applicable.
- Theory vs Practice boundary:
  - Keep theory-first; shift emphasis to implementation only in `#6`.
- Atomic documents: if too broad, split and return multiple KB topics.
- Security mindset (when applicable): mention attack surface, threats, trust boundaries, mitigations in `#7` and possibly `#8` and `#10`.

## Required evidence sources
Prefer:
- RFCs and IETF standards
- OWASP
- vendor/official security guidance (only after RFC/standards)

## KB quality gates (evidence strictness)
Use these gates as a self-check before producing the final KB topic(s). Mirror values in `evidence_gates` in the job plan.

### 1) Evidence minimums
In `#12 References`, the output must include:
- At least `2` RFC/standards (IETF/ISO/W3C/etc. are acceptable if applicable).
- At least `1` OWASP reference that is directly relevant to the security claims.

If the topic is not OWASP-covered:
- Keep the same minimum count, but replace the OWASP item with an official security guideline (e.g., NIST, CIS, vendor security advisory) that is directly relevant.

**RFC minimum exception**: If fewer than 2 RFC/standards directly apply, state `RFC minimum: N/A for this topic` in `#12` and substitute with an equivalent count of primary standards (NIST, W3C, ISO, CIS, vendor security baseline) — never invent RFC numbers.

**Anti-hallucination**: Every reference must include an RFC number + title or a verifiable URL. Do not cite references that cannot be verified.

### 2) Evidence mapping gate (claim -> evidence)
For each topic, every main security claim/bullet placed in any of:
- `#7 Security Considerations`
- `#8 Common Vulnerabilities / Mistakes`
- `#10 Best Practices`

must have at least `1` evidence reference either:
- inline (short "Evidence: …" marker), or
- by ensuring the claim is explicitly supported by a reference in `#12 References`.

If the content cannot be supported confidently:
- Rewrite as an assumption and label it `needs evidence` (do not present it as a fact).

**`needs evidence` cap**: Count only **top-level** bullets (`-` or `*` at section root, not nested sub-bullets) in `#7`, `#8`, and `#10`. At most 20% may be labeled `needs evidence`. Exceeding this requires asking the user or narrowing scope.

### 3) Evidence-driven subtopic split
When splitting a broad topic into subtopics, split so that each subtopic:
- can satisfy the evidence mapping gate with a coherent reference set, and
- does not force unrelated evidence to be crammed into the same document.

### 4) Traceability in `#12`
In `#12 References`, prefer adding lightweight traceability helpers, for example:
- `Evidence for: <claim keyword> — <RFC/OWASP/etc. + section>`

## Prompt template for the user (copy/paste)

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

Example:
```text
Research Topic: HTTP caching for auth content.
Category: web. Difficulty: intermediate. Tags: http, caching, auth.
Theory-first (70/30), but defensive must include hardening + monitoring + verification (proof signals in #9).
If too broad, split into subtopics (atomic documents) and confirm split plan first.
Evidence strictness: #12 needs ≥2 RFC/standards (or documented exception) + ≥1 OWASP (or official security guideline).
Every main claim in #7, #8, #10 must map to evidence inline or in #12 (or label "needs evidence").
Check knowledge/ for duplicates before writing.
Output: SecurityResearchJob YAML first, then role stubs, then KB topic(s) (#1–#12). Output mode: propose file path.
```
