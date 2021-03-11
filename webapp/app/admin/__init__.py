from flask import Blueprint


admin_panel = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
