!pip install openmeteo-requests
!pip install requests-cache retry-requests numpy pandas
from retry_requests import retry
import openmeteo_requests
import requests_cache

# Настраиваем клиент OpenMeteo API с кэшем и повторяем попытку при ошибке
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


url = "https://archive-api.open-meteo.com/v1/archive"

# функция извлечения нужных погодных данных
def load(cityname:str, year:int, lat:float, lon:float):
	params = {
		"latitude": lat,
		"longitude": lon,
		"start_date": f'{year}-01-01',
		"end_date": '2025-05-31' if year == 2025  else f'{year}-12-31',
		"hourly": ["temperature_2m", "snow_depth", "snowfall", "rain", "precipitation", "relative_humidity_2m", "wind_speed_100m", "wind_direction_100m", "is_day"],
		"temporal_resolution": "hourly_6"
	}
	responses = openmeteo.weather_api(url, params=params)

	#  Так как мы передаем координаты по одному, то обрабатываем только первый ответ
	response = responses[0]

	# Обрабатываем почасовые данные (код можно взять с сайта open-meteo)
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_snow_depth = hourly.Variables(1).ValuesAsNumpy()
	hourly_snowfall = hourly.Variables(2).ValuesAsNumpy()
	hourly_rain = hourly.Variables(3).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(5).ValuesAsNumpy()
	hourly_wind_speed_100m = hourly.Variables(6).ValuesAsNumpy()
	hourly_wind_direction_100m = hourly.Variables(7).ValuesAsNumpy()
	hourly_is_day = hourly.Variables(8).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
				start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
				end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
				freq = pd.Timedelta(seconds = hourly.Interval()),
				inclusive = "left"
			)}


	# Собираем все в датасет
	hourly_data['city'] = city
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["rain"] = hourly_rain
	hourly_data["snowfall"] = hourly_snowfall
	hourly_data["snow_depth"] = hourly_snow_depth
	hourly_data["is_day"] = hourly_is_day
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["wind_direction_100m"] = hourly_wind_direction_100m
	hourly_data["wind_speed_100m"] = hourly_wind_speed_100m

	hourly_dataframe = pd.DataFrame(data = hourly_data)

	return hourly_dataframe

iter_cnt = 0
iter_lim = 10 # задаем количество выгрузок данных за один запуск

for index, row in df.iterrows():
	city, lat, lon = row['city'], row['latitude'], row['longitude']
	for year in range(1975, 2026):
		filename = f'{city}_{year}.csv'
		exists = True
		try:
			frame = pd.read_csv(filename)
		except:
			exists = False
		if not exists or frame.shape[1]==0:
			iter_cnt = iter_cnt+1
			if iter_cnt>iter_lim:
				break
			frame = load(city, year, lat, lon)
			frame['city'] = city
			frame.to_csv(filename, index=False)
		elif 'city' not in frame.columns:
			frame['city'] = city
			frame.to_csv(filename, index=False)
