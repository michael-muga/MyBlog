from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired
from ..models import User

class BlogForm(FlaskForm):
    """
    form for creating a blog
    """
    blog_title = StringField('Title', validators=[DataRequired()])
    blog_content = TextAreaField("Blog:", validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """
        form for creating a blog comment
    """
    comment = TextAreaField('Leave a comment')
    submit = SubmitField('SUBMIT')

class UpdateBlogForm(FlaskForm):
    blog_title = StringField("Title", validators=[DataRequired()])
    blog_content = TextAreaField("Type Updates", validators=[DataRequired()])
    submit = SubmitField("Update")


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')
