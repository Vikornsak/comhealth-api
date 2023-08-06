import os

from flask import Flask
from waitress import serve
from dotenv import load_dotenv
from sqlalchemy.ext.automap import automap_base
from app.extensions import db, ma, api, jwt


# engine = create_engine('mssql+pyodbc://10.4.101.16/cmsLIS?driver=SQL+Server+Native+Client+11.0')



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    return app


load_dotenv()
app = create_app()
with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)

from app.apis import apis as api_blueprint
from app.apis.views import *

api.init_app(api_blueprint)
api.add_resource(TokenResource, '/token')
api.add_resource(CustomerListResource, '/customers')
api.add_resource(CustomerResource, '/customers/<int:cms_code>')
api.add_resource(ServiceResource, '/services/<int:service_no>')
api.add_resource(TestListResource, '/tests')
app.register_blueprint(api_blueprint)
