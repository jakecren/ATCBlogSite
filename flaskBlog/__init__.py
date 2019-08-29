from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sendgrid import SendGridAPIClient
from flaskBlog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

SGmail = SendGridAPIClient("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")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskBlog.users.routes import users
    from flaskBlog.posts.routes import posts
    from flaskBlog.main.routes import main
    from flaskBlog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

app = create_app()