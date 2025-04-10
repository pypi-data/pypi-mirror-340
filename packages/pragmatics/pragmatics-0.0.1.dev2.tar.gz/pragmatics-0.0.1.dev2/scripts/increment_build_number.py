# increment_build_number.py
import os
import platform
import re
import tomlkit

from pathlib import Path
from dotenv import load_dotenv; load_dotenv()

# Environment
system = platform.system()
api_key = os.getenv("UV_PUBLISH_TOKEN")
mobile_systems = ["iOS", "iPadOS", "Android"]
is_mobile: bool = system in mobile_systems
if not is_mobile:
    import subprocess


def main():
    fp = Path(Path(__file__).parent.parent, "pyproject.toml").resolve()
    
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
            result = subprocess.run(
                ["uv", "publish", "--token", api_key],
                shell=True,
                capture_output=True
            )
        except Exception as e:
            print(e)

    print(
f"""
Successfully incremented from {old_version_string} to {new_version_string}.
"""
)


if __name__ == "__main__":
    main()

