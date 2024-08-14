from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Настройка headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Опционально: для более стабильной работы

# Загрузка страницы
driver = webdriver.Chrome(options=options)
driver.get('https://httpwg.org/specs/')

# Получение HTML-кода страницы
html = driver.page_source

# Парсинг DOM-дерева с помощью Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Вывод информации о DOM-дереве
print(soup.prettify())

# Закрытие браузера
driver.quit()
