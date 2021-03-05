import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Windows = C:\Documents\coding-temple-feb-2021\week5\feb_intro_to_flask
# Mac & Linux = Documents/codingtemple-feb-2021/week5/feb_intro_to_flask

class Config():
    FLASK_APP=os.environ.get('FLASK_APP')
    FLASK_ENV=os.environ.get('FLASK_ENV')
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you will never guess....'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') #sqlite///c:\Documents\coding-temple-feb-2021\week5\feb_intro_to_flask
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
