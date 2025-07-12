# Исторические погодные метрики городов РФ с 1976г по 2024г.
Парсинг:  
[ipynb](https://github.com/Ekaterina-Smurova/pet-projects/blob/main/meteo/cities.ipynb)  
[nbviewer](https://nbviewer.org/github/Ekaterina-Smurova/pet-projects/blob/main/meteo/cities.ipynb)  

Обработка и агрегирование:  
[ipynb](https://github.com/Ekaterina-Smurova/pet-projects/blob/main/meteo/weather_cities.ipynb)  
[nbviewer](https://nbviewer.org/github/Ekaterina-Smurova/pet-projects/blob/main/meteo/weather_cities.ipynb)
## Реализация:  
- парсинг городов с сайта [wikipedia](https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8) (python) в csv; добавление геоданных [скрипт](https://github.com/Ekaterina-Smurova/pet-projects/blob/main/meteo/city_csv.py)

- парсинг погоды API [open-meteo](https://archive-api.open-meteo.com/v1/archive) архив (python) в csv [скрипт](https://github.com/Ekaterina-Smurova/pet-projects/blob/main/meteo/download_weather_archive.py)

- обработка скаченных данных (pandas) 

- загрузка в SQLITE, и выгрузка агрегированных данных (python, sql) 

- построение дашборда в [DataLens](https://datalens.yandex/8vdawcfrz9rat) 
