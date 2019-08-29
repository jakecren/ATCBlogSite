import os
import secrets
from PIL import Image
from flask import url_for, current_app
from sendgrid.helpers.mail import Mail
from flaskBlog import SGmail
from datetime import datetime


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Mail(subject="Password Reset",
        from_email="noreply@atcblog.com",
        to_emails=[user.email],
        plain_text_content = f'''To reset your password, visit the following link:
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request, please simply ignore this email and no changes will be made.
    ''')
    SGmail.send(msg)


def usersLoggedIn(uname, uid, admin):
    currentDT = datetime.utcnow().strftime("%Y-%m-%d | %H:%M:%S (UTC)")
    if admin:
        adminTF = "(ADMIN)"
    else:
        adminTF = ""
    LogFile = open("flaskBlog/userLogFile.txt", "a")
    LogFile.write(f"~ {currentDT} = login: {uname}({uid}) {adminTF}\n")
    LogFile.close()
