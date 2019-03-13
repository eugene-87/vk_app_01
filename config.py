import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    VK_ACCESS_TOKEN = '9a44eae888e06c8ac379dbb7b68bf5696c6f571c8808c38b028cb0ba7bfb537bd4c59e10ba545ccfad096'
