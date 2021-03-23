from app import db
from datetime import datetime
from slugify import slugify
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash


tag_membership = db.Table(

    'tag_membership',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))

)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag', secondary=tag_membership, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = '{}-{}'.format(slugify(self.title), str(datetime.now().timestamp()))

    def __repr__(self):
        return 'id: {}, title: {}, tags: {}\n'.format(self.id, self.title, self.tags)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = '{}-{}'.format(slugify(self.name), str(datetime.now().timestamp()))

    def __repr__(self):
        return 'id: {}, name: {}, slug: {}'.format(self.id, self.name, self.slug)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    lastname = db.Column(db.String(100))
    name = db.Column(db.String(30))
    issuenum = db.Column(db.Integer, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40))
    deliverydate = db.Column(db.DateTime)
    message = db.Column(db.Text)
    isEnabled = db.Column(db.String(6), nullable=False, server_default=u'No')
    status = db.Column(db.String(100))
    lastMessageId = db.Column(db.Integer)
    lastsenddate = db.Column(db.DateTime)
    # tags = db.Column(db.String(50))

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)


role_membership = db.Table(

    'role_membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))

)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    lastname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    # login = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))  # Password
    created = db.Column(db.DateTime, default=datetime.now)
    active = db.Column(db.Boolean(), default=True)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    login_count = db.Column(db.Integer)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    picture_url = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=role_membership, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        # self.encrypt_pkey()

    def encrypt_pkey(self):
        if self.password:
            self.password = generate_password_hash(self.password)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), unique=True)
    slug = db.Column(db.String(100))
    description = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = '{}-{}'.format(slugify(self.name), str(datetime.now().timestamp()))
