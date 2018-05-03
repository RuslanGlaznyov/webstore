import os
import os.path as op

folder_img_path = 'app/static/images'
img_path = op.join(op.dirname(__file__), folder_img_path)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY="you will never geas"
    GOOD_PER_PAGE = 9
