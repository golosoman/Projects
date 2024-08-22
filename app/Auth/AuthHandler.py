from aiogram import types
from aiogram.dispatcher import FSMContext
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
import time
from config import config, Config
from PIL import Image
from ..State import UserStates
from ..Browser import Browser
from ..BaseTemplate import BaseHandler
from ..Log import logger


class AuthHandler(BaseHandler):
    """
    Класс для управления авторизацией.
    """

    def __init__(self, config: Config, browser: Browser) -> None:
        """
        Инициализация обработчика авторизации.

        Args:
            config (Config): Объект конфигурации.
            browser (Browser): Объект браузера.
        """
        logger.info("Запуск __init__ AuthHandler")
        super().__init__(config)
        self.browser = browser
        logger.info("Завершение __init__ AuthHandler")

    async def auth_command(self, message: types.Message) -> None:
        """
        Обработка команды авторизации.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        logger.info("Запуск auth_command AuthHandler")
        try:
            await message.answer("Запускаю приложение AlfaBank. Скоро будет QR-код, приготовьте камеру.")
            await self.__process_qr(message)
        except Exception as e:
            logger.error(f"Авторизация завершена с ошибкой! {e}")
            await message.answer("Произошла ошибка при авторизации!")
        logger.info("Завершение auth_command AuthHandler")

    async def __process_qr(self, message: types.Message) -> None:
        """
        Обработка QR-кода.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        logger.info("Запуск __process_qr AuthHandler")
        try:
            await self.__execute_qr(message)
            await message.answer("Пожалуйста подождите. Авторизация займет некоторое время")

            # НУЖНО СПРОСИТЬ ПОЛЬЗОВАТЕЛЯ, ВОСПОЛЬЗОВАЛЯ ЛИ ОН QR КОДОМ
            # await message.answer("Вы использовали QR-код? (да/нет)")

            time.sleep(10)
            self.browser.get_driver().get(self.config.LK_URL)

            # Авторизация - возможно попросят установить секретный код
            if (await self.__authorize_by_qr()):
                # Запрос секретного кода
                logger.info("В __process_qr появилась кнопка доверия")
                await message.answer("Введите секретный код:")
                await UserStates.code.set()

            await message.answer("Чтобы запустить автокликер, используйте команду /start_autoclicker.")
            logger.info("__process_qr авторизация завершена успешно!")
        except Exception as e:
            logger.error("__process_qr AuthHandler был завершен с ошибкой!")
            raise e
        logger.info("Завершение __process_qr AuthHandler")

    async def __execute_qr(self, message: types.Message) -> None:
        """
        Получение и отправка QR-кода пользователю.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        logger.info("Запуск __execute_qr AuthHandler")
        try:
            # Парсинг QR-кода с сайта
            qr_image = await self.__get_qr_from_website()

            # Сохранение изображения в формате BytesIO
            qr_bytes = BytesIO()
            qr_image.save(qr_bytes, format='PNG')
            qr_bytes.seek(0)

            if (qr_bytes is None):
                logger.error(f"qr_bytes вернул None")
                raise Exception('Не удалось получить qrCode')

            # Отправка изображения пользователю
            await message.answer_photo(qr_bytes, caption="Чтобы получить новый QR-код, используйте команду /get_qr.")
        except Exception as e:
            logger.error("__execute_qr AuthHandler был завершен с ошибкой!")
            raise e
        logger.info("Завершение __execute_qr AuthHandler")

    async def __get_qr_from_website(self) -> Image:
        """
        Получение QR-кода с сайта.

        Returns:
            Image: QR-код в формате PIL.Image.
        """
        logger.info("Запуск __get_qr_from_website AuthHandler")
        try:
            self.browser.get_driver().get(self.config.AUTH_URL)

            # Ждем, пока элемент canvas с QR-кодом не будет загружен
            canvas = self.browser.get_wait_time().until(
                EC.presence_of_element_located((By.XPATH, self.config.QR_XPATH)))

            # Извлечение изображения из элемента canvas
            qr_image = Image.open(BytesIO(canvas.screenshot_as_png))

            # Проверка размера изображения
            if qr_image.size[0] <= 0 or qr_image.size[1] <= 0:
                logger.error("Возникла ошибка проверки размера изображения!")
                raise ValueError("QR-код не загружен полностью.")
            logger.info("Завершение __get_qr_from_website AuthHandler")
            return qr_image
        except Exception as e:
            logger.error(
                "__get_qr_from_website AuthHandler был завершен с ошибкой!")
            raise e

    async def __authorize_by_qr(self) -> bool:
        """
        Авторизация по QR-коду.
        """
        logger.info("Запуск __authorize_by_qr AuthHandler")
        try:
            self.browser.get_driver().get(self.config.LK_URL)
            # Ждем появления кнопки "Доверять"
            self.browser.get_wait_time().until(EC.element_to_be_clickable(
                (By.XPATH, self.config.TRUST_BUTTON_XPATH)))
            # Клик по кнопке "Доверять"
            self.browser.get_driver().find_element(
                By.XPATH, self.config.TRUST_BUTTON_XPATH).click()
            logger.info("Завершение __authorize_by_qr AuthHandler")
            return True
        except Exception as e:
            logger.error(
                f"__authorize_by_qr AuthHandler был завершен с ошибкой: {e}")
            return False

    async def __handle_code(self, message: types.Message, state: FSMContext) -> None:
        """
        Обработчик ввода секретного кода.
        """
        logger.info("Запуск __handle_code AuthHandler")
        try:
            code = message.text
            # Проверка ввода
            if len(code) != 6:
                await message.reply("Секретный код должен состоять из шести цифр.")
                raise ValueError(
                    "Секретный код должен состоять из шести цифр.")
            else:
                await self.__complete_authorization(code)
                await message.answer("Авторизация завершена!")
                await state.finish()
        except Exception as e:
            logger.error(f"Ошибка __handle_code AuthHandler: {e}")
            await message.reply("Произошла ошибка при авторизации. Попробуйте снова.")
        logger.info("Завершение __handle_code AuthHandler")

    async def __complete_authorization(self, code: str) -> None:
        """
        Завершение авторизации.
        """
        logger.info("Запуск __complete_authorization AuthHandler")
        try:
            # Вводим секретный код
            self.browser.get_driver().find_element(
                By.XPATH, self.config.CODE_INPUT_XPATH_1).send_keys(code)
            self.browser.get_driver().find_element(
                By.XPATH, self.config.CODE_INPUT_XPATH_2).send_keys(code)

            # Нажимаем кнопку "Сохранить"
            self.browser.get_driver().find_element(
                By.XPATH, self.config.SAVE_BUTTON_XPATH).click()

        except Exception as e:
            logger.error(f"Ошибка __complete_authorization AuthHandler: {e}")
            raise e
        logger.info("Завершение __complete_authorization AuthHandler")
