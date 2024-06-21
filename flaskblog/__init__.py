import os
from flask import Flask
from .auth import api as auth_ns
from .blog import api as blog_ns
from flask_restx import Api
from .db import init_app, reset_db


def create_app(test_config=None):
    """
    Create Flask app.
    
    test_config : Configuration dictionary.

    Returns:
    Flask app: Configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',                                 #default secret key
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',     #use in-memory database
        SQLALCHEMY_TRACK_MODIFICATIONS=False,             #disable sqlalchemy modification
    )

    if test_config is None:
        #load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the testing config if passed in
        app.config.from_mapping(test_config)

    try:
        #ensure the instance folder exists
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #initialize database with app context
    init_app(app)
    
    with app.app_context():
        reset_db()        #reset database(for testing purpose)

    #Initialze flask-restx API
    api = Api(app, title='Blog API', version='1.0', description='A simple Blog API')

    #add namespaces for respective APIs
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(blog_ns, path='/blog')
   
    return app
