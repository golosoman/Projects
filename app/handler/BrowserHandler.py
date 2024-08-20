from aiogram import types
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from app.Browser import Browser
from configs import config, Config
from bs4 import BeautifulSoup
from app.handler.BaseHandler import BaseHandler

class BrowserHandler(BaseHandler):
    def __init__(self, config: Config, browser: Browser) -> None:
        super().__init__(config)
        self.browser = browser

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

    async def print_page_text_command(self, message: types.Message) -> None:
        try:
            page_source = self.browser.get_driver().find_element(By.TAG_NAME, "body").text
            print(f"Текст страницы: {page_source}") # Запись в лог
        except Exception as e:
            print(f"Ошибка при получении текста страницы: {e}") # Запись ошибки в лог
        finally:
            print('-' * 30)

    async def print_body_content_command(self, message: types.Message) -> None:
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