import os
# from flask import Flask
# from dotenv import load_dotenv
# from sqlalchemy.ext.automap import automap_base
# from flasgger import Swagger
# from app.extensions import db, ma, api, jwt
# from app.apis import apis as api_blueprint
# from app.apis.views import *

import os
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy.ext.automap import automap_base
from app.extensions import db, ma, api, jwt
from flasgger import Swagger







def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    Swagger(app)

    return app


load_dotenv()


app = create_app()
with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)

from app.apis.views import *
from app.apis import apis as api_blueprint

api.init_app(api_blueprint)
api.add_resource(TokenResource, '/token')
api.add_resource(CustomerServices, '/customers')
    # api.add_resource(CustomerResource, '/customers/<int:cms_code>')
    # api.add_resource(ServiceListResource, '/services')
    # api.add_resource(ServiceResource, '/services/<service_no>')

api.add_resource(PersonalHealthResultDump, '/PersonalHealthServicesDump/')
api.add_resource(PersonalHealthServices, '/PersonalHealthServices/')

app.register_blueprint(api_blueprint)





