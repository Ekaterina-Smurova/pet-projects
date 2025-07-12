!pip install geopy
from geopy.geocoders import Nominatim

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Ссылка на страницу Википедии со списком городов РФ
URL = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8"
# Загружаем страницу
req = requests.get(URL)

soup = BeautifulSoup(req.text, 'html.parser')

# Извлекаем таблицу
table = soup.find('table', class_=['standard', 'sortable', 'jquery-tablesorter'])

cities = []

# Обработка таблицы
for row in table.find_all('tr'):
    cols = row.find_all('td')
    if cols:
        city = cols[2].get_text(strip=True).split('[')[0]
        cities.append(city)

# Сохраняем результат
df = pd.DataFrame(cities, columns=['city'])


geolocator = Nominatim(user_agent="geo_cities_app")

# Функция возвращающая координаты
def get_coordinates(city):
    location = geolocator.geocode(f"{city}, Россия", timeout=10)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


# Добавляем координаты
latitudes = []
longitudes = []

for city in df['city']:
    lat, lon = get_coordinates(city)
    latitudes.append(lat)
    longitudes.append(lon)
    time.sleep(1)  # пауза, чтобы не попасть под блокировку API

# Добавляем в датафрейм
df['latitude'] =latitudes
df['longitude'] = longitudes

# Сохраняем в csv файл
df.to_csv('coordinates_cities.csv', index=False, encoding='utf-8-sig')
