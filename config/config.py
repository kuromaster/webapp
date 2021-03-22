from dotenv import load_dotenv
import os


load_dotenv()


class Configuration(object):
    HTML_TITLE_COMPANY = 'EngiLogic'

    DEBUG = True
    THREADED = True

    DBUSER = os.getenv("DBUSER")
    DBPASWD = os.getenv("DBPASWD")
    DBNAME = os.getenv("DBNAME")
    ERR_PTH = os.getenv("ERR_PTH")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = os.getenv("SECURITY_PASSWORD_HASH")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://pythonuser:flaskdefault@localhost:3306/webappdb'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@localhost:3306/{}'.format(DBUSER, DBPASWD, DBNAME)
