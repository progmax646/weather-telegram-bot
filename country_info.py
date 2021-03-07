import requests
import re 


URL = 'https://ru.wikipedia.org/wiki/'

def find_wiki(country):
	status_text = has_cyrillic(country)
	if status_text == True:
		return URL+country
	else:
		return 'https://en.wikipedia.org/wiki/'+country




def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

