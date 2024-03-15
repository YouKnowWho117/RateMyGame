import os
basedir = os.path.abspath(os.path.dirname(__file__))

class config(object):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'fudi'
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://flaskdblz:00sJ%Z!m5&80IMQZ^TK!7K!3ps*8RdDu@dbflasklz.mysql.database.azure.com:3306/doodle'
        SQLALCHEMY_TRACK_MODIFICATIONS = False