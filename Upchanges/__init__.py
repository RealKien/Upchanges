# To connect all the codes in Upchanges's folder to run the application(app.py)
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, TimedSerializer
# from Upchanges.models import MangagePassword

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

# DATABASE SETUP
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    '../Upchanges/data.sqlite')  # Taking risk by using mysql, maysbe should had use sqlite.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
# app.config.from_object(__name__)



MAIL_USERNAME = 'letrungkien208@gmail.com'
MAIL_PASSWORD = 'bibopyeudau'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# connect_password = MangagePassword.query(1)
# mail_admin_password = connect_password.password
# print(mail_admin_password)         #Need to find a way to safely decrypt my password in a table and let this __init__.py read it and be able to log in to my Gmail account

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

db = SQLAlchemy(app)
Migrate(app, db)

# SET UP LOGIN CONFIGURATION
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

# IMPORTING BLUEPRINTS FROM VIEWS.PY FILE IN OTHER FOLDERS
from Upchanges.core.views import core
from Upchanges.core.vn_views import vn_core
from Upchanges.core.jp_views import jp_core
from Upchanges.core.usa_views import usa_core
from Upchanges.users.views import users
from Upchanges.error_pages.handlers import error_pages
from Upchanges.blog_posts.views import blog_posts
from Upchanges.blog_posts.vn_views import vn_blog_posts
from Upchanges.blog_posts.jp_views import jp_blog_posts
from Upchanges.blog_posts.usa_views import usa_blog_posts
from Upchanges.blog_info.views import blog_info

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(blog_posts)
app.register_blueprint(vn_core)
app.register_blueprint(jp_core)
app.register_blueprint(usa_core)
app.register_blueprint(vn_blog_posts)
app.register_blueprint(jp_blog_posts)
app.register_blueprint(usa_blog_posts)
app.register_blueprint(blog_info)

