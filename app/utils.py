from app import app
import requests


#########################################
# GET USER BY ID
#########################################

def get_user_by_id(user_id, access_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'v': 5.92,
        'access_token': access_token,
        'fields': 'photo_100',
        'user_ids': user_id,
    }
    r = requests.get(url, params=params)
    return r.json()


#########################################
# SEARCH USERS BY NAME
#########################################

def search_users(q, country, sex, age_from, age_to, access_token):
    url = 'https://api.vk.com/method/users.search'
    params = {
        'v': 5.92,
        'access_token': access_token,
        'fields': 'photo_100,schools,university,career,bdate,city,country',
        'q': q,
        'country': country,
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to
    }
    r = requests.get(url, params=params)
    return r.json()


#########################################
# GET A CODE FOR AN ACCESS TOKEN
#########################################

def get_code_for_access_token():
    url = 'https://oauth.vk.com/authorize?'
    params = {
        'client_id': app.config['VK_CLIENT_ID'],
        'display': 'page',
        'redirect_uri': 'http://127.0.0.1:5000/login',
        'scope': 'friends',
        'response_type': 'code',
        'v': '5.92',
    }
    for param, value in params.items():
        url += param + '=' + value + '&'
    return url[:len(url)-1]


#########################################
# GET AN ACCESS TOKEN
#########################################

def get_access_token(code):
    url = 'https://oauth.vk.com/access_token?'
    params = {
        'client_id': app.config['VK_CLIENT_ID'],
        'client_secret': 'LIj71pwcYoDT17gA1zhy',
        'redirect_uri': 'http://127.0.0.1:5000/login',
        'code': str(code),
    }
    r = requests.get(url, params=params)
    return r.json()
