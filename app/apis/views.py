from . import apis
from app import engine

@apis.route('/tests')
def get_tests():
    return 'hello, world'