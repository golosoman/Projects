
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram import types
import time
from config import config, Config
from ..Browser import Browser, BrowserHandler
from ..State import UserStates
from ..Auth import AuthHandler
from ..Clicker import AutoClickerHandler
from ..Log import logger


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
        logger.info("Запуск __init__ BotManager")
        self.config = config
        self.bot = Bot(token=self.config.API_TOKEN)
        self.browser = Browser(self.config)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.__click_handler = AutoClickerHandler(self.config, self.browser)
        self.__auth_handler = AuthHandler(self.config, self.browser)
        self.__browser_handler = BrowserHandler(self.config, self.browser)
        self.setup_handlers()  # Добавляем вызов setup_handlers
        logger.info("Завершение __init__ BotManager")

    def setup_handlers(self) -> None:
        """
        Регистрирует обработчики команд бота.
        """
        logger.info("Запуск setup_handlers BotManager")
        try:
            self.dp.register_message_handler(
                self.start_command, commands=['start'])
            self.dp.register_message_handler(
                self.help_command, commands=['help'])
            self.dp.register_message_handler(
                self.__auth_handler.auth_command, commands=['auth'])
            self.dp.register_message_handler(
                self.__browser_handler.reload_command, commands=['reload'])
            self.dp.register_message_handler(
                self.__browser_handler.get_available_clicks_command, commands=['get_available_clicks'])
            self.dp.register_message_handler(
                self.__click_handler.start_autoclicker_command, commands=['start_autoclicker'])
            self.dp.register_message_handler(
                self.__click_handler.stop_autoclicker_command, commands=['stop_autoclicker'])
            self.dp.register_message_handler(
                self.__click_handler.change_click_rate_command, commands=['change_click_rate'])
            self.dp.register_message_handler(
                self.__click_handler.process_click_rate, state=UserStates.click_rate)
            self.dp.register_message_handler(
                self.__browser_handler.print_page_text_command, commands=['get_text'])
            self.dp.register_message_handler(
                self.__browser_handler.print_body_content_command, commands=['get_body'])
            self.dp.register_message_handler(
                self.__browser_handler.go_to_game_page_command, commands=['go_to_game_page'])
            self.dp.register_message_handler(
                self.__browser_handler.get_my_game_money_command, commands=['get_my_game_money'])
            self.dp.register_message_handler(
                self.__auth_handler.__handle_code, state=UserStates.code)
            self.dp.register_message_handler(
                self.some_other_command, lambda message: message.text.startswith('/'))
        except Exception as e:
            logger.error(
                f"Не удалось завершить инициализацию бота в setup_handlers BotManager! {e}")
            raise e
        logger.info("Завершение setup_handlers BotManager")

    async def help_command(self, message: types.Message) -> None:
        """
        Обработчик команды /help. Выводит список доступных команд.
        """
        logger.info("Запуск help_command BotManager")
        try:
            list_command = [
                "/start - команда приветствия",
                "/help - получение информации по списку доступных команд",
                "/auth - авторизация в приложении АльфаБанка по QR",
                "/go_to_game_page - переход на страницу с игрой (перед этим нужно авторизоваться)",
                "/reload - перезагрузка текущей страницы браузера",
                "/start_autoclicker - запуск автокликера (перед этим нужно авторизоваться и быть в игре)",
                "/stop_autoclicker - остановка автокликера (перед этим нужно авторизоваться и быть в игре)",
                "/get_available_clicks - получить количество доступных кликов (перед этим нужно авторизоваться и быть в игре)",
                "/get_my_game_money - получить количество заработанных коинов",
                "/change_click_rate - изменить количество кликов в секунду",
                "/get_text - получить текст из текущей страницы",
                "/get_body - получить body из текущей страницы (скорее всего не сработает)",
            ]
            await message.answer("\n".join(f"{i+1})  {command} \n" for i, command in enumerate(list_command)))
        except Exception as e:
            logger.error(
                f"help_command BotManager был завершен с ошибкой! {e}")
            await message.answer("Не удалось получить список команд!")
        logger.info("Завершение help_command BotManager")

    async def start_command(self, message: types.Message) -> None:
        """
        Обработчик команды /start. Выводит приветственное сообщение.
        """
        logger.info("Запуск start_command BotManager")
        try:
            await message.answer("Привет! Я могу помочь авторизоваться в личном кабинете ALfaBank по QR-коду и запустить кликер.\n" +
                                 "Чтобы посмотреть полный список моих команд введите  \n/help Чтобы авторизоваться введите /auth")
        except Exception as e:
            logger.error(
                f"start_command BotManager был завершен с ошибкой! {e}")
        logger.info("Завершение start_command BotManager")

    async def some_other_command(self, message: types.Message) -> None:
        logger.info("Запуск some_other_command BotManager")
        try:
            await message.reply("Тутуту, такой команды нету, попробуйте что-то другое!")
        except Exception as e:
            logger.error(
                f"some_other_command BotManager был завершен с ошибкой! {e}")
            await message.answer("Что-то пошло не так!")
        logger.info("Завершение some_other_command BotManager")

    def start(self) -> None:
        logger.info("Запуск start BotManager")
        try:
            start_polling(self.dp, skip_updates=True)
        except Exception as e:
            logger.error(f"start BotManager был завершен с ошибкой! {e}")
        logger.info("Завершение start BotManager")
