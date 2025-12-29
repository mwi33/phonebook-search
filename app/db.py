import sqlite3
from typing import Optional

from flask import current_app, g
from flask.cli import with_appcontext
import click

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        db_path = current_app.config["DATABASE_PATH"]
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db(e: Optional[BaseException] = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()

@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    click.echo("Initialized database schema (if not already present).")

def init_app(app) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
