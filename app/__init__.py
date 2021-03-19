from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from datetime import date
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

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

# class EndpointAction(object):
#
#     def __init__(self, action):
#         self.action = action
#         self.response = Response(status=200, headers={})
#
#     def __call__(self, *args):
#         self.action()
#         return self.response

# PageView('smstable')
