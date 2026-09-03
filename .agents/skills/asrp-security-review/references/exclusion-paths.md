# Non-Essential Path Exclusion (Single Source of Truth)

When profiling, rule resolution, or scanning, exclude paths that do not contain business source code.

## Mandatory excluded paths

Write these into:

- `components.yaml` → `components[].exclude_paths`
- `scope.yaml` → `scope.exclude`

### Dependencies and build artifacts

- `node_modules`
- `vendor`
- `dist`
- `build`
- `out`
- `coverage`
- `.pnpm-store`
- `yarn-error.log`

### Tooling and IDE configurations

- `.vscode`
- `.idea`
- `.devcontainer`
- `.husky`
- `.github`
- `.agents`

### Version control and temp

- `.git`
- `tmp`
- `temp`

## Application rules

1. Apply exclusions during Step 1 profiling — do not wait until scan.
2. Mirror component exclusions at project scope via `scope.exclude`.
3. Propagate the same list to scanner orchestrator scope.
4. Do not scan excluded paths even if findings might exist there (e.g. secrets in `node_modules` are out of scope for project audit).

## Priority source directories (always include)

When discovering code and deriving `scan_paths`, prioritize:

- `src/`, `apps/`, `libs/`, `packages/`, `services/`, `controllers/`
- `dockerfiles/`, `k8s/`, `helm/`
- Root config: `package.json`, `Dockerfile`, `docker-compose.yaml`, `pyproject.toml`

Do **not** use legacy field names `in_scope_paths` / `out_of_scope_paths` — use `scope.include` / `scope.exclude` per schema.
