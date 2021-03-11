from flask import render_template
from app import app
from config.config import Configuration
from app import models


# NOTE: Домашняя страница
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    return render_template("home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY)
