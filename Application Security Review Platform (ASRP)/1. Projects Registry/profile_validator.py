"""
Layer 1 Profile Validator — schema, cross-file linkage, manifest hash, human gate.
Used by `asrp.py validate` (stages: profile | gate) and enforced before scan.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone

import yaml

PROFILE_FILES = [
    "project.yaml",
    "components.yaml",
    "technologies.yaml",
    "architecture.yaml",
    "scope.yaml",
    "context.yaml",
    "assessment.yaml",
]

SCHEMA_MAP = {
    "project.yaml": "project.schema.json",
    "components.yaml": "components.schema.json",
    "technologies.yaml": "technologies.schema.json",
    "architecture.yaml": "architecture.schema.json",
    "scope.yaml": "scope.schema.json",
    "context.yaml": "context.schema.json",
    "assessment.yaml": "assessment.schema.json",
    "registry.manifest.yaml": "registry-manifest.schema.json",
}

DEFAULT_SCHEMA_VERSIONS = {
    "project": "1.0",
    "components": "1.0",
    "technologies": "1.0",
    "architecture": "1.0",
    "scope": "1.0",
    "context": "1.0",
    "assessment": "1.0",
}


@dataclass
class ValidationResult:
    project_id: str
    stage: str = "gate"
    passed: bool = False
    schema_results: dict[str, bool] = field(default_factory=dict)
    schema_errors: dict[str, str] = field(default_factory=dict)
    cross_file_errors: list[str] = field(default_factory=list)
    lifecycle_errors: list[str] = field(default_factory=list)
    manifest_status: str | None = None
    project_lifecycle_status: str | None = None
    manifest_hash_expected: str | None = None
    manifest_hash_computed: str | None = None
    missing_files: list[str] = field(default_factory=list)

    @property
    def errors(self) -> list[str]:
        errs: list[str] = []
        errs.extend(f"Missing file: {f}" for f in self.missing_files)
        for fname, msg in self.schema_errors.items():
            if fname == "__tool__":
                errs.append(msg)
            else:
                errs.append(f"Schema fail ({fname}): {msg}")
        errs.extend(self.cross_file_errors)
        errs.extend(self.lifecycle_errors)
        if self.stage == "gate" and "registry.manifest.yaml" not in self.missing_files:
            if self.manifest_status != "validated":
                errs.append(
                    f"Human gate: registry.manifest.yaml lifecycle_status must be 'validated' "
                    f"(got '{self.manifest_status}')"
                )
            if (
                self.manifest_hash_expected
                and self.manifest_hash_computed
                and self.manifest_hash_expected != self.manifest_hash_computed
            ):
                errs.append(
                    "Profile hash mismatch: manifest profile_hash does not match current profile files"
                )
        return errs


class ProfileValidator:
    def __init__(self, asrp_dir: str, project_id: str, stage: str = "gate"):
        if stage not in ("profile", "gate"):
            raise ValueError(f"Invalid stage '{stage}'; use 'profile' or 'gate'")
        self.asrp_dir = asrp_dir
        self.project_id = project_id
        self.stage = stage
        self.project_dir = os.path.join(asrp_dir, "1. Projects Registry", project_id)
        self.schema_dir = os.path.join(asrp_dir, "1. Projects Registry", "schema")

    def run(self) -> ValidationResult:
        result = ValidationResult(project_id=self.project_id, stage=self.stage)

        for fname in PROFILE_FILES:
            if not os.path.exists(os.path.join(self.project_dir, fname)):
                result.missing_files.append(fname)

        manifest_path = os.path.join(self.project_dir, "registry.manifest.yaml")
        manifest_exists = os.path.exists(manifest_path)
        if self.stage == "gate" and not manifest_exists:
            result.missing_files.append("registry.manifest.yaml")

        schema_files = list(PROFILE_FILES)
        if self.stage == "gate" and manifest_exists:
            schema_files.append("registry.manifest.yaml")

        self._validate_schemas(result, schema_files)

        if result.missing_files:
            return result

        profiles = self._load_profiles(include_manifest=manifest_exists)
        self._validate_cross_file(profiles, result, manifest_exists)

        project = profiles["project.yaml"].get("project", {})
        result.project_lifecycle_status = project.get("lifecycle_status")

        if self.stage == "profile":
            if result.project_lifecycle_status != "profiled":
                result.lifecycle_errors.append(
                    f"Step 1: project.yaml lifecycle_status must be 'profiled' "
                    f"(got '{result.project_lifecycle_status}')"
                )
            result.passed = (
                not result.missing_files
                and all(result.schema_results.get(f, False) for f in PROFILE_FILES)
                and not result.cross_file_errors
                and not result.lifecycle_errors
                and "__tool__" not in result.schema_errors
            )
            return result

        manifest_data = profiles.get("registry.manifest.yaml", {}).get("registry_manifest", {})
        result.manifest_status = manifest_data.get("lifecycle_status")
        result.manifest_hash_expected = manifest_data.get("profile_hash")

        profile_file_order = manifest_data.get("profile_files") or PROFILE_FILES
        result.manifest_hash_computed = compute_profile_hash(self.project_dir, profile_file_order)

        if result.project_lifecycle_status != "validated":
            result.lifecycle_errors.append(
                f"Lifecycle sync: project.yaml lifecycle_status must be 'validated' "
                f"(got '{result.project_lifecycle_status}'); run sign-off to sync"
            )
        if result.manifest_status == "validated" and result.project_lifecycle_status == "profiled":
            result.lifecycle_errors.append(
                "Lifecycle sync: manifest is validated but project.yaml is still 'profiled'"
            )

        result.passed = (
            not result.missing_files
            and all(result.schema_results.values())
            and not result.cross_file_errors
            and not result.lifecycle_errors
            and result.manifest_status == "validated"
            and result.manifest_hash_expected == result.manifest_hash_computed
            and "__tool__" not in result.schema_errors
        )
        return result

    def _load_profiles(self, include_manifest: bool = True) -> dict[str, dict]:
        loaded: dict[str, dict] = {}
        files = list(PROFILE_FILES)
        if include_manifest:
            files.append("registry.manifest.yaml")
        for fname in files:
            path = os.path.join(self.project_dir, fname)
            with open(path, encoding="utf-8") as f:
                loaded[fname] = yaml.safe_load(f) or {}
        return loaded

    def _validate_schemas(self, result: ValidationResult, schema_files: list[str]) -> None:
        if not self._check_jsonschema_available():
            result.schema_errors["__tool__"] = (
                "check-jsonschema not installed. Run: pip install check-jsonschema pyyaml"
            )
            result.schema_results["__tool__"] = False
            return

        for fname in schema_files:
            schema_file = SCHEMA_MAP[fname]
            yaml_rel = os.path.join("..", self.project_id, fname).replace("\\", "/")
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "check_jsonschema",
                    "--schemafile",
                    schema_file,
                    yaml_rel,
                ],
                cwd=self.schema_dir,
                capture_output=True,
                text=True,
            )
            if proc.returncode == 0:
                result.schema_results[fname] = True
            else:
                result.schema_results[fname] = False
                detail = (proc.stdout + proc.stderr).strip()
                result.schema_errors[fname] = detail.splitlines()[-1] if detail else "validation failed"

    def _validate_cross_file(
        self,
        profiles: dict[str, dict],
        result: ValidationResult,
        manifest_exists: bool,
    ) -> None:
        project = profiles["project.yaml"].get("project", {})
        project_id = project.get("id")
        components = profiles["components.yaml"].get("components", [])
        technologies = profiles["technologies.yaml"].get("technologies", [])
        scope = profiles["scope.yaml"].get("scope", {})
        assessment = profiles["assessment.yaml"].get("assessment", {})

        component_ids = {c.get("id") for c in components if c.get("id")}

        if manifest_exists:
            manifest = profiles["registry.manifest.yaml"].get("registry_manifest", {})
            if manifest.get("project_id") and manifest.get("project_id") != project_id:
                result.cross_file_errors.append(
                    f"manifest project_id '{manifest.get('project_id')}' != project.id '{project_id}'"
                )

        for comp in components:
            cid = comp.get("project_id")
            if cid and cid != project_id:
                result.cross_file_errors.append(
                    f"components[{comp.get('id')}].project_id '{cid}' != project.id '{project_id}'"
                )

        for key, fname in [
            (scope.get("project_id"), "scope.yaml"),
            (profiles["context.yaml"].get("context", {}).get("project_id"), "context.yaml"),
            (profiles["architecture.yaml"].get("architecture", {}).get("project_id"), "architecture.yaml"),
            (assessment.get("project_id"), "assessment.yaml"),
        ]:
            if key and key != project_id:
                result.cross_file_errors.append(f"{fname} project_id '{key}' != project.id '{project_id}'")

        for tech in technologies:
            cid = tech.get("component_id")
            if cid and cid not in component_ids:
                result.cross_file_errors.append(
                    f"technologies component_id '{cid}' not found in components"
                )

        for cid in scope.get("component_ids") or []:
            if cid not in component_ids:
                result.cross_file_errors.append(
                    f"scope.component_ids '{cid}' not found in components"
                )

        scope_exclude = set(scope.get("exclude") or [])
        for comp in components:
            for path in comp.get("exclude_paths") or []:
                if path not in scope_exclude:
                    result.cross_file_errors.append(
                        f"components[{comp.get('id')}].exclude_paths '{path}' not in scope.exclude"
                    )

        rule_set_ids = assessment.get("rule_set_ids") or []
        if not rule_set_ids:
            result.cross_file_errors.append("assessment.rule_set_ids must be non-empty")

        review_level = scope.get("review_level")
        if not review_level:
            result.cross_file_errors.append("scope.review_level must be set")

        if not components:
            result.cross_file_errors.append("components must contain at least one entry")

        if len(technologies) != len(components):
            result.cross_file_errors.append(
                f"technologies entries ({len(technologies)}) must match components count ({len(components)})"
            )

    @staticmethod
    def _check_jsonschema_available() -> bool:
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "check_jsonschema", "--version"],
                capture_output=True,
                text=True,
            )
            return proc.returncode == 0
        except Exception:
            return False


def compute_profile_hash(project_dir: str, profile_files: list[str] | None = None) -> str:
    """SHA-256 of concatenated profile file contents in manifest order."""
    order = profile_files or PROFILE_FILES
    digest = hashlib.sha256()
    for fname in order:
        path = os.path.join(project_dir, fname)
        with open(path, "rb") as f:
            digest.update(f.read())
    return f"sha256:{digest.hexdigest()}"


def _save_yaml(data: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def sign_off_project(
    asrp_dir: str,
    project_id: str,
    validated_by: str,
    exit_on_fail: bool = False,
) -> ValidationResult:
    """Human gate sign-off: profile checks → write manifest → sync lifecycle → gate checks."""
    project_dir = os.path.join(asrp_dir, "1. Projects Registry", project_id)
    project_path = os.path.join(project_dir, "project.yaml")

    print(f"\n=======================================================")
    print(f"✍️  VALIDATE GATE SIGN-OFF: {project_id}")
    print(f"=======================================================\n")

    profile_result = ProfileValidator(asrp_dir, project_id, stage="profile").run()
    print_validation_report(profile_result)
    if not profile_result.passed:
        if exit_on_fail:
            sys.exit(1)
        return profile_result

    validated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    project_data = yaml.safe_load(open(project_path, encoding="utf-8")) or {}
    project = project_data.setdefault("project", {})
    project["lifecycle_status"] = "validated"
    project["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    _save_yaml(project_data, project_path)
    print(f"  [✓] Synced project.yaml → lifecycle_status: validated")

    profile_hash = compute_profile_hash(project_dir, PROFILE_FILES)

    manifest_data = {
        "registry_manifest": {
            "project_id": project_id,
            "registry_version": "1.0",
            "lifecycle_status": "validated",
            "validated_at": validated_at,
            "validated_by": validated_by,
            "profile_files": list(PROFILE_FILES),
            "profile_hash": profile_hash,
            "schema_versions": dict(DEFAULT_SCHEMA_VERSIONS),
        }
    }
    manifest_path = os.path.join(project_dir, "registry.manifest.yaml")
    _save_yaml(manifest_data, manifest_path)
    print(f"  [✓] Wrote registry.manifest.yaml (profile_hash: {profile_hash})\n")

    gate_result = ProfileValidator(asrp_dir, project_id, stage="gate").run()
    print_validation_report(gate_result)
    if exit_on_fail and not gate_result.passed:
        sys.exit(1)
    return gate_result


def print_validation_report(result: ValidationResult) -> None:
    stage_label = "Step 1 Profile" if result.stage == "profile" else "Validate Gate"
    print(f"\n=======================================================")
    print(f"🔎 {stage_label}: {result.project_id}")
    print(f"=======================================================\n")

    print("── Profile Files ──")
    for fname in PROFILE_FILES:
        if fname in result.missing_files:
            print(f"  [X] Missing: {fname}")
        elif result.schema_results.get(fname):
            print(f"  [✓] {fname} — schema pass")
        elif fname in result.schema_errors:
            print(f"  [X] {fname} — schema fail")
        else:
            print(f"  [✓] {fname} — found")

    if result.stage == "gate":
        print("\n── Manifest ──")
        if "registry.manifest.yaml" in result.missing_files:
            print("  [X] Missing: registry.manifest.yaml")
        elif result.schema_results.get("registry.manifest.yaml"):
            print("  [✓] registry.manifest.yaml — schema pass")
        elif "registry.manifest.yaml" in result.schema_errors:
            print("  [X] registry.manifest.yaml — schema fail")

    if result.schema_errors.get("__tool__"):
        print(f"\n  [!] {result.schema_errors['__tool__']}")

    print("\n── Cross-file Checks ──")
    if result.cross_file_errors:
        for err in result.cross_file_errors:
            print(f"  [X] {err}")
    else:
        print("  [✓] All linkage checks pass")

    print("\n── Lifecycle ──")
    print(f"  • project.yaml     : {result.project_lifecycle_status or 'N/A'}")
    if result.stage == "profile":
        expected = "profiled"
        ok = result.project_lifecycle_status == expected
        print(f"  • expected (Step 1): {expected} {'[✓]' if ok else '[X]'}")
    else:
        print(f"  • manifest status  : {result.manifest_status or 'N/A'}")
        print(f"  • manifest hash    : {result.manifest_hash_expected or 'N/A'}")
        print(f"  • computed hash    : {result.manifest_hash_computed or 'N/A'}")
        if (
            result.manifest_hash_expected
            and result.manifest_hash_computed
            and result.manifest_hash_expected == result.manifest_hash_computed
        ):
            print("  [✓] Profile hash matches")
        elif result.manifest_hash_computed:
            print("  [X] Profile hash mismatch — re-run sign-off")

    if result.lifecycle_errors:
        print("\n── Lifecycle Errors ──")
        for err in result.lifecycle_errors:
            print(f"  [X] {err}")

    print("\n-------------------------------------------------------")
    if result.passed:
        if result.stage == "profile":
            print("🎉 STEP 1 PROFILE CHECK PASSED — ready for Validate Gate sign-off.\n")
        else:
            print("🎉 PROJECT PROFILE IS VALIDATED AND READY TO SCAN!\n")
    else:
        if result.stage == "profile":
            print("[X] STEP 1 PROFILE CHECK FAILED.\n")
        else:
            print("[X] VALIDATION FAILED — project is NOT ready to scan.\n")
        for err in result.errors:
            print(f"    • {err}")
        print()


def validate_project(
    asrp_dir: str,
    project_id: str,
    stage: str = "gate",
    exit_on_fail: bool = False,
) -> ValidationResult:
    validator = ProfileValidator(asrp_dir, project_id, stage=stage)
    result = validator.run()
    print_validation_report(result)
    if exit_on_fail and not result.passed:
        sys.exit(1)
    return result
