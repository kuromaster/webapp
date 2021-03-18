from app import app
from app import db
from app import view
from app.admin import admin_panel, view_admin

# from flask import render_template, request
# from flask.views import View
# from app.admin.models import Post, Tag
# from config.config import Configuration
# from app.color_print import cprint


app.register_blueprint(admin_panel, url_prefix='/admin')


if __name__ == "__main__":
    app.run()
