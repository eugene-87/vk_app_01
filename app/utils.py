from app import app
import requests


#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                           USER UTILS
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#########################################
# GET USER BY ID
#########################################

def get_user_by_id(user_id, access_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'v': 5.92,
        'access_token': access_token,
        'fields': 'photo_50',
        'user_ids': user_id,
    }
    r = requests.get(url, params=params)
    return r.json()


#########################################
# SEARCH USERS BY HIS FIRST AND SECOND NAMES
#########################################

def search_users(q, country, sex, age_from, age_to, access_token):
    url = 'https://api.vk.com/method/users.search'
    params = {
        'v': 5.92,
        'access_token': access_token,
        'count': 1000,
        'fields': '''
            photo_100, about, activities, bdate, books, career,
            schools, universities, city, country, games, interests,
            military, movies, music, occupation, personal, quotes,
            relation, sex, tv, connections''',
        'q': q,
        'country': country,
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to,
    }
    r = requests.get(url, params=params)
    return r.json()


#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                           GROUP UTILS
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#########################################
# GET POSTS ON A GROUP WALL
#########################################

def get_posts_from_group_wall(group_id, access_token):
    url = 'https://api.vk.com/method/wall.get'

    # we must use owner_id with sign '-' (minus) if it's a group
    params = {
        'v': 5.92,
        'access_token': access_token,
        'owner_id': int(group_id) * (-1),
        'count': 100
    }
    r = requests.get(url, params=params)
    return r.json()


#########################################
# GET COUNT OF USERS POSTS IN A GROUP
#########################################

def get_posts_of_user_on_group_wall(group_id, user_id, access_token):

    posts_of_user = {}
    posts = get_posts_from_group_wall(group_id, access_token)

    if 'error' in posts:
        print('--- ERROR: {}'.format(posts['error']['error_msg']))
    else:
        for post in posts['response']['items']:
            if post['owner_id'] == user_id:
                posts_of_user[post['id']] = post['text']

    return posts_of_user

#########################################
# GET GROUPS IN WHICH A USER IS A MEMBER
#########################################


def get_groups_by_user_id(user_id, access_token):
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'v': 5.92,
        'access_token': access_token,
        'fields': 'photo_50,description',
        'extended': 1,
        'user_id': user_id
    }
    r = requests.get(url, params=params)
    return r.json()


#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                           AUTHENTICATION UTILS
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#########################################
# GET A CODE FOR AN ACCESS TOKEN
#########################################

