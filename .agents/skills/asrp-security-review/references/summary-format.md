# Summary Output Formats

Emit the appropriate summary table at the end of each step.

## Step 0 — Acquire

```markdown
## Summary — Source Acquisition

| Component | Source | Clone Path | Status |
|-----------|--------|------------|--------|
| {component_id} | {git_url or local} | clones/{project_id}/{component_id}/ | OK / FAIL |

**Run ID:** {run_id}
**Acquisition metadata:** runs/{run_id}/acquisition.json
```

## Step 1 — Profile

```markdown
## Summary — AI Auto-Profiling

| File | Schema | Status | Notes |
|------|--------|--------|-------|
| project.yaml | pass | OK | lifecycle_status: profiled |
| components.yaml | pass | OK | {n} components, scan_paths + exclude_paths |
| technologies.yaml | pass | OK | rule_set_ids per component |
| architecture.yaml | pass | OK | — |
| scope.yaml | pass | OK | review_level: {level}, exclude set |
| context.yaml | pass | OK | risk_tier: {tier} |
| assessment.yaml | pass | OK | {n} rule_set_ids, tools_enabled set |

**Components:** {n} discovered · **Rule sets:** {n} mapped
**Cross-file checks:** pass / FAIL ({details})
**Lifecycle:** profiled (manifest not updated — run Validate Gate)
**Schemas:** `asrp.py validate --stage profile` pass on 7 files
```

## Validate Gate

```markdown
## Summary — Validate Gate

| Check | Status |
|-------|--------|
| Profile stage | pass / FAIL |
| Sign-off by | {name} |
| Manifest hash | {sha256:...} |
| Gate stage | pass / FAIL |

**Lifecycle:** validated (project.yaml + manifest synced)
**Ready to scan:** yes / no
```

## Step 2 — Scan

```markdown
## Summary — Security Scan

| Severity | Count |
|----------|-------|
| CRITICAL | {n} |
| HIGH | {n} |
| MEDIUM | {n} |
| LOW | {n} |

| Component | Findings | Stage files |
|-----------|----------|-------------|
| {component_id} | {n} | 12/12 |

**Findings:** runs/{run_id}/findings.json
**Stage coverage:** {non_pass_mapped}/{non_pass_total} non-PASS items consolidated
**Scan validation:** pass / FAIL (`asrp.py validate --stage scan --run-id {run_id}`)
**Profile freshness:** pass / stale (manifest_hash match)
**Raw scan evidence:** native / emulated / empty
**Unique findings:** {n}
**Copy-paste check:** pass / FAIL
**Cross-stage mappings:** {n} findings mapped across multiple stages
```

## Step 3 — Report

```markdown
## Summary — Executive Report

| Metric | Value |
|--------|-------|
| Health Score | {score}/100 |
| Grade | {A-F} |
| Gate Status | PASSED / ACTION REQUIRED |

| Component | Score | Grade | Findings |
|-----------|-------|-------|----------|
| {component_id} | {score}/100 | {grade} | {n} |

| Report | Path |
|--------|------|
| Executive Dashboard | runs/{run_id}/security_review_report.html |
| Component ({id}) | runs/{run_id}/security_review_report_{id}.html |

**Report validation:** pass / FAIL (`asrp.py validate --stage report --run-id {run_id}`)
**SLA Roadmap:** Phase 1 ({n}) · Phase 2 ({n}) · Phase 3 ({n})
```

## Interactive checkpoint

After each phase in interactive mode:

```markdown
## Checkpoint — Phase {id}
- [x] {completed item}
- [ ] {pending item}

Proceed? (yes / amend / abort)
```
