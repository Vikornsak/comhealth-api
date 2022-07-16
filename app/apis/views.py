import csv
from io import StringIO

import pandas as pd
from flask import jsonify
from sqlalchemy.orm import relationship

from app import Base
from . import apis
from app.extensions import db
from app.apis.schemas import *


@apis.route('/v1.0/customer/<int:cmsCode>')
def get_customer_profile(cmsCode):
    employee = db.session.query(Employee).get(cmsCode)
    print(employee.services)
    return jsonify({'data': employee_schema.dumps(employee)})


@apis.route('/v1.0/service/<int:service_no>')
def get_service(service_no):
    service = db.session.query(Services).get(service_no)
    return jsonify({'data': service_schema.dumps(service)})


@apis.route('/labs')
def get_labs():
    query = db.session.query(Lab).join(Test, Lab.TCode == Test.TCode).filter(Test.TCode == 'GTT2').limit(1)
    data = labs_schema.dumps(query)
    return jsonify({'data': data})


@apis.route('/tests/reflection')
def get_test_reflection():
    # test_table = db.Table('Test', db.metadata, autoload=True, autoload_with=db.engine)
    return jsonify({'message': 'done', 'data': tests_schema.dumps(db.session.query(Test).all())})



def generate(df):
    data = StringIO()
    w = csv.writer(data)

    # write header
    w.writerows(df.to_csv())
    return data.getvalue()


@apis.route('/tests')
def get_tests():
    df = pd.read_sql_table('Test', con=engine)
    return jsonify(df.to_dict())


@apis.route('/tests-by-month')
def get_tests_by_month():
    df = pd.read_sql_query("select ServiceDate,TCode, count(*) as 'Counts' from Lab where ServiceDate>='2022-01-01' group by ServiceDate,TCode order by ServiceDate;",
                           con=engine)
    return jsonify(df.to_dict())


@apis.route('/customers-by-month')
def get_customers_by_month():
    df = pd.read_sql_query("select count(*) as 'NumberCustomer', ServiceDate from Services where ServiceDate>='2021-01-01' group by ServiceDate;",
                           con=engine)
    return jsonify(df.to_dict())
