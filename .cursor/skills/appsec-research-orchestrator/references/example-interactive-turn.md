# Example: Interactive Turn (truncated)

Reference for `execution_mode: interactive`. Full protocol: [`pipeline/interactive-mode.md`](pipeline/interactive-mode.md).

## Turn 1 — Job plan + first role

## SecurityResearchJob

```yaml
job_type: "security_research"
execution_mode: "interactive"
root_topic: "HTTP cache key and Vary correctness"
category: "web"
difficulty: "intermediate"
status: "draft"
tags: ["http", "caching", "vary"]
last_updated: "2026-07-17"
output_mode: "propose file path"
split_confirmation:
  required: false
subtopics:
  - id: "cache-key-vary"
    subtopic_title: "HTTP Cache Key and Vary Header Correctness"
    proposed_path: "knowledge/web/http-cache-key-vary.md"
    theory_scope: "Cache key derivation, Vary semantics"
    defensive_scope: "Mis-cache prevention, verification signals"
interactive:
  status: "in_progress"
  current_subtopic_id: "cache-key-vary"
  next_role: "S"
  completed_roles:
    cache-key-vary: ["A"]
  invalidated_roles: []
  turn: 1
```

## Role outputs (internal)

### Subtopic: cache-key-vary

#### Mr A (Analyst)

**#3 Core Concepts**
- Cache key: tuple of request attributes the cache uses to store and match entries.
- `Vary`: response header listing request fields that must match for cache reuse.

**#4 How It Works**
1. Origin responds with `Cache-Control` and optional `Vary`.
2. Shared cache stores entry keyed by URL + listed Vary fields.
3. Subsequent requests match only if Vary-listed headers match stored variant.

## Checkpoint

**Mode**: interactive
**Subtopic**: cache-key-vary
**Completed**: Mr A (Analyst)
**Next**: Mr S (Strategist)
**Awaiting**: user_input

Reply with one of:
- `Proceed` — continue to next role
- `Ask Mr QA: <question>` — clarify (does not advance pipeline)
- `Amend Mr A: <changes>` — revise stub; invalidates downstream roles for this subtopic
- `Skip to Mr W` — merge completed stubs only (warn: incomplete pipeline)
- `Abort` — stop; preserve job state for resume

---

## Turn 2 — User asks Mr QA (pipeline does not advance)

**User reply:**

```text
Ask Mr QA: Why does Vary: Cookie often cause cache fragmentation?
```

**Agent output:**

## Mr QA (Query Assistant)

`Vary: Cookie` tells caches to treat each distinct `Cookie` value as a separate variant. Authenticated apps send per-user or per-session cookies, so the cache stores many single-user entries instead of one shared entry — **cache fragmentation**. Shared caches may see little benefit; sometimes this is intentional (private data) but often it is a misconfiguration when the response body is identical for all users.

**Suggestion**: Proceed to Mr S to frame trust boundaries (who shares the cache). If fragmentation is unintended, consider `Cache-Control: private` or narrowing what varies.

## Checkpoint

**Mode**: interactive
**Subtopic**: cache-key-vary
**Completed**: Mr A (Analyst)
**Next**: Mr S (Strategist)
**Awaiting**: user_input

---

## Turn 3 — User amends prior stub

**User reply:**

```text
Amend Mr A: Add note that Accept-Encoding is commonly part of the cache key even when not in Vary.
Proceed
```

**Agent behavior:** Re-emit Mr A stub with amendment; clear downstream stubs for `cache-key-vary`; update job YAML `invalidated_roles`; then emit Mr S stub + checkpoint with `next_role: "H"`.

---

## Notes

- Stubs not in conversation context are not valid on `Resume interactive` — re-paste job YAML or re-run from missing role.
- `qa-only` and `single-role` examples are in [`pipeline/prompt-template.md`](pipeline/prompt-template.md).
