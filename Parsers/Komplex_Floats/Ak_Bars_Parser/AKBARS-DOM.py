from bs4 import BeautifulSoup
import httpx
import json
import re
from prefect import flow
from datetime import date
from geopy.geocoders import Nominatim
import utils

STAGE_REGEX = re.compile("(IV|I{1,3}|VI{0,3}|[IVX]+)\D+(\d{4})")
ALL_FLATS_COUNTER = 0

@flow(log_prints=True)
def parse():
    utils.upload(parse_core())
 
def parse_core():
    """
    Основная функция парсинга с постепенной записью данных в JSON-файл.
    """
    content = {
        "systemName": "akbars-dom",
        "name": "Ак Барс Дом",
        "residentialComplexes": list(parse_complexes())
    }
    with open("akbars-dom.json", "w",  encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)
    return content

def parse_complexes():
    """
    Парсинг всех жилых комплексов.
    """
    try:
        response = httpx.get("https://akbars-dom.ru/realty/", timeout=30)
        response_api = httpx.post("https://akbars-dom.ru/objects_api/apartments/filter_data/", timeout=30)
    except httpx.RequestError as e:
        print(f"Error when requesting data about complexes: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "lxml")
    project_data = extract_project_data(soup.select(".complexes__item"), response_api.json())

    for project in project_data:
        flats = list(parse_flats(project["slug"], project["link"]))
        lat, lon = project["coords"]
        if flats:
            yield {
                'internalId': project["slug"],
                'name': project["name"],
                'geoLocation': {
                    'latitude': lat,
                    'longitude': lon
                },
                'renderImageUrl': project["img_url"],
                'presentationUrl': project["project_link"],
                'flats': flats
            }

    print(f"Flats: {ALL_FLATS_COUNTER}\nProjects are parsed")

def parse_flats(slug: str, link: str):
    """
    Парсинг квартир для жилого комплекса.
    """
    print(f'parse flat from id: {slug}, url: {link}')
    if not link:
        return []

    page_number = 1
    counter = 0

    while True:
        url = f"{link}?page={page_number}"
        try:
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Error when requesting a page {page_number}: {e}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        items = soup.find_all(True, {'class': ['RealtyList_list__item__fxDRN', 'RealtyList_list__item--table__LZoww']})

        if not items:
            print("There is no content on the page. Completing the crawl.")
            break

        for item in items:
            link_href = item.find("a")['href']
            if '/apartments/genplan-choose/' not in link_href:  # Исключаем нежелательные ссылки
                counter += 1
                response = httpx.get(f'https://akbars-dom.ru{link_href}', timeout=30)
                new_soup = BeautifulSoup(response.text, "lxml")
                content_block = new_soup.find(class_='Apartment_main__col__qi3ZL')

                if content_block:
                    price = parse_price(content_block)
                    count_rooms = parse_count_rooms(new_soup)
                    features = extract_apartment_features(content_block.select_one('.Apartment_features__m1EjQ'))
                    image_url = parse_image(new_soup)
                    yield {
                        "residentialComplexInternalId": slug,
                        "developerUrl": f"https://akbars-dom.ru{link_href}",
                        "price": price,
                        "floor": features.get('floor'),
                        "area": features.get("area"),
                        "rooms": count_rooms,
                        "buildingDeadline": features.get("deadline"),
                        "layoutImageUrl": image_url,
                    }
                else:
                    print(f"The block with information about the apartment could not be found at the link: {link_href}")

        page_number += 1

    if counter:
        global ALL_FLATS_COUNTER
        ALL_FLATS_COUNTER += counter
        print(f"Flats for {slug} parsed, count: {counter}")

def extract_project_data(project_soup: BeautifulSoup, data_json: dict):
    """
    Извлечение данных о жилых комплексах.
    """
    complexes_dict = {complex_info["NAME"]: complex_info for complex_info in data_json["COMPLEXES"].values()}
    soup_data = {}
    
    for complex in project_soup:
        complex_title = complex.select_one(".complexes--title").get_text(strip=True)
        image_link = extract_image_url(complex)
        complex_href = complex.get("href")
        address_link = complex_href if "http" in complex_href else f"https://akbars-dom.ru{complex_href}"
        coords = parse_address(address_link, 'Россия', 'Республика татарстан')
        soup_data[complex_title.capitalize()] = {'img_url': image_link, 'coords': coords}

    return [
        {
            "name": complex_name,
            "slug": complex_info['CODE'],
            "link": fetch_links_not_in_list(complex_info["ID"]),
            "project_link": address_link,
            "coords": soup_data[complex_name.capitalize()]['coords'],
            "img_url": soup_data[complex_name.capitalize()]['img_url']
        }
        for complex_name, complex_info in complexes_dict.items()
    ]

def parse_price(soup):
    """
    Парсинг цены квартиры.
    """
    price_element = soup.select_one('.Apartment_price__k-uEr')
    if price_element:
        price_string = price_element.get_text(strip=True)
        price_number = price_string.replace(" ", "").replace("руб.", "").strip()
        try:
            return int(price_number)
        except ValueError:
            print("The price could not be converted to a number.")
            return None
    print("Couldn't find the price.")
    return None

def extract_apartment_features(soup):
    """
    Извлечение характеристик квартиры.
    """
    return {
        'area': parse_area(soup),
        'deadline': evaluate_building_deadline(soup),
        'floor': parse_floor(soup)
    }

def evaluate_building_deadline(soup):
    """
    Оценка срока сдачи дома.
    """
    deadline_label = soup.find('div', string='Срок сдачи:')
    quarter_div = deadline_label.find_next_sibling('div') if deadline_label else None
    quarter_info = quarter_div.get_text(strip=True) if quarter_div else None
    if quarter_info == "Дом сдан":
        return date.min.isoformat()
    if quarter_info:
        parsed_stage = STAGE_REGEX.search(quarter_info)
        if parsed_stage:
            year = int(parsed_stage.group(2))
            quarter = utils.transform_roman_to_arabic(parsed_stage.group(1))
            building_deadline_date = utils.create_date_from_quarter(year=year, quarter=quarter)
            return building_deadline_date.isoformat()
    print("The deadline for the completion of the building could not be determined.")
    return None

def parse_area(soup):
    """
    Парсинг площади квартиры.
    """
    area_div = soup.find('div', string='Площадь:')
    if area_div:
        area_value = area_div.find_next_sibling('div')
        if area_value:
            return float(area_value.get_text(strip=True).split(' ')[0])
    print("The area could not be found.")
    return None

def parse_floor(soup):
    """
    Парсинг этажа квартиры.
    """
    floor_div = soup.find('div', string='Этаж:')
    if floor_div:
        floor_value = floor_div.find_next_sibling('div')
        if floor_value:
            return int(floor_value.get_text(strip=True).split('/')[0])
    print("Couldn't find the floor.")
    return None

def parse_price(soup):
    """
    Парсинг цены квартиры.
    """
    price_element = soup.select_one('.Apartment_price__k-uEr')
    if price_element:
        price_string = price_element.get_text(strip=True)
        price_number = price_string.replace(" ", "").replace("руб.", "").strip()
        try:
            return int(price_number)
        except ValueError:
            print("The price could not be converted to a number.")
            return None
    print("Couldn't find the price.")
    return None


def evaluate_building_deadline(soup):
    """
    Получение даты сдачи квартиры
    """
    deadline_label = soup.find('div', string='Срок сдачи:')
    quarter_div = deadline_label.find_next_sibling('div') if deadline_label else None
    quarter_info = quarter_div.get_text(strip=True) if quarter_div else None
    if quarter_info == "Дом сдан":
        return date.min.isoformat()
    if quarter_info:
        parsed_stage = STAGE_REGEX.search(quarter_info)
        if parsed_stage:
            year = int(parsed_stage.group(2))
            quarter = utils.transform_roman_to_arabic(parsed_stage.group(1))
            building_deadline_date = utils.create_date_from_quarter(year=year, quarter=quarter)
            return building_deadline_date.isoformat()
    print("The deadline for the completion of the building could not be determined.")
    return None

def parse_image(soup):
    """
    Парсинг изображения плана.
    """
    content_div = soup.find(class_='RealtySlider_slider__carousel__CfFJ3')
    img_tag = content_div.select_one('img') if content_div else None
    image_url = img_tag.get('src') if img_tag else None
    return f"https://akbars-dom.ru{image_url}" if image_url else None

def parse_count_rooms(soup):
    """
    Парсинг количества комнат.
    """
    flat_content_element = soup.select_one('.Title_title__AflvS')
    if flat_content_element is None:
        print("The item with information about the apartment was not found.")
        return 0
    
    flat_content = flat_content_element.get_text(strip=True)
    match = re.search(r'(\d+)-комн\.\s+(\w+)\s+(\d+\.\d+)\s+м²', flat_content)
    if match:
        room_number = match.group(1)  # Цифра
        apartment_type = match.group(2)  # Слово 
        # Проверка на пустую строку
        if not apartment_type:
            return 0
        # Обработка типов квартир
        if apartment_type in ("Студия", "Апартаменты", "Пентхаус"):
            return 0
        return int(room_number)
    print("Information about the number of rooms could not be extracted.")
    return None

def extract_apartment_features(soup):
    """
    Извлечение аргументов комнаты.
    """
    return {
        'area': parse_area(soup),
        'deadline': evaluate_building_deadline(soup),
        'floor': parse_floor(soup)
    }

def parse_area(soup):
    """
    Парсинг площади квартиры.
    """
    area_div = soup.find('div', string='Площадь:')
    if area_div:
        area_value = area_div.find_next_sibling('div')
        if area_value:
            return float(area_value.get_text(strip=True).split(' ')[0])
    print("The area could not be found.")
    return None

def parse_floor(soup):
    """
    Парсинг этажа квартиры.
    """
    floor_div = soup.find('div', string='Этаж:')
    if floor_div:
        floor_value = floor_div.find_next_sibling('div')
        if floor_value:
            return int(floor_value.get_text(strip=True).split('/')[0])
    print("Couldn't find the floor.")
    return None

def fetch_links_not_in_list(complex_id):
    """
    Извлечь ссылки, которых нет в списке.
    """
    url = "https://akbars-dom.ru/objects_api/apartments/filter_data/"
    form_data = {'complex[]': complex_id}

    try:
        with httpx.Client() as client:
            response = client.post(url, data=form_data, timeout=30)
        response.raise_for_status()
        data = response.json()
        return f'https://akbars-dom.ru{data.get("SMART_FILTER", {}).get("URL")}'

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}, {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"JSON decoding error: {e}")

    return None
    
