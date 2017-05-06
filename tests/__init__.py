from service import create_app, app
from .test_apartment_api import test_apartment_api

if __name__ == '__main__':
    test_apartment_api(app)
