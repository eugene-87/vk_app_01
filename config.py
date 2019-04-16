import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'

    VK_CLIENT_ID = '6894406'

    DATABASE = os.environ.get('DATABASE') or \
        os.path.join(basedir, 'app.db')

    USERS_PER_PAGE = 25
