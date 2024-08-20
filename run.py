from app import BotManager
from configs import config

if __name__ == "__main__":
    bot_manager = BotManager(config)
    bot_manager.start()