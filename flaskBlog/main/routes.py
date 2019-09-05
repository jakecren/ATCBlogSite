from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from flaskBlog.models import Post

main = Blueprint("main", __name__)


########  Splash  ########
@main.route("/")
def splash():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("splash.html", title="ATC Blog")


########  Home  ########
@main.route("/home")
@login_required
def home():
    page = request.args.get("page", 1, type=int)
    homePosts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
    posts = Post.query.all()
    return render_template("home.html", title="ATC Blog", homePosts=homePosts, posts=posts)



########  About  ########
@main.route("/about")
def about():
    posts = Post.query.all()
    if current_user.is_authenticated:
        userLoggedIn = True
    else:
        userLoggedIn = False
    return render_template("about.html", title="About", posts=posts, userLoggedIn=userLoggedIn)
