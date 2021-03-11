from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Configuration
# from app.admin import admin_panel


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)



# from app.admin import view_admin
