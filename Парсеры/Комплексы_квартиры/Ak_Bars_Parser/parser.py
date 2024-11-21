from bs4 import BeautifulSoup
import httpx
import json
import re
from prefect import flow
from datetime import date
from geopy.geocoders import Nominatim
import utils
from itertools import chain

PRICE_REGEX = re.compile(r"[\d\s]+")
STAGE_REGEX = re.compile("(IV|I{1,3}|VI{0,3}|[IVX]+)\D+(\d{4})")
ALL_FLATS_COUNTER = 0

@flow(log_prints=True)
def parse():
    parse_core_iterative()

def parse_core_iterative():
    """
    Основная функция парсинга с постепенной записью данных в JSON-файл.
    """
    content = {
        "systemName": "akbars-dom",
        "name": "Ак Барс Дом"
    }

    with open("akbars-dom.json", "w", encoding="utf-8") as file:
        file.write('{\n')
        file.write(f'"systemName": "{content["systemName"]}",\n')
        file.write(f'"name": "{content["name"]}",\n')
        file.write('"residentialComplexes": [\n')
        
        first = True
        for complex_data in parse_complexes():
            if not first:
                file.write(',\n')
            else:
                first = False
            json.dump(complex_data, file, indent=4, ensure_ascii=False)
        
        file.write('\n]\n}')

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
        if flats:
            yield format_project_output(project, flats)

    print(f"Flats: {ALL_FLATS_COUNTER}\nProjects are parsed")

def extract_project_data(project_soup, data_json):
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
        coords = parse_address(address_link, 'Россия', 'Казань')
        soup_data[complex_title.capitalize()] = {'img_url': image_link, 'coords': coords}

    return [
        {
            "name": complex_name,
            "slug": complex_info['CODE'],
            "link": fetch_links_not_in_list(complex_info["ID"]),
            "coords": soup_data[complex_name.capitalize()]['coords'],
            "img_url": soup_data[complex_name.capitalize()]['img_url']
        }
        for complex_name, complex_info in complexes_dict.items()
    ]

def format_project_output(project, flats):
    """
    Форматирование данных жилого комплекса для вывода.
    """
    lat, lon = project["coords"]
    return {
        'internalId': project["slug"],
        'name': project["name"],
        'geoLocation': {
            'latitude': lat,
            'longitude': lon
        },
        'renderImageUrl': project["img_url"],
        'presentationUrl': None,
        'flats': flats
    }

def parse_flats(slug, link):
    """
    Парсинг квартир для жилого комплекса.
    """
    print(f'parse flat from id: {slug}, url: {link}')
    if not link:
        return []

    page_number = 1
    flat_data_list = [] 

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

        flat_data_list.append([
            parse_flat_data(item.find("a")['href'], slug)
            for item in items if '/apartments/genplan-choose/' not in item.find("a")['href']
        ])

        page_number += 1

    all_flats = list(chain.from_iterable(flat_data_list))

    if all_flats:
        global ALL_FLATS_COUNTER
        ALL_FLATS_COUNTER += len(all_flats)
        print(f"Flats for {slug} parsed, count: {len(all_flats)}")

    return all_flats

def parse_flat_data(link_href, slug):
    """
    Парсинг данных о конкретной квартире.
    """
    try:
        response = httpx.get(f'https://akbars-dom.ru{link_href}', timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        content_block = soup.find(class_='Apartment_main__col__qi3ZL')

        if not content_block:
            print(f"The block with information about the apartment could not be found at the link: {link_href}")
            return None

        price = parse_price(content_block)
        count_rooms = parse_count_rooms(soup)
        features = extract_apartment_features(content_block.select_one('.Apartment_features__m1EjQ'))
        image_url = parse_image(soup)

        return {
            "residentialComplexInternalId": slug,
            "developerUrl": f"https://akbars-dom.ru{link_href}",
            "price": price,
            "floor": features.get('floor'),
            "area": features.get("area"),
            "rooms": count_rooms,
            "buildingDeadline": features.get("deadline"),
            "layoutImageUrl": image_url,
        }
    except httpx.RequestError as e:
        print(f"Error when requesting an apartment via the link {link_href}: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error when requesting an apartment via a link {link_href}: {e}")
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

def parse_flat_data(link_href, slug):
    """
    Парсинг данных квартиры.
    """
    try:
        response = httpx.get(f'https://akbars-dom.ru{link_href}', timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        content_block = soup.find(class_='Apartment_main__col__qi3ZL')

        if not content_block:
            print(f"The block with information about the apartment could not be found at the link: {link_href}")
            return None

        price = parse_price(content_block)
        count_rooms = parse_count_rooms(soup)
        features = extract_apartment_features(content_block.select_one('.Apartment_features__m1EjQ'))
        image_url = parse_image(soup)

        return {
            "residentialComplexInternalId": slug,
            "developerUrl": f"https://akbars-dom.ru{link_href}",
            "price": price,
            "floor": features.get('floor'),
            "area": features.get("area"),
            "rooms": count_rooms,
            "buildingDeadline": features.get("deadline"),
            "layoutImageUrl": image_url,
        }
    except httpx.RequestError as e:
        print(f"Error when requesting an apartment via the link {link_href}: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error when requesting an apartment via a link {link_href}: {e}")
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

def parse_address(project_link, country_name, town_name):
    """
    Парсинг адреса.
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
        return try_get_coords(country_name, town_name)

    address = address_content.get_text(strip=True)
    address = expand_abbreviations(address)

    result = get_coords(address) if address else try_get_coords(country_name, town_name)
    return result or try_get_coords(country_name, town_name)

def expand_abbreviations(address):
    """
    Расширение сокращений.
    """
    abbreviations = {
        'пр.': 'проспект',
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

def try_get_coords(country_name, town_name):
    """
    Попробовать получить координаты.
    """
    result = get_coords(f'{country_name} {town_name}')
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
            # print(f"Couldn't find the coordinates for the address: {address}")
            return None
    
    except Exception as e:
        print(f"Unknown error: {e}")
        return None

if __name__ == '__main__':
    parse_core_iterative()