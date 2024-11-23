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
    Запускает основной процесс парсинга данных.
    Вызывает функцию для выполнения парсинга с постепенной записью данных в JSON-файл.
    """
    utils.upload(parse_core())

def parse_core():
    """
    Основная функция парсинга, которая записывает данные о жилых комплексах в JSON-файл.
    Создает файл, записывает в него информацию о системе и жилых комплексах.
    """
    content = {
        "systemName": "dsk-vrn",
        "name": "ДСК Воронеж",
        "residentialComplexes": list(parse_complexes())
    }

    with open("dsk-vrn.json", "w",  encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)
    return content

def parse_complexes():
    """
    Извлекает данные о всех жилых комплексах с веб-страницы.
    Возвращает генератор, который выдает форматированные данные о каждом комплексе.
    """
    try:
        response = httpx.get("https://dsk.vrn.ru/proekty/", timeout=30)
        response_api = httpx.get("https://dsk.vrn.ru/podobrat-kvartiru/?ajax=y", timeout=30)
    except httpx.RequestError as e:
        print(f"Error when requesting data about complexes: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "lxml")
    project_data = extract_project_data(soup.select('.projects-item'), convert_to_object(response_api))
    
    for project in project_data:
        flats = list(parse_flats(project["slug"], project["filter_link"]))
        lat, lon = project["coords"]
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
    Извлекает информацию о квартирах для указанного жилого комплекса.
    Возвращает генератор, который выдает данные о каждой квартире.
    Если ссылка недоступна или произошла ошибка, возвращает пустой список.
    """
    print(f'parse flat from id: {slug}, url: {link}')
    if not link:
        return []
    
    counter = 0
    page_number = 1

    while True:
        url = f"{link}&PAGEN_1={page_number}"
        try:
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Error when requesting a page {page_number}: {e}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        items = soup.find_all('a', class_='flats-item__layout')
        
        if not items:
            print("There is no content on the page. Completing the crawl.")
            break
        

        for link_content in items:
            counter += 1
            link_href = link_content.get('href')
            response = httpx.get(f'https://dsk.vrn.ru{link_href}', timeout=30)
            new_soup = BeautifulSoup(response.text, "lxml")
            content_block = new_soup.find(class_='flat_detail_desc_wr')

            if content_block:
                price = parse_price(content_block)
                count_rooms = parse_count_rooms(content_block)
                features = extract_apartment_features(content_block)
                image_url = parse_plan_image(new_soup)

                yield {
                    "residentialComplexInternalId": slug,
                    "developerUrl": f"https://dsk.vrn.ru{link_href}",
                    "price": price,
                    "floor": features.get('floor'),
                    "area": features.get("area"),
                    "rooms": count_rooms,
                    "buildingDeadline": features.get("deadline"),
                    "layoutImageUrl": image_url,
                }
                
            else:
                print(f"The block with information about the apartment could not be found at the link: {link_href}")

        # Проверяем наличие элемента "Следующая"
        next_page = soup.find('li', class_='page-item-next')
        
        if next_page is None:
            print("End of the page")
            break

        page_number += 1

    if counter:
        global ALL_FLATS_COUNTER
        ALL_FLATS_COUNTER += counter
        print(f"Flats for {slug} parsed, count: {counter}")

def extract_project_data(project_soup, data_json):
    """
    Извлекает данные о жилых комплексах из HTML-контента и JSON-данных.
    Возвращает список словарей с информацией о каждом жилом комплексе.
    """
    items = data_json['ITEMS']['30']['VALUES']
    result_dict = {}

    # Формируем словарь с данными о комплексах
    for key, value in items.items():
        result_dict[value['VALUE'].strip()] = {
            'id': value['HTML_VALUE_ALT'],
            'name': value['VALUE'].strip()
        }

    # Обновляем ключи и значения для удобства
    updated_result_dict = {}
    for key, value in result_dict.items():
        new_key = key.replace('&quot;', '«', 1).replace('&quot;', '»', 1).lower()  # Заменяем первое вхождение
        new_value = {
            'id': value['id'],
            'name': new_key
        }
        updated_result_dict[new_key] = new_value

    result_dict = updated_result_dict
    project_data = []

    # Извлекаем данные о каждом жилом комплексе
    for project_item in project_soup:
        project = {}
        project['img_url'] = f'https://dsk.vrn.ru{parse_image(project_item)}'
        project['link'] = f'https://dsk.vrn.ru{parse_link(project_item)}'
        project['slug'] = project['link'].split('/')[4]
        project['name'] = parse_title(project_item)
        try:
            project['filter_link'] = generate_link(result_dict[project['name'].lower()]['id'])
        except KeyError:
            project['filter_link'] = None
        project['coords'] = parse_address(project_item, 'Россия', 'Воронежская область')
        project_data.append(project)
    
    return project_data

def generate_link(filter_id_project):
    """
    Генерирует URL для поиска квартир по заданному фильтру.
    Возвращает строку с полным URL для запроса.
    """
    url = f'https://dsk.vrn.ru/podobrat-kvartiru/?filter_30={filter_id_project}&filter_24_MIN=2475375&filter_24_MAX=16368060&filter_22_MIN=1&filter_22_MAX=24&set_filter=Показать'
    return url

def parse_plan_image(soup):
    """
    Извлекает URL изображения плана квартиры из HTML-контента.
    Если изображение найдено, возвращает его URL. В противном случае возвращает None.
    """
    # Находим div с уникальным классом
    flat_detail_plan = soup.find('div', class_='flat_detail_plan')
    # Находим все элементы <img> внутри этого div
    img_elements = flat_detail_plan.find('img') if flat_detail_plan else None
    image_url = img_elements.get('src') if img_elements else None

    return f"https://dsk.vrn.ru{image_url}" if image_url else None

