# this class for search weather in the https://openweathermap.org/api

from settings import API_WHEATHER, API_URL
import requests

headers = {'user-agent': 'my-app/0.0.1'}

def search_weather(city):
	try:
		query = requests.get(API_URL, headers=headers, params={'q':city, 'units':'metric','appid':API_WHEATHER})
		return query.json()
	except Exception as e:
		return e