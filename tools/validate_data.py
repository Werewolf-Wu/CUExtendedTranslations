"""Python script to validate the yaml files."""

import logging
import sys
from pathlib import Path

from rich.logging import RichHandler
from yaml import YAMLError, safe_load

# Schema version needs update if you make breaking changes to yamls.
EXPECTED_SCHEMA_VERSION = 19
DATA_DIR = Path("data")
logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
flag: bool = False

for path in DATA_DIR.rglob("*.yaml"):
    try:
        with path.open() as f:
            data = safe_load(f)
        if data["schema_version"] != EXPECTED_SCHEMA_VERSION:
            logger.error("%s has incorrect schema_version", path)
            flag = True
    except YAMLError:
        logger.error("%s is not a valid YAML file", path, exc_info=False)
        flag = True

if flag:
    sys.exit(1)

logger.info("All YAML files are valid")
