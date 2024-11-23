from prefect import flow
from datetime import date

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import json
import re
import utils

ALL_FLATS_COUNTER = 0

@flow(log_prints=True)
def parse():
    """
    Главная функция парсинга, которая инициирует процесс парсинга жилых комплексов и квартир.
    """
    utils.upload(parse_core())

def parse_core():
    """
    Основная функция парсинга с постепенной записью данных в JSON-файл.
    Создает структуру JSON и записывает данные о жилых комплексах и квартирах в файл.
    """
    content = {
        "systemName": "tsi",
        "name": "Группа компаний «tsi»",
        "residentialComplexes": list(parse_complexes())
    }
    with open("suvarstroit.json", "w",  encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)
    return content

def parse_complexes():
    """
    Парсинг всех жилых комплексов.
    Получает данные о жилых комплексах и их квартирах с веб-сайта.
    Возвращает генератор, который выдает отформатированные данные о каждом жилом комплексе.
    """
    flats = list(parse_flats())
    
    complexes_response = requests.get("https://tsirt.ru/realty/")
    complexes_response.raise_for_status()
    
    soup = BeautifulSoup(complexes_response.content, "html.parser")
    list_card_content = soup.find("div", class_="rt__list")
    if not list_card_content:
        return None
    
    card_content = soup.find_all('div', class_='rt-card')

    if not card_content:
        return None

    for card in card_content:
        complex_href = parse_complex_href(card)
        if not complex_href:
            continue
        img_url = parse_complex_img(card)
        complex_img = f'https://tsirt.ru{img_url}'
        complex_title = parse_complex_title(card)
        loc = parse_address(card, 'Россия', "Республика Татарстан")
        slug = parse_slug(complex_href)
        presentation_link = f"https://tsirt.ru/{complex_href}"
        yield {
            'internalId': slug,
            'name': complex_title,
            'geoLocation': {
                'latitude': loc[0],
                'longitude': loc[1]
            },
            'renderImageUrl': complex_img,
            'presentationUrl': presentation_link,
            'flats': list(filter(lambda f: f['residentialComplexInternalId'].lower() == complex_title.lower(), flats))
        }
    print(f"Flats: {ALL_FLATS_COUNTER}\nProjects are parsed")

def parse_flats():
    """
    Парсинг квартир для жилого комплекса.
    Возвращает генератор, который последовательно выдает данные о квартирах.
    Если ссылка не указана, возвращает пустой список.
    """
    page = 1
    max_pages = requests.get(f"https://tsirt.ru/apartments/", timeout=30)
    max_pages.raise_for_status()
    max_pages = BeautifulSoup(max_pages.content, "html.parser")
    max_pages = int(max_pages.find_all("a", class_="pagination__item")[2].text)
    # print(max_pages)
    # page <= max_pages:
    while page != 2:
        counter = 0
        flats_response = requests.get(f"https://tsirt.ru/apartments/?page={page}", timeout=30)
        
        flats_response.raise_for_status()
        soup = BeautifulSoup(flats_response.content, "html.parser")
        flats = soup.find_all("a", class_="cells__image", target="_blank")
        # print(len(flats))
        if len(flats) == 0:
            break

        for flat_link in flats:
            flat_link = flat_link.get("href")
            flat_link = f"https://tsirt.ru{flat_link}"

            flat_code = requests.get(flat_link,timeout=30)
            flat_code.raise_for_status()
            flat_code = BeautifulSoup(flat_code.content, "html.parser")
            
            price = flat_code.find("span", class_="apart-reserve__price").text
            price = int(''.join(filter(str.isdigit, price)))
            
            floor = flat_code.find_all("span", class_="apart-reserve__text")[4].text
            floor = int(floor.split('/')[0])
            
            area = flat_code.find_all("span", class_="apart-reserve__text")[5].text
            area_part = area.split(' ')[0]
            area = float(area_part)
            
            rooms = flat_code.find_all("span", class_="apart-reserve__text")[3].text
            count_room = int(rooms)
            img = flat_code.find("img", class_="apart-slider__img").get("src")
            img = f"https://tsirt.ru{img}"
            counter += 1
            # print(flat_code.find_all("span", class_="apart-reserve__text")[0].text)
            yield {
                "residentialComplexInternalId": flat_code.find_all("span", class_="apart-reserve__text")[0].text,
                "developerUrl": flat_link,
                "price": price,
                "floor": floor,
                "area": area,
                "rooms": count_room,
                "buildingDeadline": evaluate_building_deadline(flat_code.find_all("span", class_="apart-reserve__text")[1].text),
                "layoutImageUrl": img,
            }
        page += 1

        if counter:
            global ALL_FLATS_COUNTER
            ALL_FLATS_COUNTER += counter
            print(f"Flats parsed from all complexes page: https://tsirt.ru/apartments/?page={page - 1}, count: {counter}")

