from app import app, db
from app.models import Good, Category, User, Order

@app.shell_context_processor
def make_shell_context():
    return{
        'db': db, 
        'Good': Good,
        'Category': Category,
        'User': User,
        'Order': Order,
    }