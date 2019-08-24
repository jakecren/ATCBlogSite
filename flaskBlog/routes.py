import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskBlog import app, db, bcrypt
from flaskBlog.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, UpdateAccountFormAdmin
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


########  Home  ########
@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", title="ATC Blog", posts=posts)


########  About  ########
@app.route("/about")
def about():
    posts = Post.query.all()
    return render_template("about.html", title="About", posts=posts)


########  Login  ########
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful.  Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form, posts=posts)


########  Register  ########
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Account created!  Please finish setting up your details in the 'Account' tab above.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form, posts=posts)


########  Account  ########
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.forename = form.forename.data
        current_user.surname = form.surname.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.forename.data = current_user.forename
        form.surname.data = current_user.surname
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form, posts=posts)


########  Logout  ########
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


########  Admin  ########
@app.route("/admin/", methods=["GET"])
@login_required
def admin():
    if current_user.administrator != 1:
        return redirect(url_for("home"))
    posts = Post.query.all()
    noSidebar = False
    users = User.query.filter(User.username != current_user.username)
    return render_template("admin.html", title="Administration", users=users, posts=posts, userE=None, userD=None)


########  Admin - Edit  ########
@app.route("/admin/e<int:userToEdit>", methods=["GET", "POST"])
@login_required
def editUser(userToEdit):
    if current_user.administrator != 1:
        abort(403)
    posts = Post.query.all()
    userE = User.query.get_or_404(userToEdit)
    userD = None
    noSidebar = False
    users = User.query.filter(User.username != current_user.username)
    form = UpdateAccountFormAdmin()
    form.userE = userE

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            userE.image_file = picture_file
        userE.username = form.username.data
        userE.email = form.email.data
        userE.forename = form.forename.data
        userE.surname = form.surname.data
        if form.admin.data == True:
            userE.administrator = 1
        db.session.commit()
        flash("Account Successfully Updated!", "success")
        return redirect(url_for("admin"))
    elif request.method == "GET":
        form.username.data = userE.username
        form.forename.data = userE.forename
        form.surname.data = userE.surname
        form.email.data = userE.email
        if userE.administrator == 1:
            form.admin.data = True
        else:
            form.admin.data = False
    image_file = url_for(
        "static", filename="profile_pics/" + userE.image_file)

    return render_template("admin.html", title="Administration", users=users, posts=posts, image_file=image_file, userE=userE, userD=userD, form=form)


########  Admin - Delete  ########
@app.route("/admin/d<int:userToDelete>")
@login_required
def deleteUser(userToDelete):
    if current_user.administrator != 1:
        abort(403)
    posts = Post.query.all()
    userD = User.query.get_or_404(userToDelete)
    userE = None
    noSidebar = False
    users = User.query.filter(User.username != current_user.username)
    return render_template("admin.html", title="Administration", users=users, posts=posts, userD=userD, userE=userE)


########  Admin - Delete: BACKEND  ########
@app.route("/admin/<int:userToDelete>/delete", methods=["POST"])
@login_required
def DELETEUSER(userToDelete):
    if current_user.administrator != 1:
        abort(403)
    userD = User.query.get_or_404(userToDelete)
    db.session.delete(userD)
    db.session.commit()
    flash(f"User {userD.username} has been removed!", "success")
    return redirect(url_for("admin"))


########  Post  ########
@app.route("/post/<int:post_id>")
def post(post_id):
    posts = Post.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post, legend="New Post", posts=posts)


########  Post - New  ########
@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form, posts=posts)


########  Post - Update  ########
@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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
            return redirect(url_for("home"))
        elif request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
        return render_template("create_post.html", title="Update Post", form=form, posts=posts, legend="Update Post")
    else:
        abort(403)


########  Post - Delete: BACKEND
@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))
