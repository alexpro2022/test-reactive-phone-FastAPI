import logging

logging.basicConfig(
    level='INFO'.upper(),
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def log(func):
    async def wrapper(*args, **kwargs):
        logger.info('Loading...')
        [logger.info(item) async for item in func(*args, **kwargs)]
        logger.info('Successfully loaded')
    return wrapper


def load(func):
    async def wrapper(*args, **kwargs):
        data = [data async for data in func(*args, **kwargs)]
        yield data
        # Here may be a loading procedure (to DB, cache or file)
    return wrapper
