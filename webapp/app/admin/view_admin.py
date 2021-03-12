from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from app.admin import admin_panel
from config.config import Configuration
from app.models import Post, Tag
from app.color_print import cprint
from app.admin.forms import PostForm
from app import db


# @admin_panel.route('/create', methods=['POST', 'GET'])
# def create_post():
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
#     # form = PostForm()
#     return render_template('admin/create_post.html', pgname="Create post", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name))


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
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        # posts = Post.query.all()
        posts = Post.query.order_by(Post.created.desc())

    return render_template("admin/home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), posts=posts, form=form)


@admin_panel.route('/post/<slug>')
def post_detail(slug):
    cprint("YELLOW", "slug: |{}|".format(slug))
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('admin/post_detail.html', pgname="post_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), post=post, tags=tags)


@admin_panel.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts.all()
    return render_template('admin/tag_detail.html', pgname="tag_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), posts=posts, tag=tag)
