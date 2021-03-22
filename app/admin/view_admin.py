from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from werkzeug.security import generate_password_hash
from flask_security import login_required, roles_required, current_user
# from datetime import datetime
# import json
import re

from app.admin import admin_panel, menu
from config.config import Configuration
from app.admin.models import Post, Tag, Customer, User, Role
from app.color_print import cprint, PrintException
from app.admin.forms import PostForm
from app import db


err_pth = Configuration.ERR_PTH


'''
    [Блок - ChangeLog]
'''


# NOTE: Домашняя страницы админки. Она же ChangeLog
@admin_panel.route('/', methods=['POST', 'GET'])
@login_required
@roles_required('admin', 'user')
def index():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception as ex:
            cprint("RED", "Error: Post insert tk db. ex: {}".format(ex))

        return redirect(url_for('admin.index'))

    form = PostForm()
    q = request.args.get('q')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=7)

    return render_template("admin/home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), form=form, pages=pages, menu=menu.get_menu(), User="{} {}".format(current_user.lastname, current_user.name))


# NOTE: Переход к посту по ссылке (работает через строку, управление не реальзовано)
@admin_panel.route('/post/<slug>')
@login_required
@roles_required('admin', 'user')
def post_detail(slug):
    cprint("YELLOW", "slug: |{}|".format(slug))
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    return render_template('admin/post_detail.html', pgname="post_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), post=post, tags=tags)


# NOTE: Ссылка редактирования поста
@admin_panel.route('/post/<slug>/edit', methods=['POST', 'GET'])
@login_required
@roles_required('admin', 'user')
def post_edit(slug):
    cprint('YELLOW', 'REQUEST METHOD: {}'.format(request.method))
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'title': post.title, 'body': post.body})
    if request.method == 'POST':

        try:
            form = PostForm(formdata=request.form, obj=post)
            form.populate_obj(post)
            db.session.commit()
        except Exception as ex:
            PrintException(err_pth)
            return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

        return jsonify({'status': 'ok'})


# NOTE: Удаление поста через ссылку
@admin_panel.route('/post/<slug>/rm', methods=['POST', 'GET'])
@login_required
@roles_required('admin', 'user')
def post_remove(slug):
    cprint('YELLOW', 'REQUEST METHOD: {}'.format(request.method))
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'title': post.title, 'id': post.id})
    if request.method == 'POST':

        try:
            cprint("RED", "REQ: {}".format(request.form))
            db.session.delete(post)
            db.session.commit()
        except Exception as ex:
            PrintException(err_pth)
            return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

        return jsonify({'status': 'ok'})


# NOTE: Страница отображения постов связанных с slug тега
# @admin_panel.route('/tag/<slug>')
# @login_required
# @roles_required('admin', 'user')
# def tag_detail(slug):
#     tag = Tag.query.filter(Tag.slug == slug).first_or_404()
#     posts = tag.posts.all()
#     return render_template('admin/tag_detail.html', pgname="tag_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), posts=posts, tag=tag)


'''
    [Блок - Динамические страницы.]
    Страницы содержат таблицы БД с возможностью управления:
        - создание
        - удаление
        - редактирование
'''


# NOTE: Динамические страницы. Редактирование
@admin_panel.route('/dynamic/<tb_name>/edit/<id>/<membership>', methods=['POST', 'GET'])
@login_required
@roles_required('admin', 'user')
def dyn_edit(tb_name, id, membership):
    cprint('YELLOW', 'dyn_edit REQUEST METHOD: {}'.format(request.method))

    Model = globals()[tb_name.capitalize()]
    Model_mmbr = None
    columns = Model.__table__.columns.keys()
    values = Model.query.filter(Model.id == id).first_or_404()

    data = {}
    data.clear()
    data_tag = {}
    data_tag.clear()

    if membership != 'dyn-empty':
        tags = getattr(values, membership)
        if tags:
            # cprint("CYAN", "tags: {}".format(type(tags)))
            data_tag.update({'membership': membership})
            i = 0

            for tag in tags:
                Model_mmbr = type(tag)
                cols = type(tag).__table__.columns.keys()
                i += 1

                for col in cols:
                    # cprint("GREEN", "elemnet[{}]: {}, {}".format(i, col, getattr(tag, col)))
                    data_tag.update({'tag_{}_{}'.format(i, col): getattr(tag, col)})

                # for field in tag:
                #     cprint("BLUE", "elemnet: {}".format(field))
                #     data.update({'tag_field_' + membership: field})
        else:
            data_tag.update({'membership': membership})
            tags = getattr(Model, membership)
            Model_mmbr = tags.property.mapper.class_
            # cprint("YELLOW", "search: {}".format(type(tags.property.mapper.class_)))
            # cprint("YELLOW", "search2: {}".format(type(Model)))
            # Model.tags.property.mapper.class_
            # getattr(Model, membership).tags.property.mapper.class_
    else:
        data_tag.update({'membership': membership})

    if request.method == 'GET':

        for column in columns:
            data.update({column: getattr(values, column)})

        data.update(data_tag)
        data.update({'status': 'ok'})
        return jsonify(data)

    data.clear()
    if request.method == 'POST':

        # cprint("BLUE", "POST data: {}".format(request.values))

        if membership != 'dyn-empty':

            # cprint("RED", "POST membership: {}; Model_mmbr: {};".format(membership, type(Model_mmbr)))
            # cprint("CYAN", "POST data_tag: {}".format(list(data_tag.values())))

            # add tags to element
            cprint("CYAN", "POST data [current]: {}".format(request.form[membership]))
            if request.form[membership]:
                for tag in re.findall(r"[\w']+", request.form[membership]):
                    if tag in list(data_tag.values()):
                        cprint("PURPLE", "check [add] tag: {} --- false".format(tag))
                    else:
                        cprint("GREEN", "check [add] tag: {}, --- True. Will be appended".format(tag))

                        is_tag_exist = Model_mmbr.query.filter(Model_mmbr.name == tag).first()
                        if is_tag_exist is None:
                            tag_to_db = Model_mmbr(name=tag)
                            db.session.add(tag_to_db)
                            db.session.commit()
                        getattr(values, membership).append(Model_mmbr.query.filter(Model_mmbr.name == tag).first())

                # remove tag from element
                for tag in iter(v for k, v in data_tag.items() if 'name' in k):
                    # cprint("BLUE", "POST check remove tag[data_tag]: {}".format(tag))
                    if tag in list(request.form[membership].split(',')):
                        cprint("PURPLE", "check [delete] tag: {} --- false".format(tag))
                    else:
                        getattr(values, membership).remove(Model_mmbr.query.filter(Model_mmbr.name == tag).first())
                        cprint("RED", "check [delete] tag: {} --- True. Will be deleted".format(tag))

                db.session.add(values)
                db.session.commit()

        for column in columns:
            if column != 'id' and request.form[column] != '':
                if column == 'passsword' and Model == User:
                    cprint("BLUE", "column: {} password: {}".format(column, str(request.form[column])))
                    if 'pbkdf2:sha256' not in str(request.form[column]):
                        # cprint("BLUE", "column: {} pkey: {}".format(column, request.form[column]))
                        pvalue = generate_password_hash(str(request.form[column]))
                        data.update({column: pvalue})
                elif column == 'active' and Model == User:
                    # cprint("BLUE", "active is: {}".format(str(request.form[column])))
                    if str(request.form[column]).capitalize() == 'True':
                        data.update({column: True})
                    else:
                        data.update({column: False})

                else:
                    cprint("GREEN", "POST elemnet: {}".format(request.form[column]))
                    data.update({column: request.form[column]})

        try:
            Model.query.filter(Model.id == id).update(data)
            # cprint("PURPLE", "res: " + str(res))
            db.session.commit()
        except Exception as ex:
            PrintException(err_pth)
            return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

        return jsonify({'status': 'ok'})


