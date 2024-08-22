from asyncio import Task
from config import config, Config
from ..Log import logger
import asyncio


class AutoClicker:
    """
    Класс, управляющий автоматическим кликанием.

    Атрибуты:
        __autoclicker_enabled: Булевый флаг, определяющий, включен ли автоклик. По умолчанию False.
        __count_clicks_per_second: Целое число, определяющее количество кликов в секунду.
        __autoclicker_thread: Объект asyncio.Task, представляющий задачу, отвечающую за выполнение кликов.
    """

    def __init__(self, config: Config) -> None:
        """
        Инициализирует объект AutoClicker.

        Args:
            config: Объект конфигурации Config, используемый для установки начального количества кликов в секунду.
        """
        logger.info("Запуск __init__ AutoClicker")
        self.__autoclicker_enabled = False
        self.__count_clicks_per_second = float(config.COUNT_CLICKS_PER_SECOND)
        self.__autoclicker_thread = None
        logger.info("Завершение __init__ AutoClicker")

    def set_clicks_per_second(self, count_clicks: float) -> None:
        """
        Устанавливает новое количество кликов в секунду.

        Args:
            count_clicks: Новое количество кликов в секунду.
        """
        self.__count_clicks_per_second = count_clicks
        logger.debug("Отработал set_clicks_per_second AutoClicker")

    def get_clicks_per_second(self) -> float:
        """
        Возвращает текущее количество кликов в секунду.

        Returns:
            Текущее количество кликов в секунду.
        """
        logger.debug("Отработал get_clicks_per_second AutoClicker")
        return self.__count_clicks_per_second

    def set_status(self, status: bool) -> None:
        """
        Устанавливает новое состояние автоклика (включено/выключено).

        Args:
            status: Новое состояние автоклика (True - включено, False - выключено).
        """
        self.__autoclicker_enabled = status
        logger.debug("Отработал set_status AutoClicker")

    def get_status(self) -> bool:
        """
        Возвращает текущее состояние автоклика.

        Returns:
            Текущее состояние автоклика (True - включено, False - выключено).
        """
        logger.debug("Отработал get_status AutoClicker")
        return self.__autoclicker_enabled

    def set_autoclicker_thread(self, task: Task) -> None:
        """
        Устанавливает задачу, выполняющую клики.

        Args:
            task: Объект asyncio.Task, представляющий задачу, отвечающую за выполнение кликов.
        """
        logger.debug("Отработал set_autoclicker_thread AutoClicker")
        self.__autoclicker_thread = task

    async def create_task(self, loop_function, *args) -> bool:
        """
        Создает и запускает задачу, выполняющую автоклик.

        Args:
            loop_function: Функция, которую нужно запускать в цикле.
            *args: Аргументы, передаваемые функции loop_function.

        Returns:
            True, если задача запущена успешно, False в противном случае.
        """
        logger.debug(f"Запуск create_task AutoClicker")

        if self.__autoclicker_enabled:
            logger.warning("Задача уже запущена.")
            return False

        try:
            # Запускаем автокликер в отдельном потоке
            logger.debug("create_task  AutoClicker Почти в потоке")
            self.__autoclicker_enabled = True
            self.__autoclicker_thread = asyncio.create_task(
                loop_function(*args))
            logger.debug("create_task  AutoClicker Создал поток")
            logger.debug(f"Успешное завершение create_task AutoClicker")
            return True
        except asyncio.CancelledError:
            logger.warning("Задача была отменена во время создания.")
            self.__autoclicker_enabled = False
            return False
        except Exception as e:
            logger.error(f"Ошибка при создании задачи: {e}")
            self.__autoclicker_enabled = False
            return False

    async def delete_task(self) -> bool:
        """
        Отменяет задачу автоклика.

        Возвращает:
            True, если задача отменена успешно, False в противном случае.
        """
        logger.debug(f"Запуск delete_task AutoClicker")
        try:
            self.__autoclicker_thread.cancel()
        except asyncio.CancelledError:
            logger.debug("Задача уже отменена!")
            return False
        except Exception as e:
            logger.error(f"Ошибка при отмене задачи: {e}")
            return False
        else:
            logger.debug("Задача отменена успешно!")
            done, pending = await asyncio.wait([self.__autoclicker_thread])
            if done:
                self.__autoclicker_thread = None
                self.__autoclicker_enabled = False
                logger.debug("Задача завершена!")
                return True
            else:
                logger.warning(
                    "Задача не завершилась, возможно, произошла ошибка.")
                return False

    def get_autoclicker_thread(self) -> Task:
        """
        Возвращает задачу, выполняющую клики.

        Returns:
            Объект asyncio.Task, представляющий задачу, отвечающую за выполнение кликов.
        """
        logger.debug("Отработал get_autoclicker_thread AutoClicker")
        return self.__autoclicker_thread
