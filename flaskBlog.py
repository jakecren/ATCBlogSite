from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
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
@app.route("/home")
def hello():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Register", form=form)

@app.route("/login")
def login():
    form = RegistrationForm()
    return render_template("login.html", title="Login", form=form)

if __name__ == "__main__":
    app.run(debug=True)