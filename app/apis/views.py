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

from datetime import datetime, timedelta  # BY THON

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



# Update 02/08/67
@apis.route('/customers-by-month', methods=['GET'])
def get_customers_by_month():

    default_start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    start_date = request.args.get('start_date', default_start_date)  # ค่าเริ่มต้นคือ "วันที่ปัจจุบัน ย้อนหลัง 10 ปี" ถ้าไม่ได้ระบุพารามิเตอร์
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))  # ค่าเริ่มต้นคือวันที่ปัจจุบัน ถ้าไม่ได้ระบุพารามิเตอร์

    query = f"""
    SELECT COUNT(*) AS 'NumberCustomer', ServiceDate 
    FROM Services 
    WHERE ServiceDate BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY ServiceDate;
    """
    df = pd.read_sql_query(query, con=db.engine)
    return jsonify(df.to_dict(orient='records')) # Ref https://thon.me/2024/08/02/python-df-to_dictorientrecords-vs-df-to_dict/
    # Using
    # Request all parameters ->  http://127.0.0.1:8080/api/v1.0/customers-by-month?start_date=2020-01-01&end_date=2020-12-31
    # Only use start_date ->  http://127.0.0.1:8080/api/v1.0/customers-by-month?start_date=2020-01-01
    # Only use end_date ->  http://127.0.0.1:8080/api/v1.0/customers-by-month?end_date=2019-01-01
    # default start date  (Current date, past 10 years)-> http://127.0.0.1:8080/api/v1.0/customers-by-month



# Update 02/08/67
@apis.route('/customer-result', methods=['GET'])
def get_customer_result():

    mobile = request.args.get('mobile')
    fname = request.args.get('fname')
    lname = request.args.get('lname')

    query = f"""
        SELECT * FROM [cmsLIS_test].[dbo].Employee A
        INNER JOIN [cmsLIS_test].[dbo].[Physical_Exam] B
        ON A.cmsCode = B.cmsCode
        WHERE A.Mobile ='{mobile}' AND A.Fname = '{fname}' AND A.Lname = '{lname}' 
        ORDER BY B.[ServiceDate] DESC;
    """

    df = pd.read_sql_query(query, con=db.engine)
    return jsonify(df.to_dict(orient='records'))

# Using
    # Request all parameters ->  http://127.0.0.1:8080/api/v1.0/customer-result?mobile=081-7551996&fname=กนกวรรณ&lname=กิตตินิยม