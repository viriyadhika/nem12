import os
import time

from .utils.files import get_upload_path
from .db import init_table
from .utils import logger


def run():
    if not os.path.exists(get_upload_path("")):
        os.mkdir(get_upload_path(""))

    for _ in range(3):
        try:
            init_table.run()
            break
        except Exception as e:
            logger.error(f"Error init table {e}")
            time.sleep(3)
