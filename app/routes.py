from app import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from app.forms import SearchForm
from app.utils import search_users


#########################################
# INDEX PAGE
#########################################

@app.route('/')
def index():
    title = 'Home | Vkontakte App'
    form = SearchForm()
    return render_template('index.html', title=title, form=form)


#########################################
# SEARCH PAGE
#########################################

@app.route('/search', methods=['GET', 'POST'])
def search():
    title = 'Search | Vkontakte App'
    q = request.form['q']
    country = request.form['country']
    sex = request.form['sex']
    age_from = request.form['age_from']
    age_to = request.form['age_to']

    data = search_users(q, country, sex, age_from, age_to)

    if 'error' in data:
        flash('{}'.format(data['error']['error_msg']))
        return redirect(url_for('index'))

    users = data['response']['items']

    return render_template('search.html', title=title, users=users)
