from dotenv import load_dotenv
import os


load_dotenv()


class Configuration(object):

    # App DIR
    WORK_DIR = "/root/flask/v3/webapp"

    # html
    HTML_TITLE_COMPANY = 'EngiLogic'

    # app
    DEBUG = True
    THREADED = True

    # MySQL
    DBUSER = os.getenv("DBUSER")
    DBPASWD = os.getenv("DBPASWD")
    DBNAME = os.getenv("DBNAME")

    # Log path for PrintException
    ERR_PTH = os.getenv("ERR_PTH")

    # app Session, Login
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = os.getenv("SECURITY_PASSWORD_HASH")

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://pythonuser:flaskdefault@localhost:3306/webappdb'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@localhost:3306/{}'.format(DBUSER, DBPASWD, DBNAME)

    # Google Auth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

    # Google spreadsheet
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    SPREADSHEET_RANGE = "B4:AG12"
