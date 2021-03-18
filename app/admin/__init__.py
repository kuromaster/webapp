from flask import Blueprint, request, render_template
from flask.views import View
from app.admin.models import Post, Tag
from app.color_print import cprint
from config.config import Configuration


admin_panel = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


class DynView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, url):
        self.model = model
        self.url = url
        self.pgname = 'Manage ' + self.model.__name__

    def dispatch_request(self):
        if request.method == 'GET':
            cols = self.model.__table__.columns.keys()
            elements = self.model.query.order_by(self.model.id.desc()).all()

            return render_template(
                "dynamic.html",
                pgname=self.pgname,
                company=Configuration.HTML_TITLE_COMPANY,
                elements=elements,
                cols=cols,
                tb_name=self.model.__name__.lower(),
                dynamic=True,
                menu=menu.get_menu())


class DynMenu(object):

    def __init__(self, name):
        self.name = name
        self.menu = {}

    def add_menu(self, label, url):
        # cprint("YELLOW", "key: {} val: {}".format(label, url))
        self.menu.update({label: url})

    def get_menu(self):
        return self.menu.items()


class DynPage(object):
    def __init__(self, app=None, ):
        self.app = app

    def add_view(self, url=None, endpoint=None, model=None):
        self.app.add_url_rule('/dynamic/' + url, view_func=DynView.as_view(endpoint, model=model, url=url))


menu = DynMenu('admin_menu')
dp = DynPage(admin_panel)

dp.add_view('post', 'tb_post', Post)
menu.add_menu(Post.__name__, '/admin/dynamic/' + Post.__name__.lower())

dp.add_view('tag', 'tb_tag', Tag)
menu.add_menu(Tag.__name__, '/admin/dynamic/' + Tag.__name__.lower())
