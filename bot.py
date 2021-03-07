from settings import TOKEN
import telebot
from telebot import types
from country_info import find_wiki
import weather
import json
import datetime
import locale
import os.path
import time
import requests


bot = telebot.TeleBot(TOKEN, parse_mode=None)
bot_async = telebot.AsyncTeleBot(TOKEN)

locale.setlocale(locale.LC_TIME, "ru")

@bot.message_handler(commands=['start'])
def sendMessage(message):
	created_at = datetime.date.today()
	list_data = ({'user_id':message.chat.id, 'created_at':str(datetime.date.today()), 'country':'', 'time':''})
	if os.path.isfile(f'users/{message.chat.id}.json'):
		with open(f'users/{message.chat.id}.json', 'r') as read_file:
			data = json.load(read_file)
			user_id = data['user_id']
			created_at = data['created_at']
			bot.send_message(user_id, f'Welcome to our bot. \n\n Your date registration: {created_at}')
	else:
		try:
			with open(f'users/{message.chat.id}.json', 'w') as write_file:
				json.dump(list_data, write_file)
			bot.send_message(message.chat.id, 'Welcome to bot. This bot can be search weather in the world. Please write which country do you search')
		except Exception as e:
			print(e)


@bot.message_handler(commands=['add'])
def addCountry(message):
	bot_async.send_message(message.chat.id, 'Please send your new country or town')
	if message.text != '/add':
		country = message.text
		time_user = time.localtime(time.time()).tm_hour
		result = weather.search_weather(country)
		if len(result) < 3:
			bot_async.send_message(message.chat.id, 'Error 404\n\n Your country not found global base.\n Try again')
		else:
			weather_graduce = result['main']['temp']
			weather_cloud = result['weather'][0]['description']
			weather_id = result['id']
			url = find_wiki(country)
			bot_async.send_message(message.chat.id, f'<strong>Погода в {message.text} </strong>\n\n Temp: {round(weather_graduce)} °С\n Cloud: {weather_cloud} \n Id:{weather_id}\n Link: {url}\n\n<strong>This notification for {country} will be send every hour for you</strong>', parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def reply_to_weather(message):
	country = message.text
	time_user = time.localtime(time.time()).tm_hour
	result = weather.search_weather(country)

	try:
		with open(f'users/{message.chat.id}.json', 'r') as read_file:
			data = json.load(read_file)
			data['country'] = country
			data['time'] = str(time_user+1)
			with open(f'users/{message.chat.id}.json', 'w') as write_file:
				json.dump(data, write_file)

	except Exception as e:
		print(e)

	if len(result) < 3:
		bot.send_message(message.chat.id, 'Error 404\n\n Your country not found global base.\n Try again')
	else:
		weather_graduce = result['main']['temp']
		weather_cloud = result['weather'][0]['description']
		weather_id = result['id']
		url = find_wiki(country)
		bot.send_message(message.chat.id, f'<strong>Погода в {message.text} </strong>\n\n Temp: {round(weather_graduce)} °С\n Cloud: {weather_cloud} \n Id:{weather_id}\n Link: {url}\n\n<strong>This notification for {country} will be send every hour for you</strong>', parse_mode='HTML')
		if message.text != '/add':
			send_notification(message.chat.id)


# notification for bot in choosen country user
def send_notification(user_id):
	time.sleep(600)
	with open(f'users/{user_id}.json') as load_file:
		data = json.load(load_file)
		result = weather.search_weather(data['country'])
		weather_graduce = result['main']['temp']
		weather_cloud = result['weather'][0]['description']
		weather_id = result['id']
		country = data['country']
		url = find_wiki(country)
		bot.send_message(data['user_id'], f'<strong>Погода в {country} </strong>\n\n Temp: {round(weather_graduce)} °С\n Cloud: {weather_cloud} \n Id:{weather_id}\n Link: {url}\n\n<strong>This notification for {country} will be send every hour for you</strong>', parse_mode='HTML')
		send_notification(data['user_id'])
bot.polling()




