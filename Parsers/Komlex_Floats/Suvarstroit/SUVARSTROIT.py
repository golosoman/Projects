from datetime import datetime
from bs4 import BeautifulSoup
import httpx
import json
import re
from prefect import flow
from geopy.geocoders import Nominatim
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
        "systemName": "suvarstroit",
        "name": "Суварстроит, Республика Татарстан (Татарстан)",
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
    try:
        project_response = httpx.get("https://suvarstroit.ru/", timeout=30)
        id_project_response = httpx.get("https://suvarstroit.ru/search/flats", timeout=30)
    except httpx.RequestError as e:
        print(f"Error when requesting data about complexes: {e}")
        return []
    
    first_soup = BeautifulSoup(project_response.text, "lxml")
    second_soup = BeautifulSoup(id_project_response.text, "lxml")
    project_data = extract_project_data(first_soup.find_all('li', class_='our-projects__list-item'), second_soup.find('ul', class_='filters__form-select-list'))
    
    for project in project_data:
        lat, lon = project["coords"]
        flats = list(parse_flats(project["slug"], project["filter_link"]))
        if flats:
            yield {
                'internalId': project["slug"],
                'name': project['name'],
                'geoLocation': {
                    'latitude': lat,
                    'longitude': lon
                },
                'renderImageUrl': project["img_url"],
                'presentationUrl': project['link'],
                'flats': flats
            }

    print(f"Flats: {ALL_FLATS_COUNTER}\nProjects are parsed")

def parse_flats(slug, link):
    """
    Парсинг квартир для жилого комплекса.
    Возвращает генератор, который последовательно выдает данные о квартирах.
    Если ссылка не указана, возвращает пустой список.
    """
    print(f'parse flat from id: {slug}, url: {link}')
    if not link:
        return []
    
    counter = 0
    page_number = 1

    while True:
        url = f"{link}&page={page_number}"
        try:
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Error when requesting a page {page_number}: {e}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        items = soup.find_all('li', class_='catalog__list-item')
        
        if not items:
            print("There is no content on the page. Completing the crawl.")
            break

        for card_content in items:
            counter += 1
            link_href = parse_flat_link(card_content)
            price = parse_flat_price(card_content)
            count_rooms = parse_count_rooms(card_content)
            features = extract_apartment_features(card_content)
            image_url = parse_plan_image(card_content)
            yield {
                "residentialComplexInternalId": slug,
                "developerUrl": f"https://suvarstroit.ru{link_href}",
                "price": price,
                "floor": features.get('floor'),
                "area": features.get("area"),
                "rooms": count_rooms,
                "buildingDeadline": features.get("deadline"),
                "layoutImageUrl": image_url,
            }

        page_number += 1

    if counter:
        global ALL_FLATS_COUNTER
        ALL_FLATS_COUNTER += counter
        print(f"Flats for {slug} parsed, count: {counter}")

def extract_project_data(project_soup, id_project_soup):
    """
    Извлечение данных о жилых комплексах.
    Возвращает список словарей с информацией о каждом жилом комплексе, включая название, ссылку, координаты и изображение.
    """
    list_content = id_project_soup.find_all('li')
    result_dict = {}
    
    for item in list_content:
        # Проверка наличия input и span
        input_element = item.find('input', class_='filters__form-select-radio-input')
        span_element = item.find('span', class_='filters__form-select-radio-text')
        
        if input_element and span_element:
            input_value = input_element.get('value')
            title_text = span_element.get_text(strip=True).title()
            result_dict[title_text] = {'name': title_text, 'id': input_value}
        else:
            print("Элемент input или span не найден в элементе li.")

    project_data = []
    for project_item in project_soup:
        project_title = parse_title(project_item)
        project_img = parse_image(project_item)
        project_address = parse_address(project_item, 'Россия', 'Республика Татарстан')
        project_link = parse_link(project_item)
        project = {
            'name': project_title,
            'link': f'https://suvarstroit.ru{project_link}/',
            'slug': project_link.split('/')[1],
            'filter_link': generate_link(result_dict[project_title.title()]['id']),
            'coords': project_address,
            'img_url': f'https://suvarstroit.ru{project_img}'
        }
        project_data.append(project)
    
    return project_data

def extract_apartment_features(card_soup):
    """
    Извлечение характеристик квартиры.
    Возвращает словарь с площадью, сроком сдачи и этажом квартиры.
    """
    list_content = card_soup.find_all('li', class_='catalog__card-specs-list-item')
    content_area = card_soup.find('h3', 'catalog__card-title')
    return {
        'area': parse_area(content_area),
        'deadline': parse_date(list_content[3]),
        'floor': parse_floor(list_content[2])
    }

def parse_plan_image(card_soup):
    """
    Парсинг изображения плана квартиры.
    Если изображение не найдено, возвращает None.
    """
    # Находим div с уникальным классом
    img_elements = card_soup.find('img', class_='catalog__card-slider-card-image')
    image_url = img_elements.get('src') if img_elements else None
    return f"{image_url}" if image_url else None

