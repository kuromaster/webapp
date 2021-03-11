from app import app
from app import db
from app import view
from app.admin import admin_panel, view_admin

app.register_blueprint(admin_panel, url_prefix='/admin')

if __name__ == "__main__":
    app.run(threaded=True, debug=True)
