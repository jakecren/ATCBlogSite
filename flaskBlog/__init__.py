from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "6441b3dbdb388ba0de5c36ebe93a32e1"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

