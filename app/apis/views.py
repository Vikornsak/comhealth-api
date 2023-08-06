import csv
from http import HTTPStatus
from io import StringIO

import arrow as arrow
import pandas as pd
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from . import apis
from flask_restful import Resource
from app.extensions import db
from app.apis.schemas import *


class TokenResource(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = db.session.query(User).filter_by(username=username, password=password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=username)
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


class ServiceListResource(Resource):
    @jwt_required()
    def get(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        start_date = arrow.get(start_date, 'YYYY-MM-DD').date()
        end_date = arrow.get(end_date, 'YYYY-MM-DD').date()
        if start_date and end_date:
            query = db.session.query(Services).filter(Services.ServiceDate.between(start_date, end_date))
            return {'data': services_schema.dumps(query.all())}
        return HTTPStatus.BAD_REQUEST


class ServiceResource(Resource):
    @jwt_required()
    def get(self, service_no=None):
        if service_no:
            service = db.session.query(Services).get_or_404(service_no)
            return service_schema.dump(service)
        return HTTPStatus.BAD_REQUEST


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
