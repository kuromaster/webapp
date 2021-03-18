from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from datetime import datetime
import json
from app.admin import admin_panel, menu
from config.config import Configuration
from app.admin.models import Post, Tag
from app.color_print import cprint, PrintException
from app.admin.forms import PostForm
from app import db


err_pth = Configuration.ERR_PTH


@admin_panel.route('/', methods=['POST', 'GET'])
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

    return render_template("admin/home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), form=form, pages=pages, menu=menu.get_menu())


@admin_panel.route('/post/<slug>')
def post_detail(slug):
    cprint("YELLOW", "slug: |{}|".format(slug))
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    return render_template('admin/post_detail.html', pgname="post_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), post=post, tags=tags)


@admin_panel.route('/post/<slug>/edit', methods=['POST', 'GET'])
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


@admin_panel.route('/post/<slug>/rm', methods=['POST', 'GET'])
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


@admin_panel.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template('admin/tag_detail.html', pgname="tag_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), posts=posts, tag=tag)


@admin_panel.route('/dynamic/<tb_name>/edit/<id>', methods=['POST', 'GET'])
def dyn_edit(tb_name, id):
    cprint('YELLOW', 'dyn_edit REQUEST METHOD: {}'.format(request.method))

    Model = globals()[tb_name.capitalize()]
    columns = Model.__table__.columns.keys()
    values = Model.query.filter(Model.id == id).first_or_404()

    data = {}
    data.clear()

    if request.method == 'GET':

        for column in columns:
            data.update({column: getattr(values, column)})

        data.update({'status': 'ok'})
        return jsonify(data)

    if request.method == 'POST':

        for column in columns:
            if column != 'id':
                if isinstance(request.form[column], datetime):
                    cprint("GREEN", "date: {}, date2: {}".format(request.form[column], request.form[column].strftime("%Y-%m-d %H:%M:%S")))
                data.update({column: request.form[column]})

        try:
            Model.query.filter(Model.id == id).update(data)
            # cprint("PURPLE", "res: " + str(res))
            db.session.commit()
        except Exception as ex:
            PrintException(err_pth)
            return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

        return jsonify({'status': 'ok'})


@admin_panel.route('/dynamic/<tb_name>/create', methods=['POST', 'GET'])
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


@admin_panel.route('/dynamic/<tb_name>/rm/<id>', methods=['POST', 'GET'])
def dyn_remove(tb_name, id):

    Model = globals()[tb_name.capitalize()]
    cprint('YELLOW', 'dyn_remove REQUEST METHOD: {}'.format(request.method))

    element = Model.query.filter(Model.id == id).first_or_404()

    if request.method == 'GET':
        return jsonify({'status': 'ok', 'id': element.id})
    if request.method == 'POST':

        try:
            cprint("RED", "REQ: {}".format(request.form.getlist()))
            db.session.delete(element)
            db.session.commit()
        except Exception as ex:
            PrintException(err_pth)
            return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

        return jsonify({'status': 'ok'})


@admin_panel.route('/dynamic/<tb_name>/removemultirow', methods=['POST', 'GET'])
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
