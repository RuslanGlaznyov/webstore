from flask_login import UserMixin
from app import db, login
import re

def slugify(s):
    """ заменяет все символы кроме букв и цифр на '-' """
    pattern = r'[^\w+]'
    slug = re.sub(pattern,"-", s)
    return slug.lower()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), unique=True)
    goods = db.relationship('Good', backref='category',lazy='dynamic')

    def __str__(self):
        return self.category
        
    def __repr__(self):
        return "<id : {}, name_category : {}>".\
                format(self.id ,self.category)        


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128)) #название товара 
    desc = db.Column(db.Text)#описание товара 
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    slug = db.Column(db.String(64)) #ссылка на товар 
    imgsrc =  db.Column(db.String(128))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __init__(self, *args, **kwargs):
        super(Good, self).__init__(*args, **kwargs)
        self.generate_slug()
        
    
    def generate_slug(self):
        """ генерирует slug на основе title """
        if self.title:
            self.slug = slugify(self.title)

    
    def __repr__(self):
        return "<id : {}, title : {}>".format(self.id , self.title)
    
    def __unicode__(self):
        return self.title

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    orders = db.relationship('Order', backref='user', lazy='dynamic')
    def __str__(self):
        return self.email

    def __repr__(self):
        return self.email

    def __unicode__(self):
        return self.email

OrderGood = db.Table('OrderGood', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('good.id')))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #  goods = db.relationship('Good', backref='order',lazy='dynamic')
    goods = db.relationship("Good", secondary=OrderGood, backref='order', lazy='dynamic')
    
@login.user_loader
def load_user(ID):
    return User.query.get(int(ID))

