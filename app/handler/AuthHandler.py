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

class AuthHandler:
    def __init__(self, config: Config, browser: Browser ) -> None:
        print("Запуск __init__ AuthHandler")
        self.config = config
        self.browser = browser

    # ==========================Авторизация (начало)===================================================

    async def auth_command(self, message: types.Message) -> None:
        print("Запуск handler auth")
        try:
            await message.answer("Запускаю приложение AlfaBank. Скоро будет QR-код, приготовьте камеру.")
            await self.__process_qr(message)
        except Exception as e:
            print(f"Авторизация завершена с ошибкой! {e}")
            await message.answer(f"Произошла ошибка при авторизации: {e}")
    
    async def __execute_qr(self, message: types.Message) -> None:
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
            await message.answer_photo(qr_bytes, caption="QR-код:\nЧтобы получить новый QR-код, используйте команду /get_qr.")
        except Exception as e:
            print("qr не удалось получить")
            raise e


    async def __process_qr(self, message: types.Message) -> None:
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
        print("Запуск get_qr_from_website")
        try:
            self.browser.get_driver().get(self.config.AUTH_URL)

            # Добавьте задержку для загрузки QR-кода (например, 3 секунды) 
            time.sleep(3)

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
        self.browser.get_driver().get(self.config.LK_URL)
        try:
            # Ждем появления кнопки "Доверять"
            self.browser.get_wait_time().until(EC.element_to_be_clickable((By.XPATH, self.config.TRUST_BUTTON_XPATH)))

            # Нажимаем кнопку "Доверять"
            self.browser.get_driver().find_element(By.XPATH, self.config.TRUST_BUTTON_XPATH).click()
            print("Кнопка доверять найдена и нажата")
        except:
            print("Кнопка 'Доверять' не найдена, пропуск шага")
            return False
        return True
    
    async def __code(self, message: types.Message, state: FSMContext) -> None:
        print("Запуск handler-состояния code")
        try:
            await state.update_data(code=message.text)
            await self.__complete_authorization(message, state)
            await state.finish()
        except Exception as e:
            raise e
        

    async def __complete_authorization(self, message: types.Message, state: FSMContext) -> None:
        print("Запуск complete_authorization")
        data = await state.get_data()
        code = data['code']

        try:
             # Проверка ввода
            if len(code) != 6:
                raise ValueError("Секретный код должен состоять из шести цифр.")

            # Вводим секретный код
            self.browser.get_driver().find_element(By.XPATH, self.config.CODE_INPUT_XPATH_1).send_keys(code)
            self.browser.get_driver().find_element(By.XPATH, self.config.CODE_INPUT_XPATH_2).send_keys(code)

            # Нажимаем кнопку "Сохранить"
            self.browser.get_driver().find_element(By.XPATH, self.config.SAVE_BUTTON_XPATH).click()

            await message.answer("Авторизация завершена!")
        except Exception as e:
            raise e
            # await message.answer(f"Произошла ошибка при авторизации и установке кода доверия: {e}")
            

    # ==========================Авторизация (конец)===================================================
