from aiogram import types
from configs import config, Config
import asyncio
from app.Browser import Browser
from app.AutoClicker import AutoClicker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class AutoClickerHandler:
    def __init__(self, config: Config, browser: Browser, autoclicker_config: AutoClicker) -> None:
        print("Запуск __init__ AutoClickerHandler")
        self.config = config
        self.browser = browser
        self.autoclicker_config = autoclicker_config
        

    # ==========================Запуск АвтоКликера (начало)===================================================

    async def start_autoclicker_command(self, message: types.Message) -> None:
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
        print("Запуск autoclick_loop")
        self.browser.get_driver().get(self.config.GAME_URL)
        element = self.browser.get_wait_time().until(EC.presence_of_element_located((By.XPATH, self.config.CLICK_TARGET_XPATH)))
        count_clicks = 0
        await message.answer("Кликер начал кликать :D")
        while self.autoclicker_config.get_status():
            try:
                # Задержка между кликами
                await asyncio.sleep(1 / self.autoclicker_config.get_clicks_per_second())
                # Клик по элементу
                element.click()
                count_clicks += 1
                if ( count_clicks == 5000 ):
                    print("Клик! 5000")
                    count_clicks = 0
            except Exception as e:
                # Если произошла ошибка, останавливаем автокликер
                self.autoclicker_config.set_status(False)
                raise e

        
    # ==========================Запуск АвтоКликера (конец)===================================================