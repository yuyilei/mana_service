from service import create_app, app
from .test_mana_api import test_mana_api

if __name__ == '__main__':
    test_mana_api(app)
