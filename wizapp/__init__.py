import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from wizapp.config import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from wizapp.users.routes import users
    from wizapp.posts.routes import posts
    from wizapp.admin.routes import admin
    from wizapp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(main)

    return app
