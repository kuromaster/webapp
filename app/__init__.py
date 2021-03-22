from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from datetime import date
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security


from config.config import Configuration



class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat(sep=' ')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.config.from_object(Configuration)
app.json_encoder = CustomJSONEncoder

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.admin.models import User, Role
# from app.color_print import cprint

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# if security is not None:
#     for i in dict(security):
#         cprint("YELLOW", "security: {}".format(i))
# if user_datastore is not None:
#     for j in dict(user_datastore):
#         cprint("BLUE", "user_datastore: {}".format(j))
