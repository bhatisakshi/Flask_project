import os
from flask import Flask
from .auth import api as auth_ns
from .blog import api as blog_ns
from flask_restx import Api
from .db import init_app, reset_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)
    
    with app.app_context():
        reset_db()

    api = Api(app, title='Blog API', version='1.0', description='A simple Blog API')
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(blog_ns, path='/blog')
   
    return app
