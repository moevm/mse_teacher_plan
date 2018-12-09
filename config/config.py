import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'future-secret-key'
    MONGODB_SETTINGS = os.environ.get('MONGODB_SETTINGS') or {
        'db': 'moevm_flask',
        'host': '127.0.0.1',
        'port': 27017,
        'username': 'python',
        'password': 'python'
    }

