from config import config
from app import BotManager, logger

try:
    if __name__ == "__main__":
        logger.info("Запуск программы!")
        bot_manager = BotManager(config)
        bot_manager.start()
        logger.info("Завершение программы!")
except Exception as e:
    logger.critical(f"Критическое заврешение программы: {e}")
