from app import db
from datetime import datetime
from slugify import slugify
# import re


# def slugify(s):
#     pattern = r'[^\w+]'
#     return re.sub(pattern, '-', s)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = '{}-{}'.format(slugify(self.title), str(datetime.now().timestamp()))

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag id: {}, name: {}, slug: {}'.format(self.id, self.name, self.slug)


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
    tags = db.Column(db.String(50))

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
