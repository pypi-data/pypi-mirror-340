# config.py
import logging
import shutil
import subprocess
import sys
from importlib import resources
from importlib.metadata import version as poetry_version
from pathlib import Path

import requests
import typer
import yaml
from packaging import version

from stratio.config import Config


# Set up a logger for the CLI.
def get_logger() -> logging.Logger:
    """Set up a module–level logger."""
    _logger = logging.getLogger("Stratio")
    if not _logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(logging.WARN)

        # Set boto3 and botocore loggers to WARNING level
        logging.getLogger("boto3").setLevel(logging.WARNING)
        logging.getLogger("botocore").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
    return _logger


logger = get_logger()
logger.propagate = False

_config = None


def load_config(config_path: str) -> Config:
    """
    Load the configuration from the specified YAML file.
    """
    try:
        config = Config.load_from_file(config_path)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise typer.Exit(1) from e


# ─── VERSIONING AND UPDATE ────────────────────────────────────────────────────────────

__version__ = poetry_version("aws-marketplace-toolkit")


def check_and_update() -> bool:
    pypi_url = "https://pypi.org/pypi/aws-marketplace-toolkit/json"
    response = requests.get(pypi_url, timeout=10)
    response.raise_for_status()
    data = response.json()
    latest_version = data["info"]["version"]
    if version.parse(latest_version) > version.parse(__version__):
        print(f"\nA new version ({latest_version}) is available (you have {__version__}).")
        answer = input("Would you like to update now? [Y/n] ").strip().lower()
        if answer in ("", "y", "yes"):
            print("Updating aws-marketplace-toolkit (pip install --upgrade aws-marketplace-toolkit)...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "aws-marketplace-toolkit"])
            print("\nUpdate installed successfully. Please restart the CLI to use the updated version.")
            return True
        else:
            return False
    else:
        return False


def matches_manifest_version(current_version: str) -> bool:
    manifest_file = Path.home() / ".marketplace" / "MANIFEST"
    manifest_version = None

    if not manifest_file.exists():
        return False

    with open(manifest_file) as manifest:
        for line in manifest:
            if line.startswith("VERSION"):
                manifest_version = line.split("=")[1].strip()
                break

    if manifest_version is None:
        return False

    return version.parse(manifest_version) == version.parse(current_version)


def update_config_environments(current_version: str):
    config_dir = Path.home() / ".marketplace"

    # Load the default configuration template.
    with resources.open_binary("stratio.cli", "config_default.yaml") as src_file:
        default_config = yaml.safe_load(src_file)

    # Ensure the default config itself is updated with the current version.
    default_config["version"] = current_version

    config_dir_path = Path(config_dir)
    for config_file in config_dir_path.glob("*.yaml"):
        with open(config_file) as f:
            try:
                user_config = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Error parsing {config_file}: {e}")
                continue

        # Compare versions if present.
        user_version = user_config.get("version")
        if user_version is None or version.parse(user_version) < version.parse(current_version):
            # Backup the existing configuration.
            backup_file = config_file.with_suffix(config_file.suffix + ".backup")
            shutil.copy(config_file, backup_file)
            print(f"Backed up {config_file} to {backup_file}")

            updated_config = deep_merge_defaults(user_config, default_config)
            updated_config["version"] = current_version

            # Write back the updated configuration.
            with open(config_file, "w") as f:
                yaml.safe_dump(updated_config, f)
            print(f"Updated configuration file {config_file}")


def update_manifest_file(current_version: str):
    manifest_file = Path.home() / ".marketplace" / "MANIFEST"
    with open(manifest_file, "w") as manifest:
        manifest.write(f"VERSION={current_version}\n")


def deep_merge_defaults(user: dict, default: dict) -> dict:
    """
    Recursively merge the default configuration into the user configuration.
    Only keys missing in the user configuration are added.
    If a key exists in both and the values are dictionaries, merge them recursively.
    Otherwise, the user configuration takes precedence.
    """
    for key, default_value in default.items():
        if key not in user:
            user[key] = default_value
        elif isinstance(default_value, dict) and isinstance(user.get(key), dict):
            deep_merge_defaults(user[key], default_value)
    return user


def copy_default_config_if_missing():
    """
    Check if the default configuration file exists in ~/.marketplace.
    If not, copy the bundled config_default.yaml from the package resources.
    """
    dest_dir = Path.home() / ".marketplace"
    config_dest = dest_dir / "config_default.yaml"
    if not config_dest.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        try:
            # Access the config_default.yaml file within the stratio.cli package.
            # Ensure that your package’s structure includes the config_default.yaml file in the correct location.
            with resources.open_binary("stratio.cli", "config_default.yaml") as src_file, open(
                config_dest, "wb"
            ) as dst_file:
                shutil.copyfileobj(src_file, dst_file)
            print(f"Default configuration copied to {config_dest}")
        except Exception as e:
            raise RuntimeError(f"Could not copy default configuration: {e}") from e


def get_current_version():
    return __version__
