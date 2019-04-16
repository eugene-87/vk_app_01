from app import app
from .db import get_db
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from app.forms import SearchForm
from app.utils import search_users
from app.utils import get_user_by_id
from app.utils import get_url_for_code
from app.utils import get_access_token
from app.utils import get_groups_by_user_id
from app.utils import get_posts_of_user_on_group_wall
from app.utils import write_user_to_db
from app.utils import update_extended_user_info
from app.utils import update_user_in_db
from app.utils import get_number_of_technical_groups
from datetime import datetime
from datetime import timedelta
from pprint import pprint


#########################################
# INDEX PAGE
#########################################

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    print('---User {} has loged in with access token {}'.format(
        session['user_id'], session['access_token']))

    title = 'Home | Vkontakte App'
    form = SearchForm()
    response = get_user_by_id(
        session['user_id'], session['access_token'])

    if 'error' in response:
        print('---ERROR: {}'.format(response['error']['error_msg']))
        print('---REDIRECTING TO {}'.format(url_for('login')))
        return redirect(url_for('login'))

    session['first_name'] = response['response'][0]['first_name']
    session['last_name'] = response['response'][0]['last_name']
    session['photo_50'] = response['response'][0]['photo_50']

    return render_template('index.html', title=title, form=form)


#########################################
# LOGIN
#########################################

@app.route('/login')
def login():
    # for first we will be redirected to the auth page of VK
    # we should type our login and password and press login
    # after that we will be redirected back to the login page
    # of our site where we will find the code in the url query
    # then we will request an access token and will be redirected
    # to our login page where we will find json request with an
    # access token
    # Then we write the access token to the session

    # if code is in url query, i.e. we

    if request.args.get('code'):
        code = request.args.get('code')
        print('---got code: {}'.format(code))
        response = get_access_token(code)

        if 'error' in response:
            print('---ERROR: {}'.format(response['error_description']))
            return redirect(url_for('login'))

        user_id = response['user_id']
        access_token = response['access_token']
        print('---User id - {} got access token'.format(user_id))
        print('--- {}'.format(access_token))
        session['user_id'] = user_id
        session['access_token'] = access_token

        return redirect(url_for('index'))

    return redirect(get_url_for_code())


#########################################
# LOGOUT
#########################################

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


#########################################
# SEARCH USERS
#########################################

# !!! don't forget to create pagination system
@app.route('/search', methods=['GET', 'POST'])
def search():
    # if we went to this page without clicking the search button
    # on the index page we will redirected to the index page
    if request.method == 'GET':
        print(request.method)
        return redirect(url_for('index'))

    title = 'Search | Vkontakte App'

    # get list of users from api
    q = request.form['q']
    country = request.form['country']
    sex = request.form['sex']
    age_from = request.form['age_from']
    age_to = request.form['age_to']
    data = search_users(
        q, country, sex, age_from, age_to, session['access_token'])

    # check if we have some error in the response json from api
    if 'error' in data:
        print('---ERROR: {}'.format(data['error']['error_msg']))
        return redirect(url_for('index'))

    response_users = data['response']['items']

    # WRITE USERS TO THE DATABASE

    # actually we don't need to use database in this case
    # we use it just for collect all recieved data about VK users
    # for something else

    db = get_db()
    vk_ids_for_template = []

    for user in response_users:
        # add vk_id of each user we got from api to know
        # which users we need to get from our db
        vk_ids_for_template.append(user['id'])

        # we need to change birthday of each user from
        # '%d.%m' / '%d.%m.%Y' to '%d %b' / '%d %b %Y'
        if 'bdate' in user:
            try:
                # if bdate doesn't include a year
                bdate = datetime.strptime(user['bdate'], '%d.%m')
                user['bdate'] = bdate.strftime('%d %b')
            except ValueError:
                # if bdate includes a year
                bdate = datetime.strptime(user['bdate'], '%d.%m.%Y')
                user['bdate'] = bdate.strftime('%d.%m.%Y')

        # write user info in the db if it's not
        if db.execute(
            'SELECT id FROM users WHERE vk_id = ?', (user['id'],)
        ).fetchone() is None:
            write_user_to_db(db, user)
            update_extended_user_info(db, user)
        else:
            # update user info in the db
            update_user_in_db(db, user)
            update_extended_user_info(db, user)

    db.commit()

    # !!! THIS CODE IS NOT USING !!!
    # we can use 'executemany' method instead 'execute'

    # get users which we've got via api from the db
    users = []
    for vk_id in vk_ids_for_template:
        user_from_db = db.execute(
            'SELECT * FROM users WHERE vk_id = ?', (vk_id,)
        ).fetchone()
        if user_from_db is not None:
            users.append(user_from_db)

    return render_template('search.html', title=title, users=response_users)


#########################################
# USER PAGE
#########################################

@app.route('/user/id_<int:user_id>')
def user(user_id):
    title = 'User | Vkontakte App'

    # get user's info
    user = get_user_by_id(user_id, session['access_token'])
    if 'error' in user:
        print('--- ERROR: {}'.format(user['error']['error_msg']))
        return redirect(url_for('index'))

    # get list of user's groups
    groups = get_groups_by_user_id(user_id, session['access_token'])
    if 'error' in groups:
        print('--- ERROR: {}'.format(groups['error']['error_msg']))
        return redirect(url_for('index'))

    # we need to create a function which recieves a groups list
    # and returns number of technical groups in the list
    group_counts = get_number_of_technical_groups(groups)
    return render_template(
        'user.html', title=title, user=user['response'][0], groups=groups,
        group_counts=group_counts)


#########################################
# GROUP PAGE
#########################################

@app.route('/user/id_<int:user_id>/group/id_<int:group_id>')
def group(user_id, group_id):

    title = 'Group | Vkontakte App'

    # get posts of user
    posts_of_user = get_posts_of_user_on_group_wall(
        group_id, user_id, session['access_token'])
    pprint(posts_of_user)
    return render_template('group.html', title=title, posts_of_user=posts_of_user)