def get_url_for_code():
    url = 'https://oauth.vk.com/authorize?'
    params = {
        'client_id': app.config['VK_CLIENT_ID'],
        'display': 'page',
        'redirect_uri': 'http://127.0.0.1:5000/login',
        'scope': 'friends, wall',
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


#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                              DATABASE
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#########################################
# WRITE USERS WHICH WE GOT FROM THE REQUEST TO API TO OUR DB
#########################################

def write_user_to_db(db, user):

    db.execute('''
        INSERT INTO users (
            vk_id,
            photo,
            first_name,
            last_name,
            is_closed
            )
        VALUES (?, ?, ?, ?, ?)
    ''', (
        user['id'],
        user['photo_100'],
        user['first_name'],
        user['last_name'],
        user['is_closed'],
    )
    )


def update_extended_user_info(db, user):

    # check if a user have some additional info and update a user's raw
    if 'sex' in user:
        db.execute('UPDATE users SET sex = ? WHERE vk_id = ?', (
            user['sex'], user['id']))
    if 'bdate' in user:
        db.execute('UPDATE users SET bdate = ? WHERE vk_id = ?', (
            user['bdate'], user['id']))
    if 'country' in user:
        db.execute('UPDATE users SET country = ? WHERE vk_id = ?', (
            user['country']['title'], user['id']))
    if 'city' in user:
        db.execute('UPDATE users SET city = ? WHERE vk_id = ?', (
            user['city']['title'], user['id']))
    if 'about' in user:
        db.execute('UPDATE users SET about = ? WHERE vk_id = ?', (
            user['about'], user['id']))
    if 'activities' in user:
        db.execute('UPDATE users SET activities = ? WHERE vk_id = ?', (
            user['activities'], user['id']))
    if 'books' in user:
        db.execute('UPDATE users SET books = ? WHERE vk_id = ?', (
            user['books'], user['id']))
    if 'games' in user:
        db.execute('UPDATE users SET games = ? WHERE vk_id = ?', (
            user['games'], user['id']))
    if 'movies' in user:
        db.execute('UPDATE users SET movies = ? WHERE vk_id = ?', (
            user['movies'], user['id']))
    if 'music' in user:
        db.execute('UPDATE users SET music = ? WHERE vk_id = ?', (
            user['music'], user['id']))
    if 'quotes' in user:
        db.execute('UPDATE users SET quotes = ? WHERE vk_id = ?', (
            user['quotes'], user['id']))
    if 'tv' in user:
        db.execute('UPDATE users SET tv = ? WHERE vk_id = ?', (
            user['tv'], user['id']))
    if 'interests' in user:
        db.execute('UPDATE users SET interests = ? WHERE vk_id = ?', (
            user['interests'], user['id']))
    if 'deactivated' in user:
        db.execute('UPDATE users SET deactivated = ? WHERE vk_id = ?', (
            user['deactivated'], user['id']))


#########################################
# UPDATE INFO ABOUT USER IN OUR DB
# WHICH WE GOT FROM THE REQUEST TO API
#########################################

def update_user_in_db(db, user):

    db.execute('''
        UPDATE users
        SET vk_id = ?,
            photo = ?,
            first_name = ?,
            last_name = ?,
            is_closed = ?
        WHERE vk_id = ?
        ''', (
        user['id'],
        user['photo_100'],
        user['first_name'],
        user['last_name'],
        user['is_closed'],
        user['id'],
    )
    )


#########################################
# SET DEFAULT VALUES FOR SEX TABLE
#########################################

def get_sex(db):
    sex = {
        0: 'пол не указан',
        1: 'мужской',
        2: 'женский'
    }
    for key, value in sex.items():
        db.execute('INSERT INTO sex (sex_id, value) VALUES (?, ?)', (
            key, value))
    db.commit()


#########################################
# SET DEFAULT VALUES FOR COUNTRIES TABLE
#########################################

def get_countries(access_token, db):
    url = 'https://api.vk.com/method/database.getCountries'
    params = {
        'v': 5.92,
        'access_token': access_token,
        'need_all': 1,
        'count': 1000,
    }
    r = requests.get(url, params=params)

    if 'error' in r.json():
        print('---ERROR: {}'.format(r.json()['error']['error_msg']))

    countries = r.json()['response']['items']

    for country in countries:
        db.execute('INSERT INTO countries (country_id, value) VALUES (?, ?)', (
            country['id'], country['title']))

    db.commit()


#########################################
# SET DEFAULT VALUES FOR CITIES TABLE
#########################################

def get_cities(access_token, db, country_id):
    url = 'https://api.vk.com/method/database.getCities'
    params = {
        'v': 5.92,
        'access_token': access_token,
        'country_id': country_id,
        'need_all': 0,
        'count': 1000,
    }
    r = requests.get(url, params=params)

    if 'error' in r.json():
        print('---ERROR: {}'.format(r.json()['error']['error_msg']))

    cities = r.json()['response']['items']

    for city in cities:
        db.execute(
            'INSERT INTO cities (city_id, value, country_id) VALUES (?, ?, ?)', (
                city['id'], city['title'], country_id))
    db.commit()


#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                              USER ANALYSIS
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#########################################
# GET COUNT OF USER'S TECHNICAL AND HUMANITARIAN GROUPS
#########################################

def get_number_of_technical_groups(groups_list):
    key_words = []
    technical_groups = []
    humanitarian_groups = []
    # loop through the list of groups and check which kind of group
    for group in groups_list:
        for key_word in key_words:
            if key_word in group.name or key_word in group.description:
                technical_groups.append(group)
            else:
                humanitarian_groups.append(group)

    return {'count_of_technical_groups': len(technical_groups),
            'count_of_humanitarian_groups': len(humanitarian_groups)}
