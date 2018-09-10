import os
import os.path as op
from jinja2 import Markup
from flask_admin import form, expose
from sqlalchemy.event import listens_for

from app.models import Good, Order
from app import db
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
    column_list=('id','title', 'price', 'quantity', 'imgsrc')
    
    column_searchable_list = ['title']
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

class OrderView(ModelView):
    column_list=('id','user', 'user_id','товары')
    
    def goods_formater(view, context, model, name):
        goods_str = ''
        for good in model.goods.all():
            goods_str += good.title + '[' +'id:'+ str(good.id) + ']' + " "

        return Markup('<p>{}</p>'.format(goods_str))

    
    column_formatters = {
       'товары': goods_formater,
    }
   
class UserView(ModelView):
    pass
    # form_ajax_refs ={
    # 'orders': {
    #     'fields': (Order.id,),
    # },
    
    # }
