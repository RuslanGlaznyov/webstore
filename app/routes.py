from app import app
from flask import render_template
from app.models import Good

goods_from_db = Good.query.all()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", goods=goods_from_db)

@app.route("/goods/<category>")
def goods(category):
    good_by_category = Good.query.filter_by(category=category)
    return render_template('goods.html', goods=goods_from_db, \
        good_by_category=good_by_category)
