import os
import os.path as op
from jinja2 import Markup
from flask_admin import form
from sqlalchemy.event import listens_for

from app.models import Good
from flask_admin.contrib.sqla import ModelView
from flask import url_for
from config import img_path

try:
    os.mkdir(img_path)
except OSError:
    pass


def del_image(mapper, connection, target):
    if target.imgsrc:
        # Delete image
        try:
            os.remove(op.join(img_path, target.imgsrc))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(img_path,
                              form.thumbgen_filename(target.imgsrc)))
        except OSError:
            pass


class GoodView(ModelView):
    def _list_thumbnail(view, context, model, title):
        if not model.imgsrc:
            return ''

        return Markup('<img src="{}">'.format(url_for( 'static', filename=form.thumbgen_filename('images/' + model.imgsrc))))
    
    form_columns = ['title', 'desc', 'price', 'quantity', 'imgsrc', 'category']
    
    column_formatters = { 
        'imgsrc': _list_thumbnail 
        }
    
    form_extra_fields = {
        'imgsrc': form.ImageUploadField('Image',
                                      base_path=img_path,
                                      url_relative_path='images/',
                                      thumbnail_size=(100, 100, True),
                                      allowed_extensions=['jpg','png','jpeg'],
                                      )
                                      
    }
    

class CategoryView(ModelView):
    form_columns = ['category']
