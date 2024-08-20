
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram import types
from app.Browser import Browser
import time
from configs import config, Config
from app.UserStates import UserStates
from app.handler.AuthHandler import AuthHandler
from app.handler.AutoClickerHandler import AutoClickerHandler
from app.handler.BrowserHandler import BrowserHandler

class BotManager:
    """
    Класс, управляющий ботом. Инициализирует бота, браузер, диспетчер и обработчики.
    """
    def __init__(self, config: Config) -> None:
        """
        Инициализирует бот, браузер, диспетчер и обработчики.

        Args:
            config (Config): Конфигурационные данные бота.
        """
        self.config = config
        self.bot = Bot(token=self.config.API_TOKEN)
        self.browser = Browser(self.config)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.__click_handler = AutoClickerHandler(self.config, self.browser)
        self.__auth_handler = AuthHandler(self.config, self.browser)
        self.__browser_handler = BrowserHandler(self.config, self.browser)
        self.setup_handlers()  #  Добавляем вызов setup_handlers

    def setup_handlers(self) -> None:
        """
        Регистрирует обработчики команд бота.
        """
        print("Запуск setup_handlers (Загрузка обработчиков)")
        try:
            self.dp.register_message_handler(self.start_command, commands=['start'])
            self.dp.register_message_handler(self.help_command, commands=['help'])
            self.dp.register_message_handler(self.__auth_handler.auth_command, commands=['auth'])
            self.dp.register_message_handler(self.__browser_handler.reload_command, commands=['reload'])
            self.dp.register_message_handler(self.__browser_handler.get_available_clicks_command, commands=['get_available_clicks'])
            self.dp.register_message_handler(self.__click_handler.start_autoclicker_command, commands=['start_autoclicker'])
            self.dp.register_message_handler(self.__click_handler.stop_autoclicker_command, commands=['stop_autoclicker'])
            self.dp.register_message_handler(self.__browser_handler.print_page_text_command, commands=['get_text'])
            self.dp.register_message_handler(self.__browser_handler.print_body_content_command, commands=['get_body'])
            self.dp.register_message_handler(self.__auth_handler.auth_command, state=UserStates.code)
            self.dp.register_message_handler(self.some_other_handler, lambda message: message.text.startswith('/'))
        except Exception as e:
            print(f"Возникла ошибка: {e}")


    async def help_command(self, message: types.Message) -> None:
        """
        Обработчик команды /help. Выводит список доступных команд.
        """
        print("Запуск handler help")
        try:
            await message.answer("Список доступных команд:\n"+
                "1) /start - команда приветствия\n"+
                "2) /help - получение информации по списку доступных команд\n"+
                "3) /auth - авторизация в приложении АльфаБанка по QR\n"+
                "4) /reload - перезагрузка текущей страницы браузера\n"+
                "5) /get_available_clicks - получить количество доступных кликов (перед этим нужно авторизоваться)\n"+
                "6) /start_autoclicker - запуск автокликера (перед этим нужно авторизоваться)\n"+
                "7) /stop_autoclicker - остановка автокликера (перед этим нужно авторизоваться)\n"+
                "8) /get_text - получить текст из текущей страницы\n"+
                "9) /get_body - получить body из текущей страницы\n"
                )
        except Exception as e:
            print(f"Возникла ошибка: {e}")
        

    async def start_command(self, message: types.Message) -> None:
        """
        Обработчик команды /start. Выводит приветственное сообщение.
        """
        print("Запуск handler start")
        try:
            await message.answer("Привет! Я могу помочь авторизоваться в личном кабинете ALfaBank по QR-коду и запустить кликер.\n" +
                                "Чтобы посмотреть полный список моих команд введите  \n/help Чтобы авторизоваться введите /auth")
        except Exception as e:
            print(f"Возникла ошибка: {e}")

    async def some_other_handler(self, message: types.Message) -> None:
        await message.reply("Тутуту, такой команды нету, попробуйте что-то другое!")

    def start(self) -> None:
        start_polling(self.dp, skip_updates=True)