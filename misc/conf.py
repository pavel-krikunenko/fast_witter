import json
import logging
import os


logger = logging.getLogger(__name__)


def read_config(path: str):
    if not os.path.exists(path):
        logger.error(f"Config not found at {path}")
        return None
    with open(path, "r") as fd:
        return json.load(fd)