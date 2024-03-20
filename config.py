import os
basedir = os.path.abspath(os.path.dirname(__file__))
#set enviroment variables from azure web app
mysql_user = os.environ.get("mysql_user")
mysql_password = os.environ.get("mysql_password")
mysql_host = os.environ.get("mysql_host")

#Connection to DB
class config(object):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'fudi'
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:3306/doodle'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
