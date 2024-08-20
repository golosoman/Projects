
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.dispatcher import FSMContext
from aiogram import types
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from app.Browser import Browser
import time
from bs4 import BeautifulSoup
from configs import config, Config
from app.AutoClicker import AutoClicker
from app.UserStates import UserStates
from app.handler.AuthHandler import AuthHandler
from app.handler.AutoClickerHandler import AutoClickerHandler

class BotManager:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.bot = Bot(token=config.API_TOKEN)
        self.autoclicker_config = AutoClicker(config)
        self.browser = Browser(config)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.setup_handlers()  #  Добавляем вызов setup_handlers

    def setup_handlers(self) -> None:
        print("Запуск setup_handlers (Загрузка обработчиков)")
        try:
            self.dp.register_message_handler(self.start_command, commands=['start'])
            self.dp.register_message_handler(self.help_command, commands=['help'])
            self.dp.register_message_handler(AuthHandler(self.config, self.browser).auth_command, commands=['auth'])
            self.dp.register_message_handler(self.reload_command, commands=['reload'])
            self.dp.register_message_handler(self.get_available_clicks_command, commands=['get_available_clicks'])
            self.dp.register_message_handler(AutoClickerHandler(self.config, self.browser, self.autoclicker_config).start_autoclicker_command, commands=['start_autoclicker'])
            self.dp.register_message_handler(self.stop_autoclicker_command, commands=['stop_autoclicker'])
            self.dp.register_message_handler(self.print_page_text_command, commands=['get_text'])
            self.dp.register_message_handler(self.print_body_content_command, commands=['get_body'])
            self.dp.register_message_handler(AuthHandler(self.config, self.browser).auth_command, state=UserStates.code)
            # self.dp.register_message_handler(AuthHandler(self.config, self.browser).__code, state=UserStates.code)
            self.dp.register_message_handler(self.some_other_handler, lambda message: message.text.startswith('/'))
        except Exception as e:
            print(f"Возникла ошибка: {e}")

    async def help_command(self, message: types.Message) -> None:
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
        print("Запуск handler start")
        try:
            await message.answer("Привет! Я могу помочь авторизоваться в личном кабинете ALfaBank по QR-коду и запустить кликер.\n" +
                                "Чтобы посмотреть полный список моих команд введите  \n/help Чтобы авторизоваться введите /auth")
        except Exception as e:
            print(f"Возникла ошибка: {e}")
        
    async def stop_autoclicker_command(self, message: types.Message) -> None:
        print("Запуск stop_autoclicker")
        try:
            if not self.autoclicker_config.get_status():
                await message.answer("Автокликер не запущен.")
                return

            self.autoclicker_config.set_status(False)
            # Отмена задачи автокликера
            task = self.autoclicker_config.get_autoclicker_thread()
            if task is not None:
                task.cancel()
                self.autoclicker_config.set_status(False)
            await message.answer("Кликер был остановлен.")
        except Exception as e:
            print(f"Возникла ошибка: {e}")

    async def get_available_clicks_command(self, message: types.Message) -> None:
        try:
            # Ожидание появления элемента с текстом
            element = self.browser.get_wait_time().until(EC.presence_of_element_located((By.XPATH, self.config.AVAILABLE_CLICKS_XPATH)))
            await message.answer(f"Текст элемента: {element.text}")
        except Exception as e:
            print(f"Ошибка при получении текста: {e}")
            await message.answer(f"Ошибка при получении текста: {e}") 

    async def reload_command(self, message: types.Message) -> None:
        try:
            self.browser.get_driver().refresh()
            await message.answer("Страница перезагружена.")
        except Exception as e:
            await message.answer(f"Не удалось перезагрузить страницу, ошибка: {e}")

    def print_page_text_command(self) -> None:
        try:
            page_source = self.browser.get_driver().find_element(By.TAG_NAME, "body").text
            print(f"Текст страницы: {page_source}") # Запись в лог
        except Exception as e:
            print(f"Ошибка при получении текста страницы: {e}") # Запись ошибки в лог
        finally:
            print('-' * 30)

    def print_body_content_command(self) -> None:
        """
        Выводит в консоль все, что находится в <body> текущей страницы.
        """
        try:
            html_code = self.browser.get_driver().page_source
            soup = BeautifulSoup(html_code, 'html.parser')
            body = soup.find('body')

            if body:
                print(body.prettify())  # Выводит разметку body в отформатированном виде
            else:
                print("Тег <body> не найден на странице.")
        except Exception as e:
            print(f"Возникла ошибка: {e}")
        finally:
            print('-' * 30)

    
    async def some_other_handler(self, message: types.Message) -> None:
        await message.reply("Тутуту, такой команды нету, попробуйте что-то другое!")

    def start(self) -> None:
        start_polling(self.dp, skip_updates=True)