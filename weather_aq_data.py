import json
import os
import requests
import zoneinfo
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

_IP_API = 'https://api.ipify.org'
_GEODATA_API = 'https://ipapi.co'
_WEATHER_API = 'https://api.openweathermap.org/data/2.5'
_WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def _get_weather_data(geo_data: dict) -> tuple:
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']

    weather_data = requests.get(f'{_WEATHER_API}/weather?lat={latitude}&lon={longitude}&units=metric&appid={_WEATHER_API_KEY}').json()
    # weather_data = json.load(open('data/res.json'))

    weather_values = {'code': weather_data['weather'][0]['id'], **weather_data['main']}
    wind_values = {**weather_data['wind']}

    return weather_values, wind_values

def _get_aq_data(geo_data: dict) -> dict:
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']

    aq_data = requests.get(f'{_WEATHER_API}/air_pollution?lat={latitude}&lon={longitude}&units=metric&appid={_WEATHER_API_KEY}').json()
    # aq_data = json.load(open('data/res2.json'))

    aq_values = {'code': aq_data['list'][0]['main']['aqi'], **aq_data['list'][0]['components']}

    return aq_values

def get_weather_aq_data() -> dict:
    # Get IP public
    ip = requests.get(_IP_API).content.decode()

    # Get geolocalization data from IP
    headers = {'User-Agent': 'PostmanRuntime/7.33.0'}
    geo_data = requests.get(f'{_GEODATA_API}/{ip}/json/', headers=headers).json()

    city = geo_data['city']
    country = geo_data['country_name']
    timezone = geo_data['timezone']

    date = datetime.now(zoneinfo.ZoneInfo(timezone))

    weather_values, wind_values = _get_weather_data(geo_data)
    aq_values = _get_aq_data(geo_data)

    return ({
        'city': city,
        'country': country,
        'datetime': date.isoformat(),
        'weather': weather_values,
        'wind': wind_values,
        'aq': aq_values
    })
