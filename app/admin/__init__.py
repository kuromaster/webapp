from flask import Blueprint, request, render_template
# from flask_security import SQLAlchemyUserDatastore
from flask_security import login_required

from flask.views import View
from app.admin.models import Post, Tag, Customer, User, Role
from app.color_print import cprint
from config.config import Configuration


admin_panel = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# user_datastore = SQLAlchemyUserDatastore(db, User, Group)


class DynView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, url, membership):
        self.model = model
        self.url = url
        self.membership = membership
        self.pgname = 'Manage ' + self.model.__name__

    def dispatch_request(self):
        if request.method == 'GET':
            cols = self.model.__table__.columns.keys()
            elements = self.model.query.order_by(self.model.id.desc()).all()

            return render_template(
                "/admin/dynamic.html",
                pgname=self.pgname,
                company=Configuration.HTML_TITLE_COMPANY,
                elements=elements,
                cols=cols,
                tb_name=self.model.__name__.lower(),
                dynamic=True,
                menu=menu.get_menu(),
                membership=self.membership)


class DynPage(object):
    def __init__(self, app=None, ):
        self.app = app

    def add_view(self, model=None, url=None, endpoint=None, membership=None):
        if url is None:
            url = model.__name__.lower()

        if endpoint is None:
            endpoint = 'tb_{}'.format(model.__name__.lower())

        self.app.add_url_rule('/dynamic/' + url, view_func=login_required(DynView.as_view(endpoint, model=model, url=url, membership=membership)))


class DynMenu(object):

    def __init__(self, name):
        self.name = name
        self.menu = {}

    def add_menu(self, label=None, url=None):
        # cprint("YELLOW", "key: {} val: {}".format(label, url))
        if url is None:
            url = '/admin/dynamic/{}'.format(label.lower())
        self.menu.update({label: url})

    def get_menu(self):
        return self.menu.items()


'''
        Динамически страницы:
    Для подключения нужно:
    1. Создать объект меню:                     menu=DynMenu('menu_name')
    2. Создать объект страницы:                 dp=DynPage(app)
    3. Добавить класс в app или Blueprint:      from model import Example
    3. Добавить класс в виюху:                  from model import Example
    4. Добавить вьюху(саму страницу):           dp.add_view(url='example', endpoint='tb_example', model=Example)
        *) полное url - http://app/dynamic/example  от класса DynPage добавляется /dynamic/
        *) model - класс с помощью которого создается таблица

    5. Добавить ссылку в дин. меню:             menu.add_menu(label='Example', url='/admin/dynamic/example')

'''

menu = DynMenu('admin_menu')
dp = DynPage(admin_panel)

dp.add_view(model=Post, membership='tags')
menu.add_menu('Post')

dp.add_view(Tag)
menu.add_menu('Tag')

dp.add_view(model=User, membership='roles')
menu.add_menu('User')

dp.add_view(Role)
menu.add_menu('Role')

dp.add_view(Customer, 'customer', 'tb_customer')
menu.add_menu(Customer.__name__, '/admin/dynamic/' + Customer.__name__.lower())
