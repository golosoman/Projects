from config import config, Config
from ..Log import logger


class BaseHandler:
    def __init__(self, config: Config) -> None:
        logger.info("Запуск __init__ BaseHandler")
        self.config = config
        logger.info("Завершение __init__ BaseHandler")
