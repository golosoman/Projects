from aiogram import types
from configs import config, Config
import asyncio
from app.Browser import Browser
from app.AutoClicker import AutoClicker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from app.handler.BaseHandler import BaseHandler

class AutoClickerHandler(BaseHandler):
    """
    Класс для управления автокликерном.
    """
    def __init__(self, config: Config, browser: Browser) -> None:
        """
        Инициализация обработчика автокликера.

        Args:
            config (Config): Объект конфигурации.
            browser (Browser): Объект браузера.
        """
        print("Запуск init AutoClickerHandler")
        super().__init__(config)
        self.browser = browser
        self.autoclicker_config = AutoClicker(config)

    async def start_autoclicker_command(self, message: types.Message) -> None:
        """
        Обработка команды запуска автокликера.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        print("Запуск start_autoclicker")
        try:
            if self.autoclicker_config.get_status():
                await message.answer("Автокликер уже запущен.")
                return
            
            # Запускаем автокликер в отдельном потоке
            self.autoclicker_config.set_status(True)
            print("Почти в потоке")
            task = asyncio.create_task(self.__autoclick_loop(message))
            print("Создал поток")
            self.autoclicker_config.set_autoclicker_thread(task)  # Храним задачу, а не поток
            print("Теперь в потоке")
            await message.answer(f"Автокликер запущен со скоростью {self.autoclicker_config.get_clicks_per_second()} кликов в секунду.")
        except Exception as e:
            print(f"Возникла ошибка: {e}")
        
    async def __autoclick_loop(self, message: types.Message) -> None: 
        """
        Цикл автокликера.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        print("Запуск autoclick_loop")
        self.browser.get_driver().get(self.config.GAME_URL)
        element = self.browser.get_wait_time().until(EC.presence_of_element_located((By.XPATH, self.config.CLICK_TARGET_XPATH)))
        count_clicks = 0
        await message.answer("Кликер начал кликать :D")
        while True:
            try:
                # Задержка между кликами
                time = float(1 / self.autoclicker_config.get_clicks_per_second())
                await asyncio.sleep(time)

                # Клик по элементу
                element.click()
                count_clicks += 1
                
                if (count_clicks == 10000 ):
                    print("Клик! 10000")
                    element = self.browser.get_wait_time().until(EC.presence_of_element_located((By.XPATH, self.config.AVAILABLE_CLICKS_XPATH)))
                    # await message.answer(f"Текст элемента: {element.text}")
                    count_clicks = 0

                if (not self.autoclicker_config.get_status()):
                    break
            except Exception as e:
                # Если произошла ошибка, останавливаем автокликер
                self.autoclicker_config.set_status(False)
                raise e
        print('Кликер остановлен')
            
    async def stop_autoclicker_command(self, message: types.Message) -> None:
        """
        Обработка команды остановки автокликера.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
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
                self.autoclicker_config.set_autoclicker_thread = None
                self.autoclicker_config.set_status(False)
            await message.answer("Кликер был остановлен.")
        except Exception as e:
            print(f"Возникла ошибка: {e}")
