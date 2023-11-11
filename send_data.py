import json
import os
import requests
from Crypto.Cipher import AES
from Crypto.Util import Padding
from dotenv import load_dotenv

from mq135 import get_data
from weather_aq_data import get_weather_aq_data

load_dotenv()

API_URL = os.getenv('API_HOST') + '/api/v2'
data = {**get_data(), **get_weather_aq_data()}

key = os.getenv('CRYPTO_KEY')
cipher = AES.new(bytes.fromhex(key), AES.MODE_ECB)
encoded = cipher.encrypt(Padding.pad(json.dumps(data).encode(), 16))

res = requests.post(f'{API_URL}/save', json=data, headers={'Content-Type': 'application/json'})
print(res.content)

res = requests.post(f'{API_URL}/save-secure', data=encoded.hex(), headers={'Content-Type': 'text/plain'})
print(res.content)