import csv
from io import StringIO

import pandas as pd
from flask import jsonify, Response, request

from . import apis
from app import engine


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