def parse_date(soup_date):
    due_date_key = soup_date.find('div', class_='catalog__card-specs-card-value')
    
    if due_date_key:
        """
        Извлекает дату из HTML-контента и преобразует её в формат ISO.
        Если дата не найдена или не может быть преобразована, возвращает None.
        """
        # Находим родительский элемент и затем значение даты
        due_date_value = due_date_key.get_text(strip=True)
        # Преобразуем строку даты в объект datetime
        date_obj = datetime.strptime(due_date_value, '%d.%m.%Y %H:%M:%S')
        # Возвращаем дату в формате ISO
        return date_obj.isoformat()
    
    print("The date element was not found.")
    return None

def parse_area(square_element):
    """
    Парсинг площади квартиры.
    Если площадь не может быть извлечена, возвращает None.
    """
    # Извлекаем значение площади
    if square_element:
        match = re.search(r'(\d+)\s*м2', square_element.get_text(strip=True))
        return float(match.group(1)) if match else None
    else:
        print("The element was not found.")
    return None

def parse_floor(floor_element):
    """
    Парсинг этажа квартиры.
    Если этаж не может быть извлечен, возвращает None.
    """
    # Извлекаем номер этажа
    if floor_element:
        # Находим все <span> внутри элемента
        floor_content = floor_element.find('div', class_='catalog__card-specs-card-value')
        if floor_content:
            floor_number = floor_content.get_text(strip=True).split(' ')[0]
            if floor_number.isnumeric():
                return int(floor_number)
    else:
        print("The element was not found.")
    return None

def parse_count_rooms(card_soup):
    flat_content_element = card_soup.find('h3', 'catalog__card-title')
    """
    Парсит количество комнат из информации о квартире.
    Если информация о квартире не найдена, возвращает 0.
    Если количество комнат не может быть извлечено, возвращает None.
    """
    if flat_content_element is None:
        print("The item with information about the apartment was not found.")
        return None
    
    flat_text = flat_content_element.get_text(strip=True)
    
    # Извлекаем количество комнат
    # Предполагаем, что текст начинается с количества комнат
    room_count = flat_text.strip()[0]

    if room_count.isnumeric():
        return int(room_count)
    
    print("Information about the number of rooms could not be extracted.")
    return None

def parse_flat_link(card_soup):
    link_content = card_soup.find('a', class_='catalog__card-link-wrapper')
    """
    Извлекает ссылку на квартиру из HTML-контента.
    Если ссылка не найдена, возвращает None.
    """
    if link_content:
       return link_content.get('href')
    return None

def parse_flat_price(card_soup):
    price_element = card_soup.find('div', 'catalog__card-price-amount')
    """
    Парсит цену квартиры из HTML-контента.
    Если цена не может быть преобразована в число, возвращает None.
    """
    if price_element:
        price_string = price_element.get_text(strip=True)
        price_number = price_string.replace(" ", "").replace("₽", "").strip()
        if price_number.isnumeric():
            return int(price_number)
        else:
            print("The price could not be converted to a number.")
            return None
    
    print("Couldn't find the price.")
    return None

def generate_link(filter_id_project):
    """
    Генерирует URL для поиска квартир по заданному идентификатору проекта.
    Возвращает сформированный URL.
    """
    url = f'https://suvarstroit.ru/search/flats/read?project={filter_id_project}&costFrom=5%C2%A0500%C2%A0000&costTo=30%C2%A0000%C2%A0000&areaFrom=0&areaTo=150'
    return url

def parse_address(project_content, country_name, region):
    """
    Парсит адрес проекта из HTML-контента.
    Если адрес не найден, пытается получить координаты по названию страны и региона.
    Возвращает координаты или None, если адрес не найден.
    """
    address_content = project_content.find('div', class_='our-projects__card-location')

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
        'ул.': 'улица',
        'д.': 'дом',
        'г.': 'город',
        'р-н': 'район',
        'с.': 'село',
        'пр.': 'проспект',
        'пр-т': 'проспект',
        'пл.': 'площадь',
        'б-р': 'бульвар',
        'ш.': 'шоссе',
        'кв.': 'квартира',
        'пер.': 'переулок',
        'р-он.': 'район'
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
    
def parse_image(project_content):
    """
    Извлекает URL изображения проекта из HTML-контента.
    Возвращает URL изображения или None, если изображение не найдено.
    """
    image_content = project_content.find('img', class_='our-projects__card-slide-image')
    return image_content.get('src') if image_content else None

def parse_link(project_content):
    """
    Извлекает ссылку на проект из HTML-контента.
    Возвращает ссылку или None, если ссылка не найдена.
    """
    link_content = project_content.find('a', class_='our-projects__card')
    return link_content.get('href') if link_content else None

def parse_title(project_content):
    """
    Извлекает название проекта из HTML-контента.
    Возвращает название или None, если название не найдено.
    """
    title_content = project_content.find('h3', class_='our-projects__card-title')
    return title_content.get_text(strip=True) if title_content else None


if __name__ == '__main__':
    print(json.dumps(parse_core()))