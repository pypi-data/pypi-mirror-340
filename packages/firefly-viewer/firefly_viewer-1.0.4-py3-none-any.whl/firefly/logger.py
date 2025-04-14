import logging
import sys
from .config import DEBUG

def setup_logger():
    logger = logging.getLogger("FireflyViewer")
    
    if DEBUG:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("firefly_debug.log"),
                logging.StreamHandler(sys.stdout),
            ],
        )
    else:
        logger.addHandler(logging.NullHandler())
    
    return logger

logger = setup_logger()