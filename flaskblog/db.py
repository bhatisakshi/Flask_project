from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db():
    """
    Initialize database by creating tables
    """
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
     """
    CLI command to initialize the database

    This command will be available in the Flask CLI as 'init-db'
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """
    Flask application instance.
    Initialize the Flask application with the database.
    """
    db.init_app(app)
    # app.cli.add_command(init_db_command)

def reset_db():
    """
    Reset the database by dropping all tables and recreating them.
    """
    with current_app.app_context():
        db.drop_all()
        db.create_all()
