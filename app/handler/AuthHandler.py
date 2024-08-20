from aiogram import types
from io import BytesIO
import time
from configs import config, Config
from app.UserStates import UserStates
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from aiogram.dispatcher import FSMContext
from app.Browser import Browser
from app.handler.BaseHandler import BaseHandler

class AuthHandler(BaseHandler):
    """
    Класс для управления авторизацией.
    """
    def __init__(self, config: Config, browser: Browser ) -> None:
        """
        Инициализация обработчика авторизации.

        Args:
            config (Config): Объект конфигурации.
            browser (Browser): Объект браузера.
        """
        print("Запуск init AuthHandler")
        super().__init__(config)
        self.browser = browser

    async def auth_command(self, message: types.Message) -> None:
        """
        Обработка команды авторизации.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        print("Запуск handler auth")
        try:
            await message.answer("Запускаю приложение AlfaBank. Скоро будет QR-код, приготовьте камеру.")
            await self.__process_qr(message)
        except Exception as e:
            print(f"Авторизация завершена с ошибкой! {e}")
            await message.answer(f"Произошла ошибка при авторизации: {e}")
    
    async def __execute_qr(self, message: types.Message) -> None:
        """
        Получение и отправка QR-кода пользователю.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        print("Запуск get_qr")
        try:
            # Парсинг QR-кода с сайта
            qr_image = await self.__get_qr_from_website()

            # Сохранение изображения в формате BytesIO
            qr_bytes = BytesIO()
            qr_image.save(qr_bytes, format='PNG')
            qr_bytes.seek(0)

            if (qr_bytes is None):
                raise Exception('Не удалось получить qrCode')
            
             # Отправка изображения пользователю
            await message.answer_photo(qr_bytes, caption="QR-код:nЧтобы получить новый QR-код, используйте команду /get_qr.")
        except Exception as e:
            print("qr не удалось получить")
            raise e


    async def __process_qr(self, message: types.Message) -> None:
        """
        Обработка QR-кода.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        print("Запуск функции process_qr")
        try:
            await self.__execute_qr(message)
            await message.answer("Пожалуйста подождите. Авторизация займет некоторое время")

            # НУЖНО СПРОСИТЬ ПОЛЬЗОВАТЕЛЯ, ВОСПОЛЬЗОВАЛЯ ЛИ ОН QR КОДОМ
            await message.answer("Вы использовали QR-код? (да/нет)")
            
            time.sleep(10)
            self.browser.get_driver().get(self.config.LK_URL)
            
            # Авторизация - возможно попросят установить секретный код
            if (await self.__authorize_by_qr()):
                # Запрос секретного кода
                await message.answer("Введите секретный код:")
                await UserStates.code.set()
            
            await message.answer("Чтобы запустить автокликер, используйте команду /start_autoclicker.")
            print("Авторизация завершена успешно!")
        except Exception as e:
            raise e


    async def __get_qr_from_website(self) -> Image:
        """
        Получение QR-кода с сайта.

        Returns:
            Image: QR-код в формате PIL.Image.
        """
        print("Запуск get_qr_from_website")
        try:
            self.browser.get_driver().get(self.config.AUTH_URL)

            # Добавьте задержку для загрузки QR-кода (например, 3 секунды) 
            # time.sleep(3)

            # Ждем, пока элемент canvas с QR-кодом не будет загружен
            canvas = self.browser.get_wait_time().until(EC.presence_of_element_located((By.XPATH, self.config.QR_XPATH)))

            # Извлечение изображения из элемента canvas
            qr_image = Image.open(BytesIO(canvas.screenshot_as_png))

            # Проверка размера изображения
            if qr_image.size[0] <= 0 or qr_image.size[1] <= 0: 
                raise Exception("QR-код не загружен полностью.")
            
            return qr_image
        except Exception as e:
            raise e
    
    async def __authorize_by_qr(self) -> bool:
        """
        Авторизация по QR-коду.

        Returns:
            bool: True, если авторизация прошла успешно, False в противном случае.
        """
        self.browser.get_driver().get(self.config.LK_URL)
        try:
            # Ждем появления кнопки "Доверять"
            self.browser.get_wait_time().until(EC.element_to_be_clickable((By.XPATH, self.config.TRUST_BUTTON_XPATH)))
            # Клик по кнопке "Доверять"
            #self.browser.get_driver().find_element(By.XPATH, self.config.TRUST_BUTTON_XPATH).click()
            await self.__get_qr_from_website()
            return True
        except Exception as e:
            return False
