from dotenv import load_dotenv
import os
# from pathlib import Path    # env_path
# env_path = Path('../${WEB_APP_DIR_V2}/config') / '.env'
# load_dotenv(dotenv_path=env_path)
load_dotenv()


class Configuration(object):
    HTML_TITLE_COMPANY = 'EngiLogic'
    DEBUG = True
    DBUSER = os.getenv("DBUSER")
    DBPASWD = os.getenv("DBPASWD")
    DBNAME = os.getenv("DBNAME")

    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://pythonuser:flaskdefault@localhost:3306/webappdb'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@localhost:3306/{}'.format(DBUSER, DBPASWD, DBNAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
