from aiogram import types
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from config import config, Config
from ..Browser import Browser
from ..BaseTemplate import BaseHandler
from ..Log import logger


class BrowserHandler(BaseHandler):
    def __init__(self, config: Config, browser: Browser) -> None:
        super().__init__(config)
        logger.info("Запуск __init__ BrowserHandler")
        self.browser = browser
        logger.info("Завершение __init__ BrowserHandler")

    async def get_available_clicks_command(self, message: types.Message) -> None:
        """
        Получение количества доступных кликов.

        Args:
            message: Сообщение от пользователя.
        """
        logger.info("Запуск get_available_clicks_command BrowserHandler")
        try:
            # Ожидание появления элемента с текстом
            element = self.browser.get_wait_time().until(
                EC.presence_of_element_located((By.XPATH, self.config.AVAILABLE_CLICKS_XPATH)))
            await message.answer(f"Текст элемента: {element.text}")
        except Exception as e:
            logger.error(
                f"get_available_clicks_command BrowserHandler был завершен с ошибкой! {e}")
            await message.answer(f"Что-то пошло не так. Не удалось получить количество доступных кликов!")
        logger.info("Завершение get_available_clicks_command BrowserHandler")

    async def get_my_game_money_command(self, message: types.Message) -> None:
        """
        Получение количества денег в игре.

        Args:
            message: Сообщение от пользователя.
        """
        logger.info("Запуск get_my_game_money_command BrowserHandler")
        try:
            # Ожидание появления элемента с текстом
            element = self.browser.get_wait_time().until(
                EC.presence_of_element_located((By.XPATH, self.config.MY_GAME_MONEY)))
            await message.answer(f"Количество денег: {element.text}")
        except Exception as e:
            logger.error(
                f"get_my_game_money_command BrowserHandler был завершен с ошибкой! {e}")
            await message.answer(f"Что-то пошло не так. Не удалось получить количество коинов")
        logger.info("Завершение get_my_game_money_command BrowserHandler")

    async def reload_command(self, message: types.Message) -> None:
        """
        Перезагрузка страницы в браузере.

        Args:
            message: Сообщение от пользователя.
        """
        logger.info("Запуск reload_command BrowserHandler")
        try:
            self.browser.get_driver().refresh()
            await message.answer("Страница перезагружена.")
        except Exception as e:
            logger.error(
                f"reload_command BrowserHandler был завершен с ошибкой! {e}")
            await message.answer(f"Не удалось перезагрузить страницу")
        logger.info("Завершение reload_command BrowserHandler")

    async def print_page_text_command(self, message: types.Message) -> None:
        """
        Печать текста всей страницы.

        Args:
            message: Сообщение от пользователя.
        """
        logger.info("Запуск print_page_text_command BrowserHandler")
        try:
            page_source = self.browser.get_driver().find_element(By.TAG_NAME, "body").text
            await message.answer(f"Текст страницы: {page_source}")
        except Exception as e:
            logger.error(
                f"print_page_text_command BrowserHandler был завершен с ошибкой! {e}")
            await message.answer("Не удалось получить текст со страницы!")
        logger.info("Завершение reload_command BrowserHandler")

    async def go_to_game_page_command(self, message: types.Message) -> None:
        """
        Переход на страницу игры.

        Args:
            message: Сообщение от пользователя.
        """
        logger.info("Запуск go_to_game_page_command BrowserHandler")
        try:
            self.browser.get_driver().get(self.config.GAME_URL)
            await self.print_page_text_command(message)
        except Exception as e:
            logger.error(
                f"go_to_game_page_command BrowserHandler был завершен с ошибкой! {e}")
            await message.answer("Не удалось загрузить страницу!")
        logger.info("Завершение go_to_game_page_command BrowserHandler")

    async def print_body_content_command(self, message: types.Message) -> None:
        """
        Выводит в консоль все, что находится в <body> текущей страницы.
        """
        logger.info("Запуск print_body_content_command BrowserHandler")
        try:
            html_code = self.browser.get_driver().page_source
            soup = BeautifulSoup(html_code, 'html.parser')
            body = soup.find('body')

            if body:
                await message.answer(f"Body: {body.prettify()}")
            else:
                await message.answer("Тег <body> не найден на странице.")

        except Exception as e:
            logger.error(
                f"print_page_text_command BrowserHandler был завершен с ошибкой! {e}")
            await message.answer("Что-то пошло не так!")
        logger.info("Завершение print_body_content_command BrowserHandler")