# NOTE: Динамические страницы. Создание записи в таблице
@admin_panel.route('/dynamic/<tb_name>/create', methods=['POST', 'GET'])
@login_required
@roles_required('admin', 'user')
def dyn_index(tb_name):
    Model = globals()[tb_name.capitalize()]
    cprint('YELLOW', 'dyn_index REQUEST METHOD: {}'.format(request.method))

    if request.method == 'POST':

        data = {}
        data.clear()

        columns = Model.__table__.columns.keys()
        for column in columns:
            if column != 'id':
                if request.form[column] is not None and request.form[column] != '':
                    data.update({column: request.form[column]})

        row = Model(**data)

        try:
            db.session.add(row)
            db.session.commit()
        except Exception as ex:
            cprint("RED", "Error: Model insert tk db. ex: {}".format(ex))

        return redirect('/admin/dynamic/' + tb_name)

    return jsonify({'status': 'ok'})


# NOTE: Динамические страницы. Удаление строки
@admin_panel.route('/dynamic/<tb_name>/rm/<id>', methods=['POST', 'GET'])
@login_required
@roles_required('admin', 'user')
def dyn_remove(tb_name, id):

    Model = globals()[tb_name.capitalize()]
    cprint('YELLOW', 'dyn_remove REQUEST METHOD: {}'.format(request.method))

    element = Model.query.filter(Model.id == id).first_or_404()

    if request.method == 'GET':
        return jsonify({'status': 'ok', 'id': element.id})
    if request.method == 'POST':

        try:
            # cprint("RED", "REQ: {}".format(request.form.getlist()))
            db.session.delete(element)
            db.session.commit()
        except Exception as ex:
            PrintException(err_pth)
            return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

        return jsonify({'status': 'ok'})


# NOTE: Динамические страницы. Удаление строк
@admin_panel.route('/dynamic/<tb_name>/removemultirow', methods=['POST', 'GET'])
@login_required
@roles_required('admin', 'user')
def dyn_removemrow(tb_name):

    Model = globals()[tb_name.capitalize()]
    cprint('YELLOW', 'dyn_remove REQUEST METHOD: {}'.format(request.method))

    if request.method == 'GET':
        return jsonify({'status': 'ok'})

    if request.method == 'POST':

        # data = request.get_json()
        cprint("GREEN", "dyn_removemrow DATA: {}".format(request.values))
        cprint("CYAN", "dyn_removemrow DATA: {}".format(request.form.getlist('id[]')))
        if request.form.getlist('id[]') is not None:
            cprint("BLUE", "REQUEST: {}".format(isinstance(request.form.getlist('id[]'), list)))
            arr = []
            arr = request.form.getlist('id[]')

            if isinstance(request.form.getlist('id[]'), list):
                for id in arr:
                    cprint("BLUE", "REQUEST: {}".format(id))
                    element = Model.query.filter(Model.id == id).first_or_404()
                    db.session.delete(element)

            else:
                cprint("BLUE", "REQUEST single: {}".format(request.form.getlist('id[]')))
                element = Model.query.filter(Model.id == id).first_or_404()
                db.session.delete(element)

        try:
            # cprint("RED", "REQ: {}".format(request.form))

            db.session.commit()
        except Exception as ex:
            PrintException(err_pth)
            return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

        return jsonify({'status': 'ok'})
