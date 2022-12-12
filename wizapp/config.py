import os


class config:
    SECRET_KEY = '78aea450efb53c77db6c2564c55ed647'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_DEFAULT_SENDER = 'WishotStudio@gmail.com'
