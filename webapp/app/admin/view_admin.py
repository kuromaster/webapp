from flask import render_template
from app.admin import admin_panel
from config.config import Configuration
from app.models import Post
from app.color_print import cprint


@admin_panel.route('/')
def index():
    posts = Post.query.all()
    return render_template("admin/home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), posts=posts)


@admin_panel.route('/<slug>')
def post_detail(slug):
    cprint("YELLOW", "slug: |{}|".format(slug))
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('admin/post_detail.html', pgname="post_detail", company=Configuration.HTML_TITLE_COMPANY, url_prefix='/{}'.format(admin_panel.name), post=post)
