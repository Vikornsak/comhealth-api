import csv
from http import HTTPStatus
from io import StringIO

import pandas as pd
from flask import jsonify
from flask_jwt_extended import create_access_token

from . import apis
from flask_restful import Resource
from app.extensions import db
from app.apis.schemas import *


class TokenResource(Resource):
    def get(self):
        access_token = create_access_token(identity=17558)
        return {'access_token': access_token}, HTTPStatus.OK


class CustomerListResource(Resource):
    def get(self):
        query = db.session.query(Employee).limit(2)
        return {'data': employees_schema.dumps(query)}


class CustomerResource(Resource):
    def get(self, cms_code):
        employee = db.session.query(Employee).get(cms_code)
        print(employee.services)
        return {'data': employee_schema.dumps(employee)}


class ServiceResource(Resource):
    def get(self, service_no):
        service = db.session.query(Services).get_or_404(service_no)
        return {'data': service_schema.dumps(service)}


class TestListResource(Resource):
    def get(self):
        # test_table = db.Table('Test', db.metadata, autoload=True, autoload_with=db.engine)
        return {'message': 'done', 'data': tests_schema.dumps(db.session.query(Test).all())}


def generate(df):
    data = StringIO()
    w = csv.writer(data)

    # write header
    w.writerows(df.to_csv())
    return data.getvalue()


@apis.route('/tests-by-month')
def get_tests_by_month():
    df = pd.read_sql_query("select ServiceDate,TCode, count(*) as 'Counts' from Lab where ServiceDate>='2022-01-01' group by ServiceDate,TCode order by ServiceDate;",
                           con=db.engine)
    return jsonify(df.to_dict())


@apis.route('/customers-by-month')
def get_customers_by_month():
    df = pd.read_sql_query("select count(*) as 'NumberCustomer', ServiceDate from Services where ServiceDate>='2021-01-01' group by ServiceDate;",
                           con=db.engine)
    return jsonify(df.to_dict())
