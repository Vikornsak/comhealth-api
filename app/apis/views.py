import pandas as pd
from flask import jsonify

from . import apis
from app import engine


@apis.route('/tests')
def get_tests():
    df = pd.read_sql_table('Test', con=engine)
    return jsonify(df.head().to_dict())