import os
import requests
from dotenv import load_dotenv

from mq135 import get_data
from weather_aq_data import get_weather_aq_data

load_dotenv()

data = {**get_data(), **get_weather_aq_data}

res = requests.post(os.getenv('API_HOST'), data, headers={'Content-Type': 'application/json'})
print(res.json())