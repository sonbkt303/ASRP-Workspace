---
name: appsec-research-orchestrator
description: AppSec research orchestrator (Mr P — Professional) that generates one or more Knowledge Base topics using the kb-write-topic output contract. Supports batch, interactive, qa-only, and single-role modes.
disable-model-invocation: true
---

# AppSec Research Orchestrator (Mr P — Professional)

## What this skill does

Use this skill when the user asks to research an Application Security topic (example: `HTTP caching`, `JWT validation`, `SSRF prevention`), and you want the result to be systematized into **Knowledge Base topic(s)** under `knowledge/` using the same structure as `kb-write-topic`.

Supports **batch** (default), **interactive** (pause after each role), **qa-only** (Mr QA Q&A), and **single-role** (one Mr without KB final).

## How to invoke

Because `disable-model-invocation: true`, invoke explicitly:

1. `@appsec-research-orchestrator` in Cursor chat, or
2. First line: `Use appsec-research-orchestrator (Mr P — Professional).`

Set `Execution mode:` in the prompt (default `batch` if omitted). User guide (Vietnamese): [`references/pipeline/USER-GUIDE.md`](references/pipeline/USER-GUIDE.md). Full prompts: [`references/pipeline/prompt-template.md`](references/pipeline/prompt-template.md).

## Skill routing

| Skill / mode | When to use |
|--------------|-------------|
| **`appsec-research-orchestrator`** + `batch` | Full KB research in one response |
| **`appsec-research-orchestrator`** + `interactive` | Review each Mr; ask/amend between steps |
| **`appsec-research-orchestrator`** + `qa-only` | Quick Q&A via Mr QA (Query Assistant) |
| **`appsec-research-orchestrator`** + `single-role` | One Mr output (threat, failure modes, evidence, etc.) |
| **`kb-write-topic`** | Write one KB topic quickly without multi-role pipeline |

## Canonical references

- `references/pipeline/USER-GUIDE.md` — user guide (Vietnamese): team, scenarios, how to invoke
- `~/.cursor/skills/kb-write-topic/SKILL.md` (or project `.cursor/skills/kb-write-topic/SKILL.md`) — KB template and compliance rules
- `references/knowledge-base-topic-template.md` — filename convention and section template
- `references/pipeline/role-glossary.md` — persona names (SSoT)
- `references/pipeline/role-output-contract.md` — per-role constraints
- `references/pipeline/interactive-mode.md` — interactive checkpoint, resume, amend (SSoT)
- `references/pipeline/job-schema.md` — `SecurityResearchJob` plan schema
- Target repo `knowledge/README.md` if present; else `references/knowledge-taxonomy.md` — domain taxonomy, category decision tree, path resolution
- `references/example-interactive-turn.md` — interactive example

## Knowledge base resolution (cross-project)

1. **Dedup search**: If target repo has `knowledge/`, search it for overlaps. If absent, note in job plan that dedup was skipped.
2. **Category taxonomy**: Prefer target repo `knowledge/README.md`. Fallback: `references/knowledge-taxonomy.md`.
3. **Output path**: `knowledge/<folder>/<kebab-case>.md` — folder = first segment of `category`.

## Execution modes

| `execution_mode` | Behavior |
|------------------|----------|
| `batch` (default) | Full flow in one response (except split confirmation) |
| `interactive` | One pipeline role per turn + mandatory `## Checkpoint` |
| `qa-only` | Emit `## Mr QA (Query Assistant)` only; no job YAML required |
| `single-role` | One `### Mr X (...)` stub; no job YAML; no KB final |

Protocol details: [`references/pipeline/interactive-mode.md`](references/pipeline/interactive-mode.md).

## Response structure

Branch on `execution_mode`. **Do not skip steps** within the chosen mode.

### Batch (`execution_mode: batch` or omitted)

