# AppSec Research Prompt Template

Copy/paste and replace placeholders:

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
