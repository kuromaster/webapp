from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
# import json
from flask_admin import AdminIndexView, expose


# from app.admin import admin_panel
from config.config import Configuration
from app.models import Post, Tag
from app.color_print import cprint, PrintException
from app.admin.forms import PostForm
from app import db


err_pth = Configuration.ERR_PTH


class MyHomeView(AdminIndexView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
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
            posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))  # .all()
        else:
            # posts = Post.query.all()
            posts = Post.query.order_by(Post.created.desc())

        pages = posts.paginate(page=page, per_page=7)

        return render_template("admin/home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format('admin'), form=form, pages=pages)

    @expose('/post/<slug>')
    def post_detail(self, slug):
        cprint("YELLOW", "slug: |{}|".format(slug))
        post = Post.query.filter(Post.slug == slug).first_or_404()
        tags = post.tags
        return render_template('admin/post_detail.html', pgname="post_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format('admin'), post=post, tags=tags)

    @expose('/post/<slug>/edit', methods=['POST', 'GET'])
    def post_edit(self, slug):
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

    @expose('/post/<slug>/rm', methods=['POST', 'GET'])
    def post_remove(self, slug):
        cprint('YELLOW', 'REQUEST METHOD: {}'.format(request.method))
        post = Post.query.filter(Post.slug == slug).first_or_404()
        if request.method == 'GET':
            return jsonify({'status': 'ok', 'title': post.title, 'id': post.id})
        if request.method == 'POST':

            try:
                cprint("RED", "REQ: {}".format(request.form))
                db.session.delete(post)
                # form = PostForm(formdata=request.form, obj=post)
                # form.populate_obj(post)
                db.session.commit()
            except Exception as ex:
                PrintException(err_pth)
                return jsonify({'status': '[PYTHON] error: {}'.format(ex)})

            return jsonify({'status': 'ok'})

    @expose('/tag/<slug>')
    def tag_detail(self, slug):
        tag = Tag.query.filter(Tag.slug == slug).first_or_404()
        posts = tag.posts.all()
        return render_template('admin/tag_detail.html', pgname="tag_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format('admin'), posts=posts, tag=tag)


#
#
#
# @admin_panel.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#
#         try:
#             post = Post(title=title, body=body)
#             db.session.add(post)
#             db.session.commit()
#         except Exception as ex:
#             cprint("RED", "Error: Post insert tk db. ex: {}".format(ex))
#
#         return redirect(url_for('admin.index'))
#
#     form = PostForm()
#     q = request.args.get('q')
#
#     page = request.args.get('page')
#     if page and page.isdigit():
#         page = int(page)
#     else:
#         page = 1
#
#     if q:
#         posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))  # .all()
#     else:
#         # posts = Post.query.all()
#         posts = Post.query.order_by(Post.created.desc())
#
#     pages = posts.paginate(page=page, per_page=7)
#
#     # print(posts.paginate)
#     # for i in dir(pages):
#     #     cprint("GREEN", "{}".format(i))
#     #
#     # cprint("YELLOW", pages.per_page)
#     # cprint("PURPLE", pages.total)
#     # for post in pages.items:
#     #     cprint("GREEN", "pages: {}".format(post.body))
#
#     return render_template("admin/home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), form=form, pages=pages)
#
#
# @admin_panel.route('/post/<slug>')
# def post_detail(slug):
#     cprint("YELLOW", "slug: |{}|".format(slug))
#     post = Post.query.filter(Post.slug == slug).first_or_404()
#     tags = post.tags
#     return render_template('admin/post_detail.html', pgname="post_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), post=post, tags=tags)
#
#
# @admin_panel.route('/post/<slug>/edit', methods=['POST', 'GET'])
# def post_edit(slug):
#     cprint('YELLOW', 'REQUEST METHOD: {}'.format(request.method))
#     post = Post.query.filter(Post.slug == slug).first_or_404()
#     if request.method == 'GET':
#         return jsonify({'status': 'ok', 'title': post.title, 'body': post.body})
#     if request.method == 'POST':
#
#         try:
#             form = PostForm(formdata=request.form, obj=post)
#             form.populate_obj(post)
#             db.session.commit()
#         except Exception as ex:
#             PrintException(err_pth)
#             return jsonify({'status': '[PYTHON] error: {}'.format(ex)})
#
#         return jsonify({'status': 'ok'})
#
#
# @admin_panel.route('/post/<slug>/rm', methods=['POST', 'GET'])
# def post_remove(slug):
#     cprint('YELLOW', 'REQUEST METHOD: {}'.format(request.method))
#     post = Post.query.filter(Post.slug == slug).first_or_404()
#     if request.method == 'GET':
#         return jsonify({'status': 'ok', 'title': post.title, 'id': post.id})
#     if request.method == 'POST':
#
#         try:
#             cprint("RED", "REQ: {}".format(request.form))
#             db.session.delete(post)
#             # form = PostForm(formdata=request.form, obj=post)
#             # form.populate_obj(post)
#             db.session.commit()
#         except Exception as ex:
#             PrintException(err_pth)
#             return jsonify({'status': '[PYTHON] error: {}'.format(ex)})
#
#         return jsonify({'status': 'ok'})
#
#
# @admin_panel.route('/tag/<slug>')
# def tag_detail(slug):
#     tag = Tag.query.filter(Tag.slug == slug).first_or_404()
#     posts = tag.posts.all()
#     return render_template('admin/tag_detail.html', pgname="tag_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), posts=posts, tag=tag)
