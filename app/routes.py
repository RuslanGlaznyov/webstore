from app import app, admin, db
from flask import render_template, url_for, request, flash, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import Good, Category, User
from sqlalchemy.event import listens_for

from app.admin import GoodView, CategoryView, del_image
from app.forms import LoginForm, RegistrationForm, AddToCartForm

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

@app.route("/goods/<category>/<int:id_good>/<title>")
def content(id_good, title, category):
    form=AddToCartForm
    good = Good.query.filter(Good.id == id_good).first_or_404()
    return render_template('content.html', good=good,form=form )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form=LoginForm()
    #тестовая фича
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None  or  user.password != form.password.data:
            flash('Введен неверный email или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/user-page")
def user_page():
    return render_template('user-page.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, теперь вы зарегистрированный пользователь!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/cart')
def cart():
    if 'cart' not in session or len(session['cart']) == 0:
        return render_template('cart.html', display_cart = {}, isEmty=True, total=0)
    else:
        id_of_goods = session['cart']
        dict_of_goods = {}
        
        total_price = 0
        for id in id_of_goods:
            good = Good.query.get(id)
            total_price += good.price
            if good.id in dict_of_goods:
                dict_of_goods[good.id]['qty'] += 1
            else:
                dict_of_goods[good.id] = {
                    'id':good.id,
                    'qty':1,
                    'title': good.title, 
                    'price':good.price, 
                    'img':good.imgsrc
                    }

        return render_template('cart.html', display_cart=dict_of_goods, total=total_price,isEmty=False)


@app.route('/addtocart', methods = ['POST', 'GET'])
def add_to_cart():
    if request.method == 'POST':
        if 'cart' not in session:
            session['cart'] = []

        form = request.form
        id = int(form.get('good_id'))
        session['cart'].append(id)
        flash('добавили в корзину')
        return redirect(url_for('cart'))

@app.route('/delete_from_cart', methods = ['POST', 'GET'])
def delete_from_cart():
    if request.method == 'POST':
        if 'cart' not in session:
            session['cart'] = []

        form = request.form
        id = int(form.get('good_id'))
        print(id)
        session['cart'].remove(id)
        flash('')
        return redirect(url_for('cart'))

#admin decoretor
listens_for(Good,'after_delete')(del_image)

admin.add_view(GoodView(Good, db.session))
admin.add_view(CategoryView(Category, db.session))
