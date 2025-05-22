import logging

from app.config import settings

LOGLEVEL = settings.LOGLEVEL
logging.basicConfig(level=LOGLEVEL, style="{")
logger = logging.getLogger("athena_backend")
logging.getLogger("aiokafka").setLevel(logging.INFO)
logging.getLogger("apscheduler.executors.default").setLevel(logging.ERROR)
logging.getLogger("apscheduler.scheduler").setLevel(logging.ERROR)
