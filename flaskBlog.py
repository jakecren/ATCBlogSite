from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)