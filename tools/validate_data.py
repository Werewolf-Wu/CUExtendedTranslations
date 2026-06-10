"""Python script to validate the yaml files."""

import logging
import sys
from pathlib import Path

from rich.logging import RichHandler
from yaml import YAMLError, safe_load

# Schema version needs update if you make breaking changes to yamls.
EXPECTED_SCHEMA_VERSION = 19
DATA_DIR = Path("data")
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])
logger = logging.getLogger(__name__)


def validate_file(path: Path) -> bool:
    """Validate a yaml file."""
    try:
        with path.open() as f:
            data = safe_load(f)
        if "schema_version" not in data:
            logger.error("%s has no schema_version", path)
            return False
        if data["schema_version"] != EXPECTED_SCHEMA_VERSION:
            logger.error("%s has incorrect schema_version", path)
            return False
    except YAMLError:
        logger.error("%s is not a valid YAML file", path, exc_info=False)
        return False
    return True


def main() -> int:
    """Perform validation on yaml files."""
    failed_paths = [
        path for path in DATA_DIR.rglob("*.yaml") if not validate_file(path)
    ]

    if not failed_paths:
        logger.info("All YAML files are valid")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
