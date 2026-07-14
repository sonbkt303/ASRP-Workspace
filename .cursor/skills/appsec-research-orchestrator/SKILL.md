---
name: appsec-research-orchestrator
description: AppSec research orchestrator (Professor P) that generates one or more Knowledge Base topics using the kb-write-topic output contract.
---

# AppSec Research Orchestrator (Professor P)

## What this skill does
Use this skill when the user asks to research an Application Security topic (example: `HTTP caching`, `JWT validation`, `SSRFi prevention`), and you want the result to be systematized into **Knowledge Base topic(s)** under `knowledge/` using the same structure as `kb-write-topic`.

This skill implements the team workflow as sections inside the final output:
- Mr A (Security Researcher): theory-first mechanism
- Mr S (Security Architect): brief threat-model & trust boundaries
- Mr B (Defensive Security Engineer): hardening + monitoring + verification signals (defensive)
- Mr H (Adversarial Security Engineer): failure modes / attack perspectives mapped into "Common Vulnerabilities / Mistakes"
- Mr R (Devil's Advocate): assumptions + edge cases that could invalidate defenses
- Mr Q (Knowledge Librarian): reference evidence (RFC/standards/official docs/OWASP)
- Mr W (Technical Writer): assemble all content into the KB template contract

## Trigger (inputs)
The user must provide at least:
1. `Topic`: the exact topic name/intent.
2. `Category` (optional if you can infer reasonably from repo taxonomy; otherwise ask).
3. `Difficulty` (optional; otherwise default to `intermediate`).
4. `Prerequisites` (optional).
5. `Tags` (optional; otherwise infer).
6. `Status` (optional; otherwise default to `draft`).
7. `References requirement`: at least RFC/standards/official docs priority.

If any mandatory input is missing and guessing would affect correctness, ask follow-up questions.

## Subtopic splitting policy (Atomic documents)
If the topic is too broad (multiple distinct security dimensions), split into multiple KB topics.
Heuristic: split when you would otherwise need to cover more than one "mechanism axis" (e.g., for HTTP caching: `cache semantics` vs `cache key/Vary correctness` vs `auth/stale auth`).

For each subtopic, generate **one** KB topic document (atomic).

## Theory-first / defensive weighting
- Narrative order inside the KB topic: theory-first 70/30.
- Defensive content must still be strong and actionable:
  - Put most defensive information into `# 7`, `# 9`, `# 10` (and supporting into `# 8`).

## Output contract (must follow)
Return one or more KB topic markdown documents.

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
   - `# 9. Debugging & Observability` (adapt/shorten if not applicable)
   - `# 10. Best Practices`
   - `# 11. Related Topics`
   - `# 12. References`

## KB compliance rules (self-check before final)
- One Concept = One Home: do not duplicate existing KB topic content; use `# 11. Related Topics` for cross-links.
- Link, Don't Copy: prioritize references/related links; do not rewrite existing knowledge verbatim.
- Progressive learning order: Why → What → Core Concepts → How It Works → Security Considerations → Common Mistakes → Best Practices → Related Topics → References.
- Theory vs Practice boundary:
  - Keep theory-first; shift emphasis to implementation only in `# 6`.
- Atomic documents: if too broad, split and return multiple KB topics.
- Security mindset (when applicable): mention attack surface, threats, trust boundaries, mitigations in `# 7` and possibly `# 8` and `# 10`.

## Required evidence sources
Prefer:
- RFCs and IETF standards
- OWASP
- vendor/official security guidance (only after RFC/standards)

## Prompt template for the user (copy/paste)
Example:
`Research Topic: HTTP caching for auth content. Theory-first (70/30), but defensive must include hardening + monitoring + verification. Split into subtopics if needed. Provide RFC/OWASP references.`

