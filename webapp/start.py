from app import app
from app import db
from app import view
from flask_admin import Admin
# from app.admin import admin_panel, view_admin
from app.view_admin_app import MyHomeView
from flask_admin.contrib.sqla import ModelView
from app.models import Post, Tag


# app.register_blueprint(admin_panel, url_prefix='/admin')
admin = Admin(app, index_view=MyHomeView(name='Home', endpoint='admin'))
admin.add_view(ModelView(Post, db.session))


if __name__ == "__main__":
    app.run(threaded=True)
