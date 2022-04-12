from logging import root
from time import localtime, strftime
from flask import Flask, redirect, render_template, url_for, flash
from wtform_fields import *
from models import *
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
#Конфигурация приложения
app = Flask(__name__)
app.secret_key = 'позже'

#Конфигурация БД
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///project.db'
db=SQLAlchemy(app)


#Инициализация Фласк SocketIO
socketio = SocketIO(app)
ROOMS=["Общение","Получение Задания","Консультация"]
#Настройка фласк-логин
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = Registration_form()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        hashd_pass=pbkdf2_sha512.hash(password)
        #Добавление полей реги в мою БД
        user = User(username=username, password=hashd_pass)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно. Пожалуйста, осуществите вход в систему.', 'success')

        return redirect(url_for('login'))
    return render_template('index.html', form=reg_form)
@app.route('/login',methods=['GET','POST'])
def login():
    log_form=Login_form()
    #Если подтверждение произошло и ошибок не возникло, то:
    if log_form.validate_on_submit(): 
        user_object= User.query.filter_by(username=log_form.username_enter.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    return render_template('login.html', form=log_form)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
           flash('Вы не аутентифицированы', 'danger')
           return redirect(url_for('login'))
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('Выход из аккаунта осуществлён успешно.', 'success')
    return redirect(url_for('login'))


@socketio.on('message')
def message(data):
    # print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data ['username'], 'time_stamp':strftime(': %d %B %H:%M', localtime())}, room=data['room'])

@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg':data['username'] + " подключился к чату " + data['room']}, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg':data['username'] + " отключился от чата " + data['room']}, room=data['room'])


if __name__ == "__main__":
    socketio.run(app, debug=True)