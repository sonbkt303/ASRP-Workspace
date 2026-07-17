---
name: kb-write-topic
description: Create a Knowledge Base topic document that follows KB rules and the topic template. Use when the user asks to write a new Knowledge Base topic (e.g., "HTTP caching for auth content").
disable-model-invocation: true
---

# KB Write Topic (template + rules)

## When to use
Use this skill when the user asks to write a new Knowledge Base topic document for the security Knowledge Base (for example: “HTTP caching for auth content”, “HTTP cache-control”, “Vary header”, “HTTP status codes and client interpretation”).

## Inputs to collect (ask if missing)
1. `Topic`: the exact topic name/intent (required).
2. `Category`: the KB domain/category (required). Example format: `networking/http`, etc.
3. `Difficulty`: any value the user prefers (required).
4. `Prerequisites`: what the reader should already know (optional but fill if possible).
5. `Tags`: comma-separated or list of tags (required).
6. `Status`: draft/active/archived (required).
7. `Last updated`: use today’s date unless user specifies (required).
8. `References`: RFC/standards/official docs/books/research (required).
9. `Related`: related KB topics/links (required if known; otherwise ask).
10. `In scope / Out of scope`: required if the topic/domain makes it applicable (otherwise incorporate boundaries into Overview and/or Security Considerations).

If any of the above are not provided, ask follow-up questions. Do not guess silently when it affects correctness (especially `Category`, `Difficulty`, and `References`).

## Output contract (must follow)
Return a single markdown document that includes:

1. YAML Frontmatter that matches the template fields:
   - `title`, `category`, `difficulty`, `prerequisites`, `related`, `tags`, `references`, `last_updated`, `status`

2. The content sections in this order (you may shorten/omit sections if not applicable, but keep the core sections):
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
Before finalizing, run this checklist. If any item fails, fix and re-check.

- Filename suggestion: propose a kebab-case/lowercase filename for a new `knowledge/` file (do not include it in output unless the user asks). Use this only for internal validation.
- One Concept = One Home: if the topic overlaps with an existing topic, do not duplicate content; put cross-links in `# 11. Related Topics` instead and ask for confirmation if ambiguous.
- Link, Don't Copy: prioritize references/related links; do not rewrite existing knowledge verbatim.
- Progressive Learning order: ensure narrative flows `Why → What → Core Concepts → How It Works → Security Considerations → Common Mistakes → Best Practices → Related Topics → References`.
- Knowledge Before Opinion: references prioritize RFC/standards/official docs; personal notes (if any) go last.
- Theory vs Practice boundary:
  - If it is theory, keep it in “knowledge” style.
  - If it is implementation guidance, shift emphasis to “apps/labs” and clearly label implementation guidance in `# 6. Implementation`.
- Atomic documents: avoid including multiple unrelated concepts; if the topic is too broad, ask which subtopic to write first.
- Define boundaries: include `In scope / Out of scope` inside `# 1. Overview` and/or `# 7. Security Considerations` when applicable.
- Security mindset (when applicable): mention attack surface, threats, trust boundaries, and mitigations in `# 7. Security Considerations` (and possibly `# 8` and `# 10`).

## Sample prompts
Copy one of these prompts and replace the topic:

### HTTP caching
User prompt:
Write a new Knowledge Base topic about HTTP caching.

### HTTP caching for auth content
User prompt:
Write a new Knowledge Base topic about HTTP caching for auth content. Focus on preventing cross-user data leakage and stale authorization.

### HTTP security headers (theory-first)
User prompt:
Write a Knowledge Base topic about HTTP security headers. Keep it theory-first (attack surface, threats, mitigations).

### HTTP status codes
User prompt:
Write a Knowledge Base topic about HTTP status codes and how clients should interpret them.

## Examples (how the output should look)
Example 1: HTTP caching
- Use the required frontmatter fields.
- Strong `# 7. Security Considerations` (cache poisoning, stale content, auth header/cookie caching issues).

Example 2: HTTP security headers (theory-first)
- Keep theory-first framing.
- Make `# 7` and `# 10` strong; keep implementation minimal unless requested.