def evaluate_building_deadline(date_value):
    """
    Определяет дату завершения строительства на основе входной строки.
    Функция принимает строку, содержащую информацию о сроках строительства, 
    и возвращает дату завершения в формате ISO. 
    """
    if date_value == "Дом сдан":
        return date.min.isoformat()
    pattern = r'([IVXLC]+)\s*квартал\s*(\d{4})'
    match = re.search(pattern, date_value)
    if match:
        quarter = match.group(1)
        year = match.group(2) 
        # print(f"Квартал: {quarter}, Год: {year}")
        building_deadline_date = utils.create_date_from_quarter(
            year=int(year),
            quarter=utils.transform_roman_to_arabic(quarter)
        )
        return building_deadline_date.isoformat()
    return None

def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении координат: {e}")
        return None

def parse_address(project_content, country_name, region):
    """
    Парсит адрес проекта из HTML-контента.
    Если адрес не найден, пытается получить координаты по названию страны и региона.
    Возвращает координаты или None, если адрес не найден.
    """
    address_content = project_content.find('div', class_='rt-card__location')

    # Если адрес не найден, пробуем получить координаты
    if not address_content:
        return try_get_coords(country_name, region)

    address = address_content.get_text(strip=True)
    address = expand_abbreviations(address)

    result = get_coords(address) if address else try_get_coords(country_name, region)
    return result or try_get_coords(country_name, region)

def expand_abbreviations(address):
    """
    Расширяет сокращения в адресе до полных форм.
    Заменяет известные сокращения на их полные значения.
    """
    abbreviations = {
        'г.': 'город ',
        'ул.': 'улица ',
        'пос.': 'поселение ',
        'д.': 'дом',
        'с.': 'село'
    }
    
    for abbr, full in abbreviations.items():
        address = address.replace(abbr, full)
        
    return address

def try_get_coords(country_name, region):
    """
    Пытается получить координаты по названию страны и региону.
    Если координаты не найдены, пытается получить их только по названию страны.
    """
    result = get_coords(f'{country_name} {region}')
    if result:
        return result
    return get_coords(f'{country_name}')

def get_coords(address):
    """
    Получает координаты для заданного адреса.
    Использует геокодер Nominatim для получения широты и долготы.
    Возвращает список с координатами или None, если координаты не найдены.
    """
    try:
        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(address, timeout=10)
        
        if getLoc:
            return [getLoc.latitude, getLoc.longitude]
        else:
            return None
    
    except Exception as e:
        print(f"Unknown error: {e}")
        return None

def parse_slug(href):
    """
    Извлекает часть URL, которая находится между двумя слешами.
    """
    if href:
        pattern = r'/[^/]+/([^/]+)/?'
        match = re.search(pattern, href)
        if match:
            return match.group(1)
    return None

def parse_complex_href(card):
    """
    Получает ссылку (href) на карточку из элемента с изображением.
    """
    complex_href = card.find('a', class_='rt-card__img')
    if complex_href:
        return complex_href.get('href')
    return None

def parse_complex_img(card):
    """
    Извлекает URL изображения из карточки.
    """
    complex_href = card.find('a', class_='rt-card__img')
    if complex_href:
        complex_url = complex_href.find('img', class_='rt-card__image')
        if complex_url:
            return complex_url.get('src') 
    return None

def parse_complex_title(card):
    """
    Получает заголовок карточки из элемента с классом 'rt-card__title'.
    """
    complex_title = card.find('a', class_='rt-card__title')
    if complex_title:
        return complex_title.get_text(strip=True)
    return None
    
if __name__ == '__main__':
    print(json.dumps(parse_core()))
