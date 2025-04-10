# increment_build_number.py
import os
import platform
import re
import tomlkit

from pathlib import Path
from dotenv import load_dotenv

root = Path(Path(__file__).parent.parent)
print(root)
load_dotenv(root / ".env")

# Environment

fp = root / "pyproject.toml" 
system = platform.system()
api_key = os.getenv("UV_PUBLISH_TOKEN")
mobile_systems = ["iOS", "iPadOS", "Android"]
is_mobile: bool = system in mobile_systems
print(f"""
Project config file path:   {fp}
System name:                {system}
API Key:                    {api_key}
Mobile?                     {is_mobile}
""")
if not is_mobile:
    import subprocess


def main():    
    with open(fp, "r") as f:
        data = tomlkit.load(f)

    old_version_string = data["project"]["version"]
    sanitized_old_version_string = (
        re.sub(r"[a-z]+", ".", old_version_string)
    )

    major, minor, patch, build = [
        int(i) for i in sanitized_old_version_string.split(".")
    ]

    build += 1

    new_version_string = f"{major}.{minor}.{patch}dev{build}"

    data["project"]["version"] = new_version_string

    with open(fp, "w") as f:
        tomlkit.dump(data, f)

    if not is_mobile:
        try:
            print("Running subprocesses...")
            try:
                dist_dir = Path(root, "dist").resolve()

                print(f"Removing build artifacts from {dist_dir}")
                subprocess.run(["cd", ".."])
                subprocess.run(["rm", "-rf", "dist"])
                print("Success.")
            except Exception as e:
                print(e)
            try:
                print("Building package...")
                subprocess.run(["uv", "build"])
                print("Success.")
            except Exception as e:
                print(e)
            try:
                print(f"Publishing to PyPI with API key: {api_key}...")
                args = ["uv", "publish"]
                subprocess.run(args)
                print("Done.")
            except Exception as e:
                print(e)
            print("Subprocesses complete.")
        except Exception as e:
            print(e)

    print(
f"""
Successfully incremented from {old_version_string} to {new_version_string}.
"""
)


if __name__ == "__main__":
    main()

