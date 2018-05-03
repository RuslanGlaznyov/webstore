from app import app, admin, db
from flask import render_template, url_for, request
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
    page = request.args.get('page', 1, type=int)

    category_from_db = Category.query.filter(Category.category == category).first()
    goods_by_category = category_from_db.goods.paginate(
    page, app.config['GOOD_PER_PAGE'], False)

    next_url = url_for('.goods', category=category, page=goods_by_category.next_num) \
        if goods_by_category.has_next else None
    
    prev_url = url_for('.goods', category=category, page=goods_by_category.prev_num) \
        if goods_by_category.has_prev else None

    return render_template('goods.html', goods_by_category=goods_by_category.items, \
        categories=categories, prev_url=prev_url, next_url=next_url, pages=goods_by_category, \
        category=category)

@app.route("/goods/<int:id_good>")
def content(id_good):
    good = Good.query.filter(Good.id == id_good).first()
    return render_template('content.html', good=good)

#gamnocode (((
listens_for(Good,'after_delete')(del_image)

admin.add_view(GoodView(Good, db.session))
admin.add_view(CategoryView(Category, db.session))

