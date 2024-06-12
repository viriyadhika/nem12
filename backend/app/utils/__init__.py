import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    stream=sys.stdout,
)
