# increment_build_number.py

# Import statements
import os
import platform
import re
import shlex
import tomlkit

from pathlib import Path
from typing import Dict, Optional, List 

from dotenv import load_dotenv

# Determine the path to the project's root directory
root = Path(Path(__file__).parents[3])
print(root)
load_dotenv(root / ".env")


# Globals
mobile_os_names: list[str] = ["iOS", "iPadOS", "Android"]
system: str = platform.system()
toml_fp: Path = root / "pyproject.toml"
is_mobile: bool = system in mobile_os_names 

if not is_mobile:
    import subprocess


# Environment variables
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")
PYPI_API_KEY = os.getenv("UV_PUBLISH_TOKEN")


# Helper functions
def get_root_dir() -> Path:
    """Computes the path to the current project's root directory.

    Returns:
        A `Path` object representing the absolute path to the
        current project's root directory.
    """
    return Path(__file__).parents[3]


def get_toml(fp: str | Path = get_root_dir() / "pyproject.toml") -> Dict:
    """Loads the `pyproject.toml` file into memory.

    Returns:
        A dictionary representation of the `pyproject.toml` file.
    """
    with open(fp, "r") as f:
        data = tomlkit.load(f)
    return data


def get_version_string() -> str:
    """Retrieves the version string from the `pyproject.toml` file.

    Returns:
        The current version string value.
    """
    data = get_toml()
    version_string = data["project"]["version"]

    return version_string


def compute_new_version_string() -> str:
    """Computes the project's incremented SemVer string.

    Returns:
        The literal value of the project's updated SemVer string.
    """
    current_version_string = get_version_string()
    normalized_version_string = (
        re.sub(r"[a-z]+", ".", current_version_string)
    )

    version_string_components = major, minor, patch, build = [
        int(i) for i in normalized_version_string.split(".")
    ]

    build += 1

    new_version_string = f"{major}.{minor}.{patch}dev{build}"

    return new_version_string


def bump_version_string(fp: str | Path = get_root_dir() / "pyproject.toml"):
    new_version_string = compute_new_version_string()

    with open(fp, "w") as f:
        data = {"project": {"version": new-version_string}}
        tomlkit.dump(data, f)


# Subprocesses
def git_commit(message: str):
    args = ["git", "commit", "-am", message]
    return subprocess.run(args)

def git_fetch():
    args = ["git", "fetch"]
    return subprocess.run(args)

def git_pull():
    args = ["git", "pull"]
    return subprocess.run(args)

def git_push(force: bool = False):
    args = ["git", "push"] if force is False else ["git", "push", "--force"]
    return subprocess.run(args)

def uv_build():
    """Builds the local package."""
    return subprocess.run(["uv", "build"])

def uv_publish():
    """Publishes the package's distribution files to PyPI."""
    return subprocess.run(["uv", "publish"])

def remove_build_artifacts():
    dist_dir = Path(root / "dist").resolve()
    args = ["rm", "-rf", dist_dir]

    return subprocess.run(args)


# Main process
def main():
    try:
        bump_version_string()
    except Exception as e:
        print(e)

    if not is_mobile:
        try:
            print("Running subprocesses...")
            try:
                dist_dir = Path(root, "dist").resolve()

                print(f"Removing build artifacts from {dist_dir}")
                remove_build_artifacts()
                print("Success.")
            except Exception as e:
                print(e)

            try:
                print("Building package...")
                uv_build()
                print("Success.")
            except Exception as e:
                print(e)

            try:
                print(f"Publishing to PyPI with API key: {PYPI_API_KEY}...")
                uv_publish()
                print("Done.")
            except Exception as e:
                print(e) 

            print("Subprocesses complete.")

        except Exception as e:
            print(e)

        if GITHUB_REPO_URL:
            try:
                print(f"Committing to remote repository at {GITHUB_REPO_URL}...")
                git_fetch()
                git_pull()
                git_commit(message=f"Automatic build: {get_version_string()}")
                git_push()
                print("Success.")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    print(
f"""
Project config file path:   {toml_fp}
System name:                {system}
API Key:                    {PYPI_API_KEY}
Mobile?                     {is_mobile}
"""
    )

    main()

