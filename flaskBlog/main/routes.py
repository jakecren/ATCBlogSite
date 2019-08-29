from flask import render_template, request, Blueprint
from flaskBlog.models import Post

main = Blueprint("main", __name__)


########  Home  ########
@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    homePosts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
    posts = Post.query.all()
    return render_template("home.html", title="ATC Blog", homePosts=homePosts, posts=posts)


########  About  ########
@main.route("/about")
def about():
    posts = Post.query.all()
    return render_template("about.html", title="About", posts=posts)
