from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from configs import config, Config
from selenium import webdriver
from selenium.webdriver import Chrome

class Browser:
    """
    Класс, представляющий браузер для автоматизации действий.

    Атрибуты:
        driver: Объект WebDriver, представляющий браузер.
        __wait_time: Объект WebDriverWait, отвечающий за ожидание загрузки элементов на странице.
    """

    def __init__(self, config: Config) -> None:
        """
        Инициализирует объект Browser.

        Args:
            config: Объект конфигурации Config, используемый для настройки браузера.
        """
        self.__driver = self.init_driver()  # Инициализация self.__driver
        self.__wait_time = WebDriverWait(self.__driver, int(config.WEB_DRIVER_WAIT))

    def init_driver(self) -> Chrome:
        """
        Инициализирует драйвер браузера.

        Args:
            None

        Returns:
            Объект Chrome, представляющий драйвер браузера.
        """
        options = Options()
        if config.TYPE_BROWSER == "CHROME":
            options.add_argument('--headless=new')
            driver = webdriver.Chrome(options=options)
        return driver
    
    def get_driver(self) -> Chrome:
        """
        Возвращает объект WebDriver.

        Returns:
            Объект Chrome, представляющий драйвер браузера.
        """
        return self.__driver 
    
    def get_wait_time(self) -> WebDriverWait:
        """
        Возвращает объект WebDriverWait.

        Returns:
            Объект WebDriverWait, отвечающий за ожидание загрузки элементов на странице.
        """
        return self.__wait_time
    
    def set_wait_time(self, wait_time: int) -> None:
        """
        Устанавливает новое время ожидания для WebDriverWait.

        Args:
            wait_time: Новое время ожидания в секундах.
        """
        self.__wait_time = WebDriverWait(self.__driver, wait_time)

    def __del__(self) -> None:  # Использование правильного имени метода
        """
        Закрывает драйвер браузера при удалении объекта Browser.
        """
        self.__driver.quit() 
