import os
import json
from deployment.logger import get_logger

logger = get_logger()


def load_json_file(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        raise


def load_text_file(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading text file {file_path}: {e}")
        raise
