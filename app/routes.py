from app import app
from flask import render_template
from app.models import Good

goods_from_db = Good.query.all()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/goods")
def goods():
    return render_template('goods.html', goods=goods_from_db)

