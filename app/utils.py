from app import app
import requests


#########################################
# SEARCH USERS BY NAME
#########################################

def search_users(q, country, sex, age_from, age_to):
    url = 'https://api.vk.com/method/users.search'
    params = {
        'v': 5.92,
        'access_token': app.config['VK_ACCESS_TOKEN'],
        'fields': 'photo_100,schools,university,career,bdate,city,country',
        'q': q,
        'country': country,
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to
    }
    r = requests.get(url, params)
    return r.json()
