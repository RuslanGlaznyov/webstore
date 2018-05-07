from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

require_val= 'Заполните поле'
class LoginForm(FlaskForm):
    email = StringField('Эл. Почта', validators=[DataRequired(message=require_val)])
    password = PasswordField('Пароль', validators=[DataRequired(message=require_val)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    email = StringField('Эл. Почта', validators=[DataRequired(message=require_val), Email(message="Не валидный адрес эл.почты")])
    username = StringField('Имя', validators=[DataRequired(message=require_val)])
    password = PasswordField('Пароль', validators=[DataRequired(message=require_val)])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(message=require_val), EqualTo('password',message='пароли должны совпадать')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Пожалуйста используйте другой адрес эл.почты')

class AddToCartForm(FlaskForm):
    submit = SubmitField("добавить в корзину")
    good_id = HiddenField()