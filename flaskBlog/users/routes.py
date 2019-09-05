from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flaskBlog import db, bcrypt
from flaskBlog.models import User, Post
from flaskBlog.users.forms import RegistrationForm, RegistrationMultiForm, RegistrationMultiBACKENDForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, UpdateAccountFormAdmin
from flaskBlog.users.utils import save_picture, send_reset_email, usersLoggedIn
import csv
from werkzeug.utils import secure_filename
import os


users = Blueprint("users", __name__)


########  Login  ########
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        user = User.query.filter_by(email=str(form.email.data).lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            usersLoggedIn(user.username, user.id, user.administrator)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful.  Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form, posts=posts)


########  Register  ########
@users.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if current_user.administrator != 1:
        abort(403)
    form = RegistrationForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=str(form.username.data).lower(), email=str(form.email.data).lower(), password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        usersLoggedIn(user.username, user.id, user.administrator)
        flash("Account created!  Please finish setting up user details when ready.", "success")
        return redirect(url_for("users.admin"))
    return render_template("register.html", title="Register User", form=form, posts=posts)


########  Register Multiple Users  ########
@users.route("/registermulti", methods=["GET", "POST"])
@login_required
def registerMulti():
    if current_user.administrator != 1:
        abort(403)
    form = RegistrationMultiForm()
    backval = RegistrationMultiBACKENDForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        usersFileFN = secure_filename(form.csvFile.data.filename)
        usersFile = form.csvFile.data
        usersFile.save(os.path.join(current_app.root_path, "temp/", usersFileFN))

        with open(f"flaskBlog/temp/{usersFileFN}") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                backval.username.data = row[0]
                backval.forename.data = row[1]
                backval.surname.data = row[2]
                backval.email.data = row[3]
                backval.password.data = row[4]

                if backval.validate():
                    hashedPwd = bcrypt.generate_password_hash(row[4]).decode("utf-8")
                    newUser = User(username=str(row[0]).lower(), forename=row[1], surname=row[2], email=str(row[3]).lower(), password=hashedPwd)
                    db.session.add(newUser)
                    line_count += 1
                else:
                    db.session.flush()
                    flash(f"Multiple User Creation Failed.  Record with username: '{row[0]}' does not follow the proper registration criteria.", "danger")
                    os.remove(f"flaskBlog/temp/{usersFileFN}")
                    return redirect(url_for("users.admin"))

        os.remove(f"flaskBlog/temp/{usersFileFN}")
        db.session.commit()
        flash(f"Succesfully Added {line_count} Users!", "success")

        return redirect(url_for("users.admin"))
    return render_template("registerMulti.html", title="Register Users", form=form, posts=posts)


########  Account  ########
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = str(form.username.data).lower()
        current_user.email = str(form.email.data).lower()
        current_user.forename = form.forename.data
        current_user.surname = form.surname.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.forename.data = current_user.forename
        form.surname.data = current_user.surname
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form, posts=posts)


########  Reset Password: Request  ########
@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    posts = Post.query.all()
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions on your password reset", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form, posts=posts)


########  Reset Password: GET Token  ########
@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    posts = Post.query.all()
    user = User.verify_reset_token(token)
    if not user:
        flash("Error: Invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashedPassword
        db.session.commit()
        login_user(user)
        usersLoggedIn(user.username, user.id, user.administrator)
        flash(f"Password Updated!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form, posts=posts)


########  Logout  ########
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.splash"))


########  Admin  ########
@users.route("/admin/", methods=["GET"])
@login_required
def admin():
    if current_user.administrator != 1:
        return redirect(url_for("main.home"))
    posts = Post.query.all()
    noSidebar = False
    users = User.query.filter(User.username != current_user.username)
    return render_template("admin.html", title="Administration", users=users, posts=posts, userE=None, userD=None)


########  Admin - Edit  ########
@users.route("/admin/e<int:userToEdit>", methods=["GET", "POST"])
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
        userE.username = str(form.username.data).lower()
        userE.email = str(form.email.data).lower()
        userE.forename = form.forename.data
        userE.surname = form.surname.data
        if form.admin.data == True:
            userE.administrator = 1
        else:
            userE.administrator = 0
        db.session.commit()
        flash("Account Successfully Updated!", "success")
        return redirect(url_for("users.admin"))
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
@users.route("/admin/d<int:userToDelete>")
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
@users.route("/admin/<int:userToDelete>/delete", methods=["POST"])
@login_required
def DELETEUSER(userToDelete):
    if current_user.administrator != 1:
        abort(403)
    userD = User.query.get_or_404(userToDelete)
    userDPosts = Post.query.filter_by(author=userD)
    for post in userDPosts:
        db.session.delete(post)
    db.session.delete(userD)
    db.session.commit()
    flash(f"User {userD.username} and any posts made by them have been removed!", "success")
    return redirect(url_for("users.admin"))


######## Admin - View Login Log.txt File ########
@users.route("/admin/ulf")
@login_required
def userLogFile():
    if current_user.administrator != 1:
        abort(403)
    with open("flaskBlog/userLogFile.txt", "r") as f:
        content = f.read()
    return render_template("userLog.html", title="Administration", content=content)