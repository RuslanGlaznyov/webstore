from app import db
import re

def slugify(s):
    """ заменяет все символы кроме букв и цифр на '-' """
    pattern = r'[^\w+]'
    slug = re.sub(pattern,"-", s)
    return slug.lower()

class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer) #название товара 
    category = db.Column(db.String(64))
    desc = db.Column(db.Text)#описание товара 
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    slug = db.Column(db.String(64)) #ссылка на товар 
    imgsrc =  db.Column(db.String(128))

    def __init__(self, *args, **kwargs):
        super(Good, self).__init__(*args, **kwargs)
        self.generate_slug()
        
    
    def generate_slug(self):
        """ генерирует slug на основе title """
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return "<id : {}, title : {}>".format(self.id , self.title)

