from app import app
from flask import render_template
from app.models import Good, Category

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
