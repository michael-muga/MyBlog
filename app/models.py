from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    blog = db.relationship("Blog", backref="user", lazy="dynamic")
    comment = db.relationship("Comment", backref="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash= generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    """
    List of blogs in each category 
    """
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String)
    blog_content = db.Column(db.String)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment = db.relationship('Comment', backref='blog', lazy="dynamic")


    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.filter_by(user_id = id).order_by(Blog.posted_at.desc()).all()
        return blogs

    @classmethod
    def getBlogId(cls, id):
        blog = Blog.query.filter_by(id=id).first()
        return blog

    @classmethod
    def get_all_blogs(cls):
        return Blog.query.order_by(Blog.posted_at).all()

class Comment(db.Model):
    """
    User comment model for each blog 
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def getCommentId(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        return comment

    @classmethod
    def get_comments(self, id):
        comment = Comment.query.order_by(
            Comment.comment_date.desc()).filter_by(blog_id=id).all()
        return comment

class Quote:
    """
    Class for creating our random quotes.
    """
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote