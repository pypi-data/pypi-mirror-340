# Copyright (C) 2025 Your Name <mohamadmorady412@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.

import subprocess
import sys
import importlib.util
import os
import argparse

DEV_REQUIREMENTS_FILE = "dev-requirements.txt"
REQUIRED_DEV_MODULES = ["requests", "pyyaml", "packaging"]

def is_module_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def install_and_track_modules(modules):
    with open(DEV_REQUIREMENTS_FILE, "w") as f:
        for module in modules:
            if not is_module_installed(module):
                print(f"📦 Installing {module} ...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            version = get_installed_version(module)
            if version:
                f.write(f"{module}=={version}\n")
                print(f"✅ Added to {DEV_REQUIREMENTS_FILE}: {module}=={version}")
            else:
                print(f"⚠️ Could not detect version for {module}")

def get_installed_version(module_name):
    try:
        import pkg_resources
        return pkg_resources.get_distribution(module_name).version
    except Exception:
        return None

def get_latest_stable_version(package_name):
    import requests
    from packaging.version import parse as parse_version

    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Couldn't fetch data for {package_name}")
        return None
    data = response.json()
    versions = list(data["releases"].keys())
    stable_versions = [v for v in versions if all(x not in v for x in ['a', 'b', 'rc', 'dev'])]
    stable_versions.sort(key=parse_version, reverse=True)
    return stable_versions[0] if stable_versions else None

def generate_requirements(yaml_path, output_path="requirements.txt"):
    import yaml

    with open(yaml_path, 'r') as f:
        packages = yaml.safe_load(f)['libraries']

    with open(output_path, 'w') as f:
        for package in packages:
            version = get_latest_stable_version(package)
            if version:
                f.write(f"{package}=={version}\n")
                print(f"✅ {package}=={version}")
            else:
                print(f"⚠️ Skipping {package}")

def main():
    install_and_track_modules(REQUIRED_DEV_MODULES)

    parser = argparse.ArgumentParser(description="📦 Generate requirements.txt with latest stable versions.")
    parser.add_argument("yaml_file", help="YAML file containing library names under 'libraries' key.")
    parser.add_argument("--output", "-o", default="requirements.txt", help="Output file name (default: requirements.txt)")
    args = parser.parse_args()

    if not os.path.exists(args.yaml_file):
        print(f"❌ File not found: {args.yaml_file}")
        sys.exit(1)

    generate_requirements(args.yaml_file, args.output)
