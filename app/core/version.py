from __future__ import annotations

from importlib import metadata

PACKAGE_NAME = "pyserp-api"


def get_app_version(default: str = "unknown") -> str:
    try:
        return metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        return default
