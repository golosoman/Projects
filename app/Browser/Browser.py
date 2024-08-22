from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from config import config, Config
from ..Log import logger


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
        logger.info("Запуск __init__ Browser")
        self.__driver = self.init_driver()
        self.__wait_time = WebDriverWait(
            self.__driver, int(config.WEB_DRIVER_WAIT))
        logger.info("Завершение __init__ Browser")

    def init_driver(self, config: Config) -> webdriver.Chrome | webdriver.Firefox:
        """
        Инициализирует драйвер браузера.

        Args:
            config: Объект конфигурации Config, используемый для настройки браузера.

        Returns:
            Объект WebDriver, представляющий драйвер браузера.
        """
        logger.info("Запуск init_driver Browser")
        if config.TYPE_BROWSER == "CHROME":
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')
            driver = webdriver.Chrome(
                service=ChromeService(), options=chrome_options)
        elif config.TYPE_BROWSER == "FIREFOX":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument('--headless=new')
            driver = webdriver.Firefox(
                service=FirefoxService(), options=firefox_options)
        else:
            raise ValueError("Неверный тип браузера в конфигурации.")

        logger.info("Завершение init_driver Browser")
        return driver

    def get_driver(self) -> webdriver.Chrome | webdriver.Firefox:
        """
        Возвращает объект WebDriver.

        Returns:
            Объект Chrome, представляющий драйвер браузера.
        """
        logger.debug("Отработал get_driver Browser")
        return self.__driver

    def get_wait_time(self) -> WebDriverWait:
        """
        Возвращает объект WebDriverWait.

        Returns:
            Объект WebDriverWait, отвечающий за ожидание загрузки элементов на странице.
        """
        logger.debug("Отработал get_wait_time Browser")
        return self.__wait_time

    def set_wait_time(self, wait_time: int) -> None:
        """
        Устанавливает новое время ожидания для WebDriverWait.

        Args:
            wait_time: Новое время ожидания в секундах.
        """
        self.__wait_time = WebDriverWait(self.__driver, wait_time)
        logger.debug("Отработал set_wait_time Browser")

    def __del__(self) -> None:
        """
        Закрывает драйвер браузера при удалении объекта Browser.
        """
        logger.info("Запуск __del__ Browser")
        self.__driver.quit()
        logger.info("Завершение __del__ Browser")
