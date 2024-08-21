import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка .env

class Config:
    """
    Класс, содержащий конфигурационные параметры приложения.

    Атрибуты:
        API_TOKEN: Токен API.
        AUTH_URL: URL-адрес для аутентификации.
        GAME_URL: URL-адрес для игры.
        LK_URL: URL-адрес для личного кабинета.
        QR_XPATH: XPath-селектор для элемента QR-кода.
        CLICK_TARGET_XPATH: XPath-селектор для элемента, по которому нужно кликать.
        AVAILABLE_CLICKS_XPATH: XPath-селектор для элемента, отображающего количество доступных кликов.
        TRUST_BUTTON_XPATH: XPath-селектор для кнопки "Доверие".
        CODE_INPUT_XPATH_1: XPath-селектор для первого поля ввода кода.
        CODE_INPUT_XPATH_2: XPath-селектор для второго поля ввода кода.
        SAVE_BUTTON_XPATH: XPath-селектор для кнопки "Сохранить".
        WEB_DRIVER_WAIT: Время ожидания загрузки элементов на странице в секундах.
        COUNT_CLICKS_PER_SECOND: Количество кликов в секунду.
        TYPE_BROWSER: Тип браузера.
    """
    API_TOKEN = os.getenv('API_TOKEN')
    AUTH_URL = os.getenv('AUTH_URL')
    GAME_URL = os.getenv('GAME_URL')
    LK_URL = os.getenv('LK_URL')
    QR_XPATH = os.getenv('QR_XPATH')
    CLICK_TARGET_XPATH = os.getenv('CLICK_XPATH')
    AVAILABLE_CLICKS_XPATH = os.getenv('AVAILABLE_CLICKS_XPATH')
    TRUST_BUTTON_XPATH = os.getenv('TRUST_BUTTON_XPATH')
    CODE_INPUT_XPATH_1 = os.getenv('CODE_INPUT_XPATH_1')
    CODE_INPUT_XPATH_2 = os.getenv('CODE_INPUT_XPATH_2')
    SAVE_BUTTON_XPATH = os.getenv('SAVE_BUTTON_XPATH')
    WEB_DRIVER_WAIT = int(os.getenv('WEB_DRIVER_WAIT'))
    COUNT_CLICKS_PER_SECOND = float(os.getenv('COUNT_CLICKS_PER_SECOND'))
    TYPE_BROWSER = os.getenv('TYPE_BROWSER')


config = Config() 