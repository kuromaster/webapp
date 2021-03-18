from wtforms import Form, StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.admin.models import Post


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(0, Post.title.type.length)])
    body = TextAreaField('Body')
