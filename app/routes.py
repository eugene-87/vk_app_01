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
from app.utils import get_code_for_access_token
from app.utils import get_access_token


#########################################
# INDEX PAGE
#########################################

@app.route('/')
def index():
    # if user is not loged in then redirect to login page
    # if 'username' not in session:
    #     return redirect(url_for('login'))
    if 'user_id' not in session:
        return redirect(url_for('login'))

    print('User {} has loged in with access token {}'.format(
        session['user_id'], session['access_token']))
    title = 'Home | Vkontakte App'
    form = SearchForm()
    data = get_user_by_id(
        session['user_id'], session['access_token'])
    if 'error' in data:
        flash('{}'.format(data['error']['error_msg']))
        return redirect(url_for('index'))
    session['first_name'] = data['response'][0]['first_name']
    session['last_name'] = data['response'][0]['last_name']
    session['photo_100'] = data['response'][0]['photo_100']

    return render_template('index.html', title=title, form=form)


#########################################
# LOGIN
#########################################

@app.route('/login')
def login():
    title = 'Login | Vkontakte App'
    # выполнять только, если передан код в url
    # данное условие может быть не верное
    if 'REFERER' in request.headers and \
            request.headers['REFERER'] == 'http://127.0.0.1:5000/login':
        code = request.args.get('code')
        print('--- Got code {}'.format(code))

        if code:
            data = get_access_token(code)

            db = get_db()
            vk_id = (data['user_id'], )

            # Check if the user doesn't exist yet
            user = db.execute(
                'SELECT * FROM user WHERE vk_id=?', vk_id).fetchone()
            if user is None:
                db.execute(
                    'INSERT INTO user(vk_id, access_token) VALUES(?, ?)',
                    (data['user_id'], data['access_token'],))

            # if the user already exists we override his access token
            else:
                db.execute(
                    'UPDATE user SET access_token=? WHERE vk_id=?',
                    (data['access_token'], data['user_id'],))
            db.commit()

            # add current user to the session
            session.clear()
            session['user_id'] = data['user_id']
            session['access_token'] = data['access_token']
            return redirect(url_for('index'))

    return render_template('login.html', title=title,
                           get_code_for_access_token=get_code_for_access_token)


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

@app.route('/search', methods=['GET', 'POST'])
def search():
    title = 'Search | Vkontakte App'
    q = request.form['q']
    country = request.form['country']
    sex = request.form['sex']
    age_from = request.form['age_from']
    age_to = request.form['age_to']

    data = search_users(
        q, country, sex, age_from, age_to, session['access_token'])

    if 'error' in data:
        flash('{}'.format(data['error']['error_msg']))
        return redirect(url_for('login'))

    users = data['response']['items']

    return render_template('search.html', title=title, users=users)
