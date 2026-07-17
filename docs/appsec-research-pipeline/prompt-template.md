# AppSec Research Prompt Template

Invoke the skill explicitly (`disable-model-invocation: true`):

```text
Use appsec-research-orchestrator (Mr P — Professional).
```

Protocol reference: [`interactive-mode.md`](interactive-mode.md).

## Batch (default)

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: batch.

Research Topic: <topic>.
Category: <category>. Difficulty: <level>. Tags: <tags>.
Status: draft. Last updated: <YYYY-MM-DD>.
References requirement: RFC/standards first, then OWASP.
Theory-first (70/30), but defensive must include hardening + monitoring + verification (proof signals in #9).
If too broad, split into subtopics (atomic documents) and confirm split plan first.
Evidence strictness: #12 needs ≥2 RFC/standards (or documented exception) + ≥1 OWASP (or official security guideline).
Every main claim in #7, #8, #10 must map to evidence inline or in #12 (or label "needs evidence").
Check knowledge/ for duplicates before writing.
Output: SecurityResearchJob YAML first, then role stubs, then KB topic(s) (#1–#12). Output mode: propose file path.
```

## Interactive (pause after each role)

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: interactive.

Research Topic: SSRF prevention in microservices.
Category: application-security. Difficulty: intermediate.
Tags: ssrf, microservices, egress.
Status: draft. Last updated: <YYYY-MM-DD>.
References requirement: RFC/standards first, then OWASP.
Output mode: propose file path.
```

After each role, reply with one of:

```text
Proceed
```

```text
Ask Mr QA: What is the difference between egress filtering and SSRF allowlists?
```

```text
Amend Mr H: Add failure mode for DNS rebinding in internal metadata access.
```

```text
Abort
```

Resume later:

```text
Resume interactive
[paste or reference prior SecurityResearchJob YAML]
Proceed
```

Split confirmation (when required):

```text
Approve split plan: all 3 subtopics. Proceed.
```

```text
Merge to 1 doc: SSRF prevention overview. Proceed.
```

## Qa-only (Mr QA standalone)

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: qa-only.

Topic: HTTP cache poisoning.
Ask Mr QA: When should I use Vary: Cookie vs marking responses private?
```

## Single-role (one Mr, no KB final)

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: single-role.

Role: Mr H (Hazard).
Topic: JWT alg confusion.
Question: List common failure modes (defensive framing only).
```

Other roles: `Mr A (Analyst)`, `Mr S (Strategist)`, `Mr R (Realist)`, `Mr B (Builder)`, `Mr Q (Qualifier)`.
