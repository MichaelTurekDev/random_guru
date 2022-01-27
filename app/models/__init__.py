'''
Initialize the database which persists a history of visited web pages.
'''
import sqlite3

from pathlib import Path

from app import app


model_path = Path().joinpath('app', 'models').resolve()
ddl_path = model_path.joinpath('ddl.sql')
db_path = model_path.joinpath(f'{app.config["DB_NAME"]}.db')

if not db_path.exists():
    # Initialize database
    with sqlite3.connect(db_path) as conn, open(ddl_path) as f:
        conn.executescript(f.read())
