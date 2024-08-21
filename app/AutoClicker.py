from configs import config, Config
from asyncio import Task

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
        self.__autoclicker_enabled = False
        self.__count_clicks_per_second= float(config.COUNT_CLICKS_PER_SECOND)
        self.__autoclicker_thread = None

    def set_clicks_per_second(self, count_clicks: float) -> None:
        """
        Устанавливает новое количество кликов в секунду.

        Args:
            count_clicks: Новое количество кликов в секунду.
        """
        self.__count_clicks_per_second = count_clicks

    def get_clicks_per_second(self) -> float:
        """
        Возвращает текущее количество кликов в секунду.

        Returns:
            Текущее количество кликов в секунду.
        """
        return self.__count_clicks_per_second
    
    def set_status(self, status: bool) -> None:
        """
        Устанавливает новое состояние автоклика (включено/выключено).

        Args:
            status: Новое состояние автоклика (True - включено, False - выключено).
        """
        self.__autoclicker_enabled = status

    def get_status(self) -> bool:
        """
        Возвращает текущее состояние автоклика.

        Returns:
            Текущее состояние автоклика (True - включено, False - выключено).
        """
        return self.__autoclicker_enabled
    
    def set_autoclicker_thread(self, task: Task) -> None:
        """
        Устанавливает задачу, выполняющую клики.

        Args:
            task: Объект asyncio.Task, представляющий задачу, отвечающую за выполнение кликов.
        """
        self.__autoclicker_thread = task

    def get_autoclicker_thread(self) -> Task:
        """
        Возвращает задачу, выполняющую клики.

        Returns:
            Объект asyncio.Task, представляющий задачу, отвечающую за выполнение кликов.
        """
        return self.__autoclicker_thread