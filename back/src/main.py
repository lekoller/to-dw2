import os
from flask import Flask
from flask_migrate import Migrate, upgrade

from repository import base
from dotenv import load_dotenv
from api import api


def create_app(db_url: str, db_name: str) -> Flask:

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url+"/"+db_name

    return app

def migrate_db(app: Flask, db: base.db) -> Migrate:
    return Migrate(app, db)


load_dotenv()

db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

db_url = "postgresql://"+db_user+":"+db_pass+"@"+db_host+":"+db_port

base.create_db(db_url=db_url, db_name=db_name)

app = create_app(db_name=db_name, db_url=db_url)

base.db.init_app(app)
api.start_api(app)

migrate = migrate_db(app, base.db)

with app.app_context():
    upgrade()


if __name__ == '__main__':
    app.run()