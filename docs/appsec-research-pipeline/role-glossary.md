# Role Glossary (SSoT)

Single source of truth for AppSec research pipeline persona names. All other docs link here; do not duplicate the full table elsewhere.

**Naming format**: `Mr [Letter] ([Mnemonic])` — letter is stable; mnemonic describes the role.

**Mnemonic chain** (pipeline roles P→W):

```text
Professional → Analyst → Strategist → Hazard → Realist → Builder → Qualifier → Writer
     P              A           S          H         R          B          Q         W
```

## Canonical roles

| Letter | Display name | Formerly | Primary responsibility | KB sections |
|--------|--------------|----------|------------------------|-------------|
| **P** | **Mr P (Professional)** | Professor P | Orchestrator: pre-flight, job plan, coordinate team | — |
| **A** | **Mr A (Analyst)** | Security Researcher | Theory, mechanism, terminology | `#3`, `#4`, minimal `#1–#2` |
| **S** | **Mr S (Strategist)** | Security Architect | Threat model, trust boundaries, scope | `#7`, `#1` |
| **H** | **Mr H (Hazard)** | Adversarial Security Engineer | Failure modes, common mistakes (defensive framing) | `#8` |
| **R** | **Mr R (Realist)** | Devil's Advocate | Assumptions, edge cases, where defenses fail | `#7`, `#8` |
| **B** | **Mr B (Builder)** | Defensive Security Engineer | Mitigations, verification signals, best practices | `#7`, `#9`, `#10` |
| **Q** | **Mr Q (Qualifier)** | Knowledge Librarian | Evidence pack, related links, claim qualification | `#11`, `#12` |
| **W** | **Mr W (Writer)** | Technical Writer | Merge stubs → KB final, reconciliation, quality gates | `#1–#12` |

## Interactive-only personas

| Letter | Display name | Primary responsibility | In execution order? |
|--------|--------------|------------------------|---------------------|
| **QA** | **Mr QA (Query Assistant)** | Q&A, clarify stubs, suggest Proceed/Amend | **No** — on-demand at checkpoints or `qa-only` mode |

See [`interactive-mode.md`](interactive-mode.md) for checkpoint and standalone protocols.

## Execution order (normative)

Mr P orchestrates; research roles execute **sequentially**:

```text
Mr A (Analyst) → Mr S (Strategist) → Mr H (Hazard) → Mr R (Realist) → Mr B (Builder) → Mr Q (Qualifier) → Mr W (Writer)
```

Do not batch roles (e.g. "Mr A + Mr S" in one pass). In `interactive` mode, one role per turn — see [`interactive-mode.md`](interactive-mode.md).

## Output heading format

In `## Role outputs (internal)`, use **full form** for each role heading:

```markdown
### Mr A (Analyst)
### Mr S (Strategist)
### Mr H (Hazard)
### Mr R (Realist)
### Mr B (Builder)
### Mr Q (Qualifier)
### Mr W (Writer)
```

Mr QA uses `## Mr QA (Query Assistant)` (top-level, not under role outputs).

Do not use former names (e.g. "Security Researcher") in output headings.

## Naming rules

1. **First mention** in a section: full form `Mr B (Builder)`.
2. **Same section**: may shorten to `Mr B` after first mention.
3. **Do not use** `Professor P` after migration (except in the "Formerly" column above).
4. Skill id remains `appsec-research-orchestrator`; only display names change.
