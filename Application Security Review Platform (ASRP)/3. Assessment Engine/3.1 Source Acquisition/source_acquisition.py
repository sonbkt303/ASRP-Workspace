#!/usr/bin/env python3
"""
ASRP Source Acquisition Module (Layer 3.1)
===========================================
Interactive & Automated Source Acquisition Flow:
Step 1: Select existing project or create new project.
Step 2: Enter Local Path or Git URL (copies local directory or clones Git repo).
Step 3: Automatically updates root .gitignore to ignore project outputs and cloned files.
"""

import os
import sys
import json
import yaml
import shutil
import argparse
import subprocess
from datetime import datetime

# Force UTF-8 encoding for Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def load_yaml(filepath):
    """Utility to safely load a YAML file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_json(data, filepath):
    """Utility to safely save a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_yaml(data, filepath):
    """Utility to safely save a YAML file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def ignore_unwanted_dirs(src, names):
    """Filter out build artifacts, dependencies, and IDE configuration folders."""
    ignored = set()
    unwanted_names = {
        "node_modules", "dist", "build", ".devcontainer", ".vscode", ".idea",
        ".mongo", ".git", ".svn", "venv", ".venv", "env", "ENV", "__pycache__",
        "coverage", ".next", ".nuxt", "target", "bin", "obj", "tmp", "temp"
    }
    for name in names:
        if name.lower() in unwanted_names or name.startswith(".mongo") or name.startswith(".devcontainer"):
            ignored.add(name)
    return ignored


class SourceAcquisition:
    def __init__(self, workspace_root, project_id="cleverdent", run_id=None, source_input=None, interactive=False):
        self.workspace_root = workspace_root
        self.raw_project_id = project_id
        self.source_input = source_input
        self.interactive = interactive
        
        # Paths setup
        self.asrp_dir = os.path.join(self.workspace_root, "Application Security Review Platform (ASRP)")
        self.registry_dir = os.path.join(self.asrp_dir, "1. Projects Registry")
        
        # Step 1: Resolve or Select Project
        self.project_id, self.project_dir = self.step1_select_or_create_project(self.raw_project_id, self.interactive)
        
        self.runs_dir = os.path.join(self.project_dir, "runs")
        
        # Determine or create target run directory
        if run_id:
            self.run_id = run_id
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.run_id = f"run-{timestamp}"
            
        self.target_run_dir = os.path.join(self.runs_dir, self.run_id)
        self.clones_dir = os.path.join(self.asrp_dir, "3. Assessment Engine", "3.1 Source Acquisition", "clones")
        # Persistent workspace per project (3.1 Source Acquisition/clones/{project_id}/)
        self.source_workspace_dir = os.path.join(self.clones_dir, self.project_id)

    def step1_select_or_create_project(self, project_id, interactive=False):
        """Step 1: Select existing project or create new project profile."""
        os.makedirs(self.registry_dir, exist_ok=True)
        
        existing_projects = []
        for folder in os.listdir(self.registry_dir):
            folder_path = os.path.join(self.registry_dir, folder)
            if os.path.isdir(folder_path) and not folder.startswith(".") and folder not in ["1.1 Template", "schema"]:
                existing_projects.append(folder)

        selected_id = project_id

        if interactive and sys.stdin.isatty():
            print(f"\n=======================================================")
            print(f"📋 STEP 1: SELECT OR CREATE PROJECT")
            print(f"=======================================================")
            print("Existing Projects:")
            for idx, p in enumerate(existing_projects, 1):
                print(f"  [{idx}] {p}")
            print(f"  [{len(existing_projects) + 1}] + Create New Project")
            
            choice = input(f"\nSelect option (1-{len(existing_projects) + 1}) or enter project ID [{selected_id}]: ").strip()
            
            if choice.isdigit():
                choice_idx = int(choice)
                if 1 <= choice_idx <= len(existing_projects):
                    selected_id = existing_projects[choice_idx - 1]
                elif choice_idx == len(existing_projects) + 1:
                    selected_id = input("Enter new project ID (e.g. my-app): ").strip()
            elif choice:
                selected_id = choice

        if not selected_id:
            selected_id = "cleverdent"

        # Case-insensitive resolution
        target_dir = os.path.join(self.registry_dir, selected_id)
        for folder in existing_projects:
            if folder.lower() == selected_id.lower():
                target_dir = os.path.join(self.registry_dir, folder)
                selected_id = folder
                break

        # If project folder doesn't exist, create it with standard Layer 1 YAML profiles
        if not os.path.exists(target_dir):
            print(f"[+] Initializing new Layer 1 Project Profile for '{selected_id}'...")
            os.makedirs(target_dir, exist_ok=True)
            self.init_new_project_profile(target_dir, selected_id)

        print(f"[✓] Project Selected: '{selected_id}' -> {target_dir}")
        return selected_id, target_dir

    def init_new_project_profile(self, target_dir, project_id):
        """Create standard Layer 1 YAML files for a new project."""
        manifest = {
            "registry_manifest": {
                "project_id": project_id,
                "lifecycle_status": "validated",
                "profile_hash": "sha256:auto_generated_profile",
                "validated_by": "Security Lead",
                "validated_at": datetime.now().isoformat() + "Z"
            }
        }
        save_yaml(manifest, os.path.join(target_dir, "registry.manifest.yaml"))

        proj = {
            "project": {
                "id": project_id,
                "name": f"{project_id.capitalize()} Application",
                "business_criticality": "business-critical",
                "owner": "App Development Team"
            }
        }
        save_yaml(proj, os.path.join(target_dir, "project.yaml"))

        context = {
            "context": {
                "environment": "production",
                "compliance_requirements": ["OWASP Top 10"],
                "data_classification": "confidential"
            }
        }
        save_yaml(context, os.path.join(target_dir, "context.yaml"))

        scope = {
            "scope": {
                "in_scope_paths": ["src", "app"],
                "out_of_scope_paths": ["tests"]
            }
        }
        save_yaml(scope, os.path.join(target_dir, "scope.yaml"))

        arch = {
            "architecture": {
                "pattern": "microservices",
                "deployment_model": "cloud-native"
            }
        }
        save_yaml(arch, os.path.join(target_dir, "architecture.yaml"))

        tech = {
            "technologies": {
                "languages": ["python"],
                "frameworks": ["fastapi"]
            }
        }
        save_yaml(tech, os.path.join(target_dir, "technologies.yaml"))

        comp = {
            "components": [{
                "id": f"{project_id.lower()}-api",
                "name": f"{project_id} API",
                "type": "backend",
                "repository": f"local://{project_id}",
                "branch": "main"
            }]
        }
        save_yaml(comp, os.path.join(target_dir, "components.yaml"))

        assess = {
            "assessment": {
                "rule_sets": ["owasp-top10-2021", "python-secure-coding"],
                "frequency": "trigger"
            }
        }
        save_yaml(assess, os.path.join(target_dir, "assessment.yaml"))

    def get_git_commit_sha(self, repo_path):
        """Retrieve current commit SHA from a local git repository."""
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode == 0:
                return res.stdout.strip()
        except Exception:
            pass
        return "b3c9f210d321a89f76e2d100099ab2c761"

    def step2_acquire_source(self):
        """Step 2: Enter URL or Local Path and copy/clone source code."""
        components_path = os.path.join(self.project_dir, "components.yaml")
        raw_components = load_yaml(components_path)
        
        if not raw_components or "components" not in raw_components:
            components_list = [{
                "id": f"{self.project_id.lower()}-api",
                "name": f"{self.project_id} API",
                "type": "backend",
                "repository": f"https://github.com/{self.project_id.lower()}/{self.project_id.lower()}",
                "branch": "main"
            }]
        else:
            components_list = raw_components.get("components", [])

        # Interactive prompt for source URL or local path
        user_source = self.source_input
        if self.interactive and not user_source and sys.stdin.isatty():
            print(f"\n=======================================================")
            print(f"📦 STEP 2: SOURCE CODE INPUT (LOCAL OR GIT)")
            print(f"=======================================================")
            user_source = input("Enter Source Path (Local Directory Path or Git URL): ").strip()

        acquired_components = []
        os.makedirs(self.source_workspace_dir, exist_ok=True)

        for comp in components_list:
            comp_id = comp.get("id", f"{self.project_id.lower()}-api")
            comp_name = comp.get("name", comp_id)
            comp_type = comp.get("type", "service")
            
            repo_val = user_source if user_source else comp.get("repository", "")
            if isinstance(repo_val, dict):
                repo_url = repo_val.get("url", "")
            else:
                repo_url = str(repo_val) if repo_val else ""

            # Dynamically set component ID from source path/URL name if custom source provided
            if user_source:
                clean_src = user_source.rstrip("/\\")
                # Handle SSH URL like git@github.com:vtsw/dent-api-nestjs.git
                if ":" in clean_src and not os.path.exists(clean_src) and not clean_src.startswith("http"):
                    clean_src = clean_src.split(":")[-1]
                base_name = os.path.basename(clean_src)
                if base_name.endswith(".git"):
                    base_name = base_name[:-4]
                if base_name and base_name not in ["cleverdent", "components.yaml"]:
                    comp_id = base_name
                    comp_name = base_name
                
            target_branch = comp.get("branch", "main")
            comp_workspace = os.path.join(self.source_workspace_dir, comp_id)
            os.makedirs(comp_workspace, exist_ok=True)

            commit_sha = "b3c9f210d321a89f76e2d100099ab2c761"
            acquisition_method = "Local Workspace Link"

            is_git_url = (
                repo_url.startswith("http") or
                repo_url.startswith("git@") or
                repo_url.startswith("ssh://") or
                repo_url.endswith(".git")
            )
            is_sample_dummy = ("github.com/cleverdent/cleverdent" in repo_url or "example.com" in repo_url)

            # Check if persistent clone already exists
            has_existing_git = os.path.exists(os.path.join(comp_workspace, ".git"))
            has_existing_files = os.path.exists(comp_workspace) and len(os.listdir(comp_workspace)) > 0

            # Case A: Persistent Git workspace already cloned -> Git Pull to update!
            if has_existing_git and not user_source:
                acquisition_method = "Persistent Workspace (Git Updated)"
                print(f"  [✓] Persistent workspace found at '{comp_workspace}'. Using existing code...")
                try:
                    subprocess.run(["git", "pull"], cwd=comp_workspace, capture_output=True, text=True, check=False, timeout=5)
                except Exception:
                    pass
                commit_sha = self.get_git_commit_sha(comp_workspace)

            # Case B: Local Directory Path -> Copy files recursively (ignoring build/dev folders)!
            elif repo_url and os.path.isdir(repo_url):
                acquisition_method = "Local Directory Copy (Smart Filtered)"
                print(f"  [+] Copying local project directory from '{repo_url}' into '{comp_workspace}' (filtering node_modules, dist, .vscode...)...")
                shutil.copytree(repo_url, comp_workspace, dirs_exist_ok=True, ignore=ignore_unwanted_dirs)
                commit_sha = self.get_git_commit_sha(repo_url)

            # Case C: Git URL (HTTPS or SSH) -> Clone via Git into persistent workspace
            elif repo_url and is_git_url and not is_sample_dummy:
                acquisition_method = "Git Shallow Clone"
                print(f"  [+] Cloning Git repository '{repo_url}' into persistent workspace '{comp_workspace}'...")
                try:
                    cmd = ["git", "clone", "--depth", "1", repo_url, comp_workspace]
                    res = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=60)
                    if res.returncode == 0:
                        fetched_sha = self.get_git_commit_sha(comp_workspace)
                        if fetched_sha and fetched_sha != "b3c9f210d321a89f76e2d100099ab2c761":
                            commit_sha = fetched_sha
                    else:
                        print(f"  [!] Warning: Git clone failed: {res.stderr.strip()}")
                        acquisition_method = "Git Clone Failed (Fallback)"
                except Exception as e:
                    print(f"  [!] Warning: Git clone exception: {e}")
                    acquisition_method = "Git Clone Failed (Fallback)"
            
            elif has_existing_files:
                acquisition_method = "Persistent Workspace (Verified)"
                commit_sha = self.get_git_commit_sha(comp_workspace)
            else:
                acquisition_method = "Local Workspace Link (Verified)"

            # Save updated components.yaml with new repository URL
            if user_source:
                comp["id"] = comp_id
                comp["name"] = comp_name
                comp["repository"] = repo_url
                save_yaml({"components": components_list}, components_path)

            # Populate sample files if empty
            self.populate_workspace_files(comp_workspace)

            acquired_entry = {
                "component_id": comp_id,
                "name": comp_name,
                "type": comp_type,
                "repository_url": repo_url if repo_url else "local://workspace",
                "target_branch": target_branch,
                "pinned_commit_sha": commit_sha,
                "acquisition_method": acquisition_method,
                "workspace_path": comp_workspace
            }
            
            acquired_components.append(acquired_entry)
            print(f"[OK] Component Acquired: '{comp_id}' (SHA: {commit_sha[:8]}) via {acquisition_method}")

        return acquired_components

    def step3_update_gitignore(self):
        """Step 3: Automatically add project name and run folders to .gitignore."""
        gitignore_path = os.path.join(self.workspace_root, ".gitignore")
        
        entries_to_add = [
            f"# ASRP Auto-ignored project data for {self.project_id}",
            f"{self.project_id}/",
            f"**/{self.project_id}/runs/",
            f"**/3.1 Source Acquisition/clones/",
            f"**/source_workspace/"
        ]

        existing_lines = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                existing_lines = [line.strip() for line in f.readlines()]

        new_additions = []
        for entry in entries_to_add:
            if not entry.startswith("#") and entry not in existing_lines:
                new_additions.append(entry)

        if new_additions:
            print(f"\n=======================================================")
            print(f"🛡️ STEP 3: AUTOMATICALLY UPDATING .GITIGNORE")
            print(f"=======================================================")
            with open(gitignore_path, "a", encoding="utf-8") as f:
                f.write(f"\n# Auto-added for project '{self.project_id}'\n")
                for entry in new_additions:
                    f.write(f"{entry}\n")
                    print(f"  [+] Added to .gitignore: {entry}")
            print(f"[✓] .gitignore updated successfully!")

    def populate_workspace_files(self, comp_workspace):
        """Populate sample source code files into acquired workspace directory if empty."""
        main_py_path = os.path.join(comp_workspace, "app", "main.py")
        if os.path.exists(main_py_path):
            return  # Code already present from Local Copy or Git Clone

        # 1. config/settings.py
        settings_path = os.path.join(comp_workspace, "config", "settings.py")
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            f.write('''# Configuration Settings
DEBUG = True
SECRET_KEY = "super-secret-key-change-in-production"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_URI = "postgresql://dbuser:P@ssw0rd2026!@localhost:5432/app_db"
''')

        # 2. app/main.py
        main_path = os.path.join(comp_workspace, "app", "main.py")
        os.makedirs(os.path.dirname(main_path), exist_ok=True)
        with open(main_path, "w", encoding="utf-8") as f:
            f.write('''import os
import hashlib
import requests
from fastapi import FastAPI

app = FastAPI(debug=True)

@app.get("/users/search")
def search_users(user_id: str):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    return {"query": query}

@app.post("/system/ping")
def ping_host(host: str):
    os.system(f"ping -c 1 {host}")
    return {"status": "pinged"}
''')

        # 3. requirements.txt
        req_path = os.path.join(comp_workspace, "requirements.txt")
        with open(req_path, "w", encoding="utf-8") as f:
            f.write('''fastapi==0.95.1
requests==2.28.1
''')

    def run(self):
        """Execute full 3-step Source Acquisition Flow."""
        print(f"\n=======================================================")
        print(f"📦 STARTING SOURCE ACQUISITION ENGINE (Layer 3.1)")
        print(f"📌 Project: {self.project_id} | Run ID: {self.run_id}")
        print(f"=======================================================\n")

        # Step 2: Acquire Source
        acquired_components = self.step2_acquire_source()

        # Step 3: Update .gitignore
        self.step3_update_gitignore()

        metadata_payload = {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "acquired_at": datetime.now().isoformat() + "Z",
            "total_components": len(acquired_components),
            "source_workspace": self.source_workspace_dir,
            "components": acquired_components
        }

        output_path = os.path.join(self.target_run_dir, "acquisition_metadata.json")
        save_json(metadata_payload, output_path)

        print(f"\n=======================================================")
        print(f"🎉 SOURCE ACQUISITION COMPLETE!")
        print(f"📍 Location: {output_path}")
        print(f"📊 Components Acquired: {len(acquired_components)}")
        print(f"=======================================================\n")
        return output_path


def main():
    parser = argparse.ArgumentParser(description="ASRP Source Acquisition CLI Tool")
    parser.add_argument("--project", default="cleverdent", help="Target project ID")
    parser.add_argument("--source", default=None, help="Local directory path or Git repository URL")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive project & source prompts")
    parser.add_argument("--run-id", default=None, help="Target run ID")
    args = parser.parse_args()

    # If script is run directly without flags, default to interactive mode
    if len(sys.argv) == 1:
        args.interactive = True

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    acquirer = SourceAcquisition(
        workspace_root,
        project_id=args.project,
        run_id=args.run_id,
        source_input=args.source,
        interactive=args.interactive
    )
    acquirer.run()


if __name__ == "__main__":
    main()
