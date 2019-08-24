from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskBlog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password", validators=[
                                    DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username is unavailable, please choose a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Email is unavailable, please choose a different username.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    forename = StringField("First Name", validators=[Length(max=50)])
    surname = StringField("Last Name", validators=[Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[
                        FileAllowed(["jpg", "png"])])
    admin = BooleanField("Administrator")
    submit = SubmitField("Update Details")

    def validate_username(self, username):
        if not username.data == current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username is unavailable, please choose a different username.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email is unavailable, please choose a different username.")


class UpdateAccountFormAdmin(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    forename = StringField("First Name", validators=[Length(max=50)])
    surname = StringField("Last Name", validators=[Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[
                        FileAllowed(["jpg", "png"])])
    admin = BooleanField("Administrator")
    submit = SubmitField("Update Details")

    def validate_username(self, username):
        if not username.data == self.userE.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username is unavailable, please choose a different username.")

    def validate_email(self, email):
        if email.data != self.userE.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email is unavailable, please choose a different username.")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
