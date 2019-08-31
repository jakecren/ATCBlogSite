from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskBlog import db
from flaskBlog.models import Post, User
from flaskBlog.posts.forms import PostForm
from datetime import datetime
import pytz


posts = Blueprint("posts", __name__)

########  Post  ########
@posts.route("/post/<int:post_id>")
def post(post_id):
    posts = Post.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post, legend="New Post", posts=posts)


########  Post: user  ########
@posts.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    homePosts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=8)

    posts = Post.query.all()
    return render_template("user_posts.html", title=user.username, homePosts=homePosts, posts=posts, user=user)


########  Post - New  ########
@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user, date_posted=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Australia/Brisbane")))
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form, posts=posts, legend="New Post")


########  Post - Update  ########
@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    posts = Post.query.all()
    post = Post.query.get_or_404(post_id)
    if post.author == current_user or current_user.administrator == 1:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Your post has been updated!", "success")
            return redirect(url_for("main.home"))
        elif request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
        return render_template("create_post.html", title="Update Post", form=form, posts=posts, legend="Update Post")
    else:
        abort(403)


########  Post - Delete: BACKEND
@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user or current_user.administrator == 1:
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted!", "success")
        return redirect(url_for("main.home"))
    else:
        abort(403)
