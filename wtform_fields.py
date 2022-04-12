
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import *
from passlib.hash import pbkdf2_sha512

#Функция проверки соответсвия логина
def invalid_data(form, field):
    username_entered=form.username_enter.data
    password_entered=field.data
    user_log_obj=User.query.filter_by(username=username_entered).first()
    if user_log_obj is None:
        raise ValidationError('Неверное имя или пароль')
    elif not pbkdf2_sha512.verify(password_entered, user_log_obj.password):
        raise ValidationError('Неверное имя или пароль')

#Класс, содержащий форму регистрации с полями
class Registration_form(FlaskForm):
    username = StringField('name', validators=[InputRequired('Необходимо ввести имя пользователя'), 
        Length(min=2,max=25, message='Имя должно быть в диапазоне от 2 до 25 символов')])
    password = PasswordField('pass', validators=[InputRequired('Необходимо ввести пароль'),
        Length(min=4, max=20, message='Длина пароля от 4 до 20 символов')])
    confirm_password = PasswordField('pass_conf', validators=[InputRequired('Необходимо ввести подтверждение пароля'), EqualTo('password', message='Пароли должны быть идентичными')])
    
    #Функция кастомной проверки на наличие данных, введённых в полях в БД
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('Имя пользователя уже занято') 

#Класс формы входа(логинизации)
class Login_form(FlaskForm):
    username_enter = StringField(validators=[InputRequired('Необходимо ввести имя пользователя')])
    password_enter = PasswordField(validators=[InputRequired('Необходимо ввести пароль'), invalid_data])