1. **`## SecurityResearchJob`** — fenced YAML per `job-schema.md`.
2. **Split confirmation** (if `split_confirmation.required`) — stop before step 3.
3. **`## Role outputs (internal)`** — all roles per subtopic (`### Mr A (Analyst)` … `### Mr W (Writer)`).
4. **`## KB topic(s)`** — final merged markdown per subtopic (#1–#12).

**Gate**: No `## Role outputs` or `## KB topic(s)` until `## SecurityResearchJob` is emitted.

### Interactive (`execution_mode: interactive`)

Per turn, emit **at most one** of:

| Turn | Output |
|------|--------|
| Start / resume | `## SecurityResearchJob` (with `interactive` state) |
| Role step | `## Role outputs (internal)` — **one role** + `## Checkpoint` |
| Mr QA | `## Mr QA (Query Assistant)` + `## Checkpoint` |
| Final | `## KB topic(s)` (after Mr W) |

**Gates**:
- Never emit more than one pipeline role stub per turn.
- After `Amend Mr X`, do not emit KB final until roles X→W are re-completed for that subtopic.
- Mr QA does not advance `next_role`.

Checkpoint and reply vocabulary: [`references/pipeline/interactive-mode.md`](references/pipeline/interactive-mode.md).

### Qa-only (`execution_mode: qa-only`)

- Emit **`## Mr QA (Query Assistant)`** only.
- No `SecurityResearchJob`, no role stubs, no KB final.
- May search `knowledge/` briefly if relevant.

### Single-role (`execution_mode: single-role`)

- Required: `Role: Mr X (Mnemonic)`, `Topic`; optional `Question`.
- Emit **`## Role outputs (internal)`** with one `### Mr X (...)` heading.
- No `SecurityResearchJob`, no KB final. Mutually exclusive with `interactive`.

## Role workflow (mandatory for batch and interactive)

For each subtopic, execute roles **in order** (do not batch in one turn except batch mode at end). Constraints per `role-output-contract.md`; names per `role-glossary.md`:

1. **Mr A (Analyst)** → `#3 Core Concepts`, `#4 How It Works`, minimal `#1–#2`.
   - No controls or mitigations in theory sections.

2. **Mr S (Strategist)** → threat summary, trust boundaries, attack surface → `#7`.
   - In-scope / out-of-scope → `#1` and/or `#7`.

3. **Mr H (Hazard)** → failure modes and common mistakes → `#8`.
   - Defensive framing only — **no exploit walkthroughs**.

4. **Mr R (Realist)** → assumptions and edge cases → `#7`/`#8` with `Assumption:` or `Edge case:`.

5. **Mr B (Builder)** → mitigations → `#7` and `#10`; verification → `#9`.
   - At least 2 verification signals in `#9` when `defensive_scope` is non-empty.
   - Each `#10` item: `Maps to #8:` or `Maps to edge case:`.

6. **Mr Q (Qualifier)** → evidence pack → `#12`; related links → `#11`.

7. **Mr W (Writer)** → merge stubs into final KB, dedupe, reconciliation, quality gates.

**Mr QA (Query Assistant)**: on-demand at checkpoints or `qa-only`; not in the chain above.

**Reconciliation rule**: Every item in `#10` must address at least one item in `#8` or an edge case from Mr R (Realist).

**`defensive_scope` fallback**: If job plan is omitted, assume non-empty unless user requests pure theory only.

## Trigger (inputs)

**Required** for `batch` / `interactive` (ask if missing):
1. `Topic`, `Category`, `Difficulty`, `Tags`, `Status`, `Last updated`, `References requirement`
2. `Related`: if pre-flight dedup finds overlaps

**Required** for `single-role`:
- `Role: Mr X (Mnemonic)`, `Topic`

**Required** for `qa-only`:
- `Topic` or question context

**Optional**:
- `Execution mode`: `batch` | `interactive` | `qa-only` | `single-role` (default `batch`)
- `Prerequisites`, `In scope / Out of scope`
- `Output mode`: `chat-only` | `propose file path` (default) | `write to knowledge/`

## Pre-flight (mandatory for batch and interactive)

1. **KB dedup search**: Search `knowledge/` in target repo if present. Record hits in `dedup_hits`. Set `legacy_format: true` for files without YAML frontmatter or lifecycle headings. Cross-link; do not duplicate core content.
2. **Category resolution**: Per target repo `knowledge/README.md`, else `references/knowledge-taxonomy.md`; ask if uncertain.
3. **Job plan**: Emit `## SecurityResearchJob` with `execution_mode`, `interactive` state when interactive, `split_confirmation`, `subtopics[]`.

**Split confirmation**: `split_confirmation.required: true` when user wants single doc or split count > 3. Stop after job plan. Resume per [`references/pipeline/interactive-mode.md`](references/pipeline/interactive-mode.md).

## Subtopic splitting policy

Split when topic spans multiple mechanism axes (semantics, trust/threat, verification). One KB topic per subtopic. See `job-schema.md`.

Multi-subtopic role output nesting (interactive): subtopic-first — `### Subtopic: <id>` then `#### Mr X (...)`. Single subtopic: `### Mr X (...)`.

## Theory-first / defensive weighting

- Theory-first 70/30; defensive depth in `#7`–`#10`.
- `#9` required with ≥2 signals when `defensive_scope` non-empty.

## Output contract (must follow)

### Output modes (file delivery)

| Mode | Proposed path | Write file |
|------|---------------|------------|
| `propose file path` (default) | Yes | No |
| `chat-only` | No | No |
| `write to knowledge/` | Yes | Yes after user chose mode; no overwrite without confirm |

**Path resolution**: `knowledge/<folder>/<kebab-case>.md` — folder = first segment of `category`.

KB sections #1–#12 per template (see `kb-write-topic`). Prefix `**Proposed path**:` in default mode.

## KB compliance rules (self-check before final)

- One Concept = One Home; link don't copy.
- Progressive learning order; atomic documents; boundaries in `#1`/`#7`.

## KB quality gates (evidence strictness)

Mirror `evidence_gates` in job plan:

- `#12`: ≥2 RFC/standards (or documented exception) + ≥1 OWASP or official guideline.
- Claims in `#7`, `#8`, `#10` map to evidence or `needs evidence` (≤20% top-level bullets).
- Anti-hallucination: verifiable references only.

## Prompt template

See [`references/pipeline/prompt-template.md`](references/pipeline/prompt-template.md). Invoke:

```text
Use appsec-research-orchestrator (Mr P — Professional).
```

Batch example adds research fields; interactive/qa-only/single-role examples are in the same file.
