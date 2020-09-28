import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
        Connect to sqlite3 database.

        :Returns: 
            - db (connection): Connection with database

        :author: sarareginaff       
        :creation: Sep/2020
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
        Close connction with sqlite3 database.

        :author: sarareginaff       
        :creation: Sep/2020
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
        Initialize database with schema.sql

        :author: sarareginaff       
        :creation: Sep/2020
    """
    db = get_db()

    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
        Initialize database

        :author: sarareginaff       
        :creation: Sep/2020
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
        Set close_db as teardown_appcontext and set init_db as cli command

        :author: sarareginaff       
        :creation: Sep/2020
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
