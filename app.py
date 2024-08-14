from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from dotenv import load_dotenv
import re

# Функция для преобразования номера
def format_phone_number(phone_number):
    if phone_number.startswith("8"):
        phone_number = " ".join([phone_number[1:4], phone_number[4:7], phone_number[7:9], phone_number[9:12]])
    return phone_number

def format_account_number(account_number):
    """Форматирует номер счета в формат xxxx xxxx xxxx xxxx."""
    account_number = account_number.replace(' ', '').replace('-', '')
    return ' '.join([account_number[i:i+4] for i in range(0, len(account_number), 4)])

def open_register_page(driver):
    """Открывает страницу регистрации."""
    driver.get(os.getenv('REGISTER_PATH'))

def click_restore_button(driver):
    """Нажимает на кнопку "У меня нет логина или пароля"."""
    wait = WebDriverWait(driver, 10)
    restore_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/div/div/form/button[2]")))
    restore_button.click()

def input_phone_number(driver):
    """Вводит номер телефона."""
    wait = WebDriverWait(driver, 10)
    phone_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div/div[2]/div[2]/input")))
    # phone_number = input("Введите номер телефона: ")
    phone_number = format_phone_number(os.getenv('TELEPHONE_NUMBER'))

    # Проверка формата номера телефона
    pattern = r"^\+7 \d{3} \d{3} \d{2} \d{2}$"
    if re.match(pattern, phone_number):
        print("Номер телефона введен в правильном формате!")
    else:
        print("Номер телефона введен в неправильном формате. Проверьте введенные данные.")

    # Ввод номера телефона
    actions = ActionChains(driver)
    actions.click(phone_input).send_keys(phone_number).perform()
    # Проверьте, является ли кнопка enabled
    
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/button")))

    # Получите номер счета из input поля
    account_number = phone_input.get_attribute('value')

    # Выведите полученный номер телефона
    print("Номер телефона:", account_number)

    is_enabled = continue_button.is_enabled()
    # Выведите результат проверки
    if is_enabled:
        print("Кнопка enabled.")
        continue_button.click()
    else:
        print("Кнопка disabled.")

    account_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div/div/div[2]/input")))
    body = driver.find_element(By.XPATH, "//body")
    body_text = body.text
    print(body_text)
    print(continue_button.is_enabled())
    


def click_continue_button(driver):
    """Нажимает на кнопку "Продолжить"."""
    wait = WebDriverWait(driver, 10)
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/button")))
    continue_button.click()

def input_account_number(driver):
    """Вводит номер счета."""
    wait = WebDriverWait(driver, 10)

    account_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div/div/div[2]/input")))
    body = driver.find_element(By.XPATH, "//body")
    body_text = body.text
    print(body_text)
    # account_number = input("Введите номер счета: ")
    account_number = format_account_number(os.getenv('ACCAUNT_NUMBER'))

    # Проверка формата номера счета
    pattern = r"^\d{4} \d{4} \d{4} \d{4}$"
    print(account_number)
    if re.match(pattern, account_number):
        print("Номер счета введен в правильном формате!")
    else:
        print("Номер счета введен в неправильном формате. Проверьте введенные данные.")

    # Сфокусируйтесь на поле ввода и введите номер счета
    actions = ActionChains(driver)
    actions.click(account_input).send_keys(account_number).perform()

    # Получите номер счета из input поля
    account_number = account_input.get_attribute('value')

    # Выведите полученный номер счета
    print("Номер счета:", account_number)

    # continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/div/div/form/div[3]/button")))
    # continue_button.click()


# Настройка headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Создание экземпляра WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Открытие URL страницы
open_register_page(driver)
click_restore_button(driver)
input_phone_number(driver)
# input_account_number(driver)
