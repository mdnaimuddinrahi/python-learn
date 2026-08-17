import logging
from app.constant import BASE_DIR

logging.basicConfig(
    filename=BASE_DIR / "app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)