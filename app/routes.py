from app import app, admin, db
from flask import render_template
from app.models import Good, Category

from sqlalchemy.event import listens_for

from app.admin import GoodView, CategoryView, del_image

categories = Category.query.all()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", categories=categories)

@app.route("/goods/<category>")
def goods(category):
    category_from_db = Category.query.filter(Category.category == category).first()
    goods_by_category = category_from_db.goods.all()

    return render_template('goods.html', goods_by_category=goods_by_category, \
        categories=categories)

 
#gamnocode (((
listens_for(Good,'after_delete')(del_image)

admin.add_view(GoodView(Good, db.session))
admin.add_view(CategoryView(Category, db.session))

