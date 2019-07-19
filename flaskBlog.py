from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
app = Flask(__name__)

app.config["SECRET_KEY"] = "6441b3dbdb388ba0de5c36ebe93a32e1"

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


if __name__ == "__main__":
    app.run(debug=True)