def extract_apartment_features(soup):
    """
    Извлекает характеристики квартиры из HTML-контента.
    Возвращает словарь с площадью, номером этажа и сроком сдачи квартиры.
    """
    square_elements = soup.find_all('div', class_='flat_detail_desc_square')

    return {
        'area': parse_area(square_elements[0]),
        'deadline': None,
        'floor': parse_floor(square_elements[2])
    }

def parse_area(square_element):
    """
    Извлекает площадь квартиры из HTML-элемента.
    Если площадь найдена и может быть преобразована в число, возвращает ее как число с плавающей точкой.
    В противном случае возвращает None.
    """
    # Извлекаем значение площади
    if square_element:
        # Находим все <span> внутри элемента
        spans = square_element.find_all('span')
        if len(spans) > 1:
            area_value = spans[1].get_text(strip=True).split(' ')[0]
            if re.match(r'^-?\d+(?:\.\d+)?$', area_value) is not None:
                return float(area_value)
        else:
            print("There are not enough <span> elements.")
    else:
        print("The element was not found.")
    return None

def parse_floor(floor_element):
    """
    Извлекает номер этажа квартиры из HTML-элемента.
    Если этаж найден и является числом, возвращает его как целое число.
    В противном случае возвращает None.
    """
    # Извлекаем номер этажа
    if floor_element:
        # Находим все <span> внутри элемента
        spans = floor_element.find_all('span')
        if len(spans) > 1:
            floor_number = spans[1].get_text(strip=True)
            if floor_number.isnumeric():
                return int(floor_number)
        else:
            print("There are not enough <span> elements.")
    else:
        print("The element was not found.")
    return None

def parse_count_rooms(soup):
    """
    Извлекает количество комнат квартиры из HTML-контента.
    Если количество комнат найдено и является числом, возвращает его как целое число.
    В противном случае возвращает None.
    """
    flat_content_element = soup.select_one('.falt_detail_rooms')
    if flat_content_element is None:
        print("The item with information about the apartment was not found.")
        return None
    
    flat_text = flat_content_element.get_text(strip=True)
    
    # Извлекаем количество комнат
    # Предполагаем, что текст начинается с количества комнат
    room_count = flat_text.split('-')[0].strip()

    if room_count.isnumeric():
        return int(room_count)
    print("Information about the number of rooms could not be extracted.")
    return None

def parse_price(soup):
    """
    Парсит цену квартиры из HTML-контента.
    Если цена найдена и может быть преобразована в число, возвращает ее как целое число.
    В противном случае возвращает None.
    """
    price_element = soup.select_one('.flat_detail_desc_price_val')
    if price_element:
        price_string = price_element.get_text(strip=True)
        price_number = price_string.replace(" ", "").replace("р", "").strip()
        if price_number.isnumeric():
            return int(price_number)
        else:
            print("The price could not be converted to a number.")
            return None
    print("Couldn't find the price.")
    return None

def convert_to_object(invalid_json):
    """
    Преобразует строку с некорректным JSON в корректный объект JSON.
    Заменяет одинарные кавычки на двойные и загружает данные.
    """
    valid_json = invalid_json.text.replace("\'", "\"")
    result = json.loads(valid_json)
    return result

def parse_address(project_content, country_name, region):
    """
    Извлекает адрес проекта из HTML-контента.
    Если адрес не найден, пытается получить координаты по названию страны и региона.
    """
    address_content = project_content.select_one('.projects-item__address')

    # Если адрес не найден, пробуем получить координаты
    if not address_content:
        return try_get_coords(country_name, region)

    address = address_content.get_text(strip=True)
    address = expand_abbreviations(address)

    result = get_coords(address) if address else try_get_coords(country_name, region)
    return result or try_get_coords(country_name, region)

def expand_abbreviations(address):
    """
    Заменяет сокращения в адресе на полные формы.
    Например, 'ул.' заменяется на 'улица'.
    """
    abbreviations = {
        'пр.': 'проспект',
        'пр-т': 'проспект',
        'ул.': 'улица',
        'пл.': 'площадь',
        'б-р': 'бульвар',
        'ш.': 'шоссе',
        'кв.': 'квартира',
        'д.': 'дом',
        'пер.': 'переулок',
        'с.': 'село',
        'р-он.': 'Район'
    }
    
    for abbr, full in abbreviations.items():
        address = address.replace(abbr, full)
        
    return address

def try_get_coords(country_name, region):
    """
    Получает координаты для страны и региона.
    Если регион не найден, возвращает координаты только для страны.
    """
    result = get_coords(f'{country_name} {region}')
    if result:
        return result
    return get_coords(f'{country_name}')

def get_coords(address):
    """
    Получает координаты (широту и долготу) для заданного адреса.
    Возвращает None, если адрес не найден.
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
    """
    span_image_content = project_content.select_one('.projects-item__image')
    image_content = span_image_content.select_one('img')
    return image_content.get('src')


def parse_link(project_content):
    """
    Извлекает ссылку на проект из HTML-контента.
    """
    link_content = project_content.select_one('a')
    return link_content.get('href')


def parse_title(project_content):
    """
    Извлекает название проекта из HTML-контента.
    """
    title_content = project_content.select_one('.projects-item__rc')
    return title_content.get_text(strip=True)

if __name__ == '__main__':
    print(json.dumps(parse_core()))