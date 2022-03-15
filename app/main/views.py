from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile
from .. import db,photos
from ..request import get_quote
from flask_login import current_user, login_required
from ..models import User, Blog, Comment
from app.main.forms import BlogForm,CommentForm
from datetime import datetime




@main.route("/", methods=["GET", "BLOG"])
def index():
    blogs = Blog.get_all_blogs()
    quote = get_quote()

    return render_template('index.html', blogs = blogs, quote = quote)

@main.route("/blog/new", methods=["POST", "GET"])
@login_required
def new_blog():
    newblogform = BlogForm()
    if newblogform.validate_on_submit():
        blog_title = newblogform.blog_title.data
        newblogform.blog_title.data = ""
        blog_content = newblogform.blog_content.data
        newblogform.blog_content.data = ""
        new_blog = Blog(blog_title=blog_title,
                        blog_content=blog_content,
                        posted_at=datetime.now(),
                        user_id=current_user.id)
        new_blog.save_blog()

        return redirect(url_for(".index", id=new_blog.id))
    return render_template("new_blog.html", newblogform=newblogform)

@main.route("/blog/<int:id>", methods=["POST", "GET"])
@login_required
def write_comment(id):
    blog = Blog.getBlogId(id)
    comment = Comment.get_comments(id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        comment_form.comment.data = ""
        new_comment = Comment(comment=comment,
                              user_id=current_user.id,
                              blog_id=blog.id)
        new_comment.save_comment()
        return redirect(url_for(".write_comment", id=blog.id))

    return render_template("comment.html",
                           comment_form=comment_form,
                           comment=comment,
                           blog=blog)


@main.route("/blog/<int:id>/delete", methods=["POST"])
@login_required
def delete_comment(id):
    comment = Comment.getCommentId(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for(".write_comment", id=comment.id))

@main.route("/blog/<int:id>/delete")
@login_required
def delete_blog(id):
    blog = Blog.getBlogId(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for(".index", id=blog.id))

@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_blog(id):
    blog = Blog.query.get_or_404(id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.blog_title = form.blog_title.data
        blog.blog_content = form.blog_content.data
        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('.index'))
    elif request.method == 'GET':
        form.blog_title.data = blog.blog_title
        form.blog_content.data = blog.blog_content
    return render_template('update.html', blog=blog, form=form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))