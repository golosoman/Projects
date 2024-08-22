import asyncio
from aiogram import types
from selenium.webdriver.common.by import By
from aiogram.dispatcher import FSMContext
from selenium.webdriver.support import expected_conditions as EC
from config import config, Config
from ..Browser import Browser
from ..Clicker import AutoClicker
from ..BaseTemplate import BaseHandler
from ..Log import logger
from ..State import UserStates


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
        super().__init__(config)
        logger.info("Запуск __init__ AutoClickerHandler")
        self.browser = browser
        self.autoclicker_config = AutoClicker(config)
        logger.info("Завершение __init__ AutoClickerHandler")

    async def change_click_rate_command(self, message: types.Message):
        """
        Обработка команды изменения скорости клика.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        logger.info("Запуск change_click_rate_command AutoClickerHandler")
        try:
            await UserStates.click_rate.set()
            await message.reply("Введите новое количество кликов в секунду:")
        except Exception as e:
            logger.error(
                f"change_click_rate_command AutoClickerHandler был завершен с ошибкой! {e}")
        logger.info("Завершение change_click_rate_command AutoClickerHandler")

    async def process_click_rate(self, message: types.Message, state: FSMContext):
        """
        Обработка ввода новой скорости клика.

        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния.
        """
        logger.info("Запуск process_click_rate AutoClickerHandler")
        try:
            new_click_rate = float(message.text)
            # Обновление конфигурации автокликера
            self.autoclicker_config.set_clicks_per_second(new_click_rate)
            await message.reply(f"Количество кликов в секунду успешно изменено на {new_click_rate}")
        except ValueError:
            logger.error(
                f"Некорректный ввод. Что-то не так с числом: {message.text}")
            await message.reply("Некорректный ввод. Введите число.")
        except Exception as e:
            logger.error(
                f"process_click_rate AutoClickerHandler был завершен с ошибкой! {e}")
        finally:
            await state.finish()
        logger.info("Завершение process_click_rate AutoClickerHandler")

    async def start_autoclicker_command(self, message: types.Message) -> None:
        """
        Обработка команды запуска автокликера.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        logger.info("Запуск start_autoclicker_command AutoClickerHandler")
        try:
            # Проверяем, уже ли открыта страница игры
            current_url = self.browser.get_driver().current_url
            if current_url != self.config.GAME_URL:
                self.browser.get_driver().get(self.config.GAME_URL)
            
             # Проверяем, есть ли запущенный автокликер
            if self.autoclicker_config.get_status():
                await message.answer("Автокликер уже запущен.")
            else:
                if (await self.autoclicker_config.create_task(self.__autoclick_loop, message)):
                    await message.answer(f"Автокликер запущен со скоростью {self.autoclicker_config.get_clicks_per_second()} кликов в секунду.")
                else:
                    raise asyncio.CancelledError("Не удалось создать задачу!")
            # Выводим сообщение после запуска задачи
            await message.answer("Кликер начал кликать :D")
        except asyncio.CancelledError as e:
            logger.error(
                f"start_autoclicker_command AutoClickerHandler был завершен с ошибкой! {e}")
            await message.answer(f"Что-то пошло не так, не удалось запустить кликер!")
        except Exception as e:
            logger.error(
                f"start_autoclicker_command AutoClickerHandler был завершен с ошибкой! {e}")
            await message.answer(f"Что-то пошло не так, не удалось запустить кликер!")
        logger.info("Завершение start_autoclicker_command AutoClickerHandler")

    async def __autoclick_loop(self, message: types.Message) -> None:
        """
        Цикл автокликера.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        logger.info("Запуск __autoclick_loop AutoClickerHandler")
        try:
            element = self.browser.get_wait_time().until(
                EC.presence_of_element_located((By.XPATH, self.config.CLICK_TARGET_XPATH)))
            count_clicks = 0
            logger.debug("Элемент для кликов на странице был найден!")
            while True:
                try:
                    # Задержка между кликами
                    await asyncio.sleep(1 / self.autoclicker_config.get_clicks_per_second())
                    # Клик по элементу
                    element.click()
                    count_clicks += 1
                    if (count_clicks == 10000):
                        logger.debug(
                            f"Клик! {count_clicks} __autoclick_loop AutoClickerHandler")
                        count_clicks = 0
                    # Проверка статуса кликера
                    if (not self.autoclicker_config.get_status()):
                        logger.debug(
                            f"Выходим из цикла __autoclick_loop AutoClickerHandler")
                        break
                except Exception as e:
                    logger.error(
                        f"__autoclick_loop AutoClickerHandler ошибка внутри цикла!")
                    raise Exception(
                        f"__autoclick_loop AutoClickerHandler ошибка внутри цикла! {e}")
        except Exception as e:
            logger.error(
                f"__autoclick_loop AutoClickerHandler был завершен с ошибкой! {e}")
        logger.info("Завершение __autoclick_loop AutoClickerHandler")

    async def stop_autoclicker_command(self, message: types.Message) -> None:
        """
        Обработка команды остановки автокликера.

        Args:
            message (types.Message): Сообщение от пользователя.
        """
        logger.info("Запуск stop_autoclicker_command AutoClickerHandler")
        try:
            if not self.autoclicker_config.get_status():
                await message.answer("Автокликер не запущен.")
            else:
                # Отмена задачи автокликера
                task = self.autoclicker_config.get_autoclicker_thread()
                if task is not None:
                    if (await self.autoclicker_config.delete_task()):
                        await message.answer("Кликер был остановлен.")
                    else:
                        raise asyncio.CancelledError(
                            "Не удалось остановить кликер!")
        except asyncio.CancelledError as e:
            logger.error(
                f"__autoclick_loop AutoClickerHandler был завершен с ошибкой! {e}")
            await message.answer("Что-то пошло не так, не удалось остановить кликер!")
        except Exception as e:
            logger.error(
                f"__autoclick_loop AutoClickerHandler был завершен с ошибкой! {e}")
            await message.answer("Что-то пошло не так, не удалось остановить кликер!")
        logger.info("Завершение stop_autoclicker_command AutoClickerHandler")
