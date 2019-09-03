import os

class Config():
    SECRET_KEY = os.environ.get("ATCBlogSite_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("ATCBlogSite_SQLALCHEMY_DATABASE_URI")
    MAIL_USERNAME = os.environ.get("ATCBlogSite_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("ATCBlogSite_MAIL_PASSWORD")