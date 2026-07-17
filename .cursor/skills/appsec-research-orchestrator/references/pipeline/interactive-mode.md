# Interactive Mode (SSoT)

Single source of truth for interactive pipeline execution, checkpoints, resume, and amend protocol. Other docs link here; do not duplicate the full protocol elsewhere.

**Related**: [`role-glossary.md`](role-glossary.md) (personas), [`job-schema.md`](job-schema.md) (`execution_mode`, `interactive` state).

## Execution modes

| `execution_mode` | Description |
|------------------|-------------|
| `batch` (default) | Full pipeline in one response (except split confirmation) |
| `interactive` | One research role per turn + mandatory checkpoint |
| `qa-only` | Standalone Mr QA (Query Assistant); no job YAML required |
| `single-role` | One pipeline Mr only; no KB final |

## Interactive pipeline flow

```text
SecurityResearchJob (with interactive state)
  → [split confirm if required]
  → Mr A stub → Checkpoint
  → Mr S stub → Checkpoint
  → Mr H stub → Checkpoint
  → Mr R stub → Checkpoint
  → Mr B stub → Checkpoint
  → Mr Q stub → Checkpoint
  → Mr W stub → Checkpoint (optional: review before KB)
  → KB topic(s)
```

**Role order (normative)** — same as batch; see [`role-glossary.md`](role-glossary.md):

```text
Mr A (Analyst) → Mr S (Strategist) → Mr H (Hazard) → Mr R (Realist) → Mr B (Builder) → Mr Q (Qualifier) → Mr W (Writer)
```

## Per-turn output rules (interactive)

Each agent turn emits **at most one** primary block (do not combine):

| Turn type | Output |
|-----------|--------|
| Start / resume | `## SecurityResearchJob` (includes `interactive` state) |
| Role step | `## Role outputs (internal)` — **one role only** + `## Checkpoint` |
| Mr QA | `## Mr QA (Query Assistant)` + `## Checkpoint` (next role unchanged) |
| Final | `## KB topic(s)` (only after Mr W completes) |

**Gate**: In `interactive` mode, never emit more than one pipeline role stub per turn.

## Checkpoint block (mandatory)

After every role stub or Mr QA response in interactive mode, emit:

```markdown
## Checkpoint

**Mode**: interactive
**Subtopic**: <subtopic-id>
**Completed**: <Mr X (Mnemonic) or list>
**Next**: <Mr Y (Mnemonic)>
**Awaiting**: user_input

Reply with one of:
- `Proceed` — continue to next role
- `Ask Mr QA: <question>` — clarify (does not advance pipeline)
- `Amend Mr X: <changes>` — revise stub; invalidates downstream roles for this subtopic
- `Skip to Mr W` — merge completed stubs only (warn: incomplete pipeline)
- `Abort` — stop; preserve job state for resume
```

For split confirmation (before first role), use the same reply vocabulary plus `Approve split plan: ...` / `Merge to 1 doc: ...`.

## User reply vocabulary (normative)

| Reply | Agent behavior |
|-------|----------------|
| `Proceed` | Run next role in order for current subtopic |
| `Ask Mr QA: <question>` | Emit Mr QA answer + checkpoint; `next_role` unchanged |
| `Amend Mr X: <changes>` | Re-emit stub for Mr X; clear downstream stubs for same subtopic; update `invalidated_roles` in job YAML |
| `Approve split plan: ...` / `Merge to 1 doc: ...` | Re-emit job YAML; continue or restart from Mr A |
| `Skip to Mr W` | Mr W merges completed stubs only; warn about gaps |
| `Abort` | Set `interactive.status: aborted`; stop until resume |
| `Resume interactive` | Re-emit job YAML; continue from `next_role` |

## Interactive state (job YAML)

```yaml
execution_mode: "interactive"
interactive:
  status: "in_progress"  # in_progress | paused | completed | aborted
  current_subtopic_id: "cache-key-vary"
  next_role: "S"         # A | S | H | R | B | Q | W
  completed_roles:
    cache-key-vary: ["A"]
  invalidated_roles: []
  turn: 3
```

**Resume rule**: User sends `Resume interactive` plus job YAML (paste or reference). Agent re-emits updated job YAML, then continues from `next_role`. Stubs not in conversation context are **not valid** — ask user to re-paste or re-run from the missing role.

**Amend rule**: After `Amend Mr X`, do not emit `## KB topic(s)` until all roles from X through W are re-completed for that subtopic.

## Mr QA (Query Assistant)

Interactive-only persona; **not** in the A→W execution chain. Invoked on demand at checkpoints or via `qa-only` mode.

- Output heading: `## Mr QA (Query Assistant)`
- Does not advance `next_role`
- Contract: [`role-output-contract.md`](role-output-contract.md)

## Standalone modes

### `qa-only`

- No `SecurityResearchJob` required (optional topic context)
- Emit `## Mr QA (Query Assistant)` only
- May search `knowledge/` briefly if relevant
- No role stubs, no KB final

### `single-role`

- Required: `Role: Mr X (Mnemonic)`, `Topic`; optional `Question`
- Emit `## Role outputs (internal)` with one `### Mr X (...)` heading
- Follow role contract; no job YAML; no KB final
- Mutually exclusive with `interactive` in the same run

## Multi-subtopic nesting (interactive)

Subtopic-first structure under `## Role outputs (internal)`:

```markdown
## Role outputs (internal)

### Subtopic: cache-key-vary
#### Mr A (Analyst)
...
```

Single subtopic: use `### Mr A (Analyst)` (three hashes). Checkpoint always states `current_subtopic_id`.
