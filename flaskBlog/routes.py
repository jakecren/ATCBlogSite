from flask import render_template, url_for, flash, redirect
from flaskBlog import app
from flaskBlog.forms import LoginForm, RegistrationForm
from flaskBlog.models import User, Post

posts = [
    {
        "author": "Jake Rennie",
        "title": "First Blog Post",
        "content": "This is the first ever post for my test site!",
        "datePosted": "July 14, 2019"
    },
    {
        "author": "siteBot",
        "title": "System Trial",
        "content": "Routine System Check",
        "datePosted": "July 14, 2019"
    }
]

@app.route("/")
def home():
    return render_template("home.html", posts=posts)


@app.route("/aboutpage")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful.  Please check username and password!", "danger")
    return render_template("login.html", title="Login", form=form)