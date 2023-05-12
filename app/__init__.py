import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

from sqlalchemy.engine import Engine
from sqlalchemy import event

from app.inject_data import populate_db

# Logging configuration
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)


# app and db configuration
app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)
db.create_all()


# inject_data command
@app.cli.command("inject-data")
def inject_data():
    populate_db(db)


# fab recommendation
# Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


from . import views
