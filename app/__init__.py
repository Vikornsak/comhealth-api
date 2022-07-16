import os

from flask import Flask
from waitress import serve
from dotenv import load_dotenv
from sqlalchemy.ext.automap import automap_base
from app.extensions import db, ma


# engine = create_engine('mssql+pyodbc://10.4.101.16/cmsLIS?driver=SQL+Server+Native+Client+11.0')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    db.init_app(app)
    ma.init_app(app)
    return app


load_dotenv()
app = create_app()
with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)

from app.apis import apis

app.register_blueprint(apis, url_prefix='/apis')
