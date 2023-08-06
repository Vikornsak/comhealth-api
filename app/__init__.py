from flask import Flask
from sqlalchemy import create_engine

engine = create_engine('mssql+pyodbc://10.4.101.16/cmsLIS?driver=SQL+Server+Native+Client+11.0')


def create_app():
    app = Flask(__name__)
    return app
