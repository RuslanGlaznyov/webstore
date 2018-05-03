from app import app, db
from app.models import Category, Good

def delete_db():
    goods = Good.query.all()
    for good in goods:
        db.session.delete(good)
    
    categorys = Category.query.all()
    for category in categorys:
        db.session.delete(category)
    
    db.session.commit()



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.create_all()
delete_db()

title = 'good'
price=1
quantity = 1
category = Category(category='куб')


for i in range(100):
    good = Good(title=title, price=price, quantity=quantity, category=category, desc=title)
    db.session.add(good)
    
    title = 'good'
    price += 1
    quantity += 1
    title = title + str(price)
    
    

db.session.commit()