def extract_image_url(project):
    """
    Извлечь изображение комплекса.
    """
    style = project.select_one('.complexes__left').get('style')
    match = re.search(r'url\((.*?)\)', style)
    return "https://akbars-dom.ru" + match.group(1).strip(" '\"") if match else None

def parse_address(project_link, country_name, region):
    """
    Извлекает адрес проекта из HTML-контента.
    Если адрес не найден, пытается получить координаты по названию страны и региона.
    """
    try:
        response = httpx.get(project_link, timeout=30)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        return None

    soup = BeautifulSoup(response.content, "lxml")
    address_content = soup.select_one(".mainTitle--address")
    
    # Если адрес не найден, пробуем получить координаты
    if not address_content:
        return try_get_coords(country_name, region)

    address = address_content.get_text(strip=True)
    address = expand_abbreviations(address)

    result = get_coords(address) if address else try_get_coords(country_name, region)
    return result or try_get_coords(country_name, region)

def expand_abbreviations(address):
    """
    Расширение сокращений.
    """
    abbreviations = {
        'пр.': 'проспект',
        'ул.': 'улица',
        'д.': 'дом',
        'с.': 'село',
        'р-н.': 'район',
        'р-он': 'район'
    }
    
    for abbr, full in abbreviations.items():
        address = address.replace(abbr, full)
        
    return address

def try_get_coords(country_name, region):
    """
    Попробовать получить координаты.
    """
    result = get_coords(f'{country_name} {region}')
    if result:
        return result
    return get_coords(f'{country_name}')

def get_coords(address):
    """
    Получить координаты.
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

if __name__ == '__main__':
    print(json.dumps(parse_core()))