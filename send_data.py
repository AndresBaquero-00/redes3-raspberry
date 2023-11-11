import os
import requests
from dotenv import load_dotenv

from mq135 import get_data
from weather_aq_data import get_weather_aq_data

load_dotenv()

API_URL = os.getenv('API_HOST') + '/api/v2'
data = {**get_data(), **get_weather_aq_data()}

res = requests.post(f'{API_URL}/save', json=data, headers={'Content-Type': 'application/json'})
print(res.content)