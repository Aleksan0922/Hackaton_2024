from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired

from werkzeug.utils import secure_filename

import os
import random

from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/users.db")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


def generate_quiz(type, lvl):
    if type == '+':
        if lvl == 1:
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'{num_1} + {num_2}', num_1 + num_2
        if lvl == 2:
            num_1 = random.randint(11, 50)
            num_2 = random.randint(11, 50)
            num_3 = random.randint(0, 10)
            return f'{num_1} + {num_2} + {num_3}', num_1 + num_2 + num_3
        if lvl == 3:
            num_1 = random.randint(100, 500)
            num_2 = random.randint(100, 500)
            num_3 = random.randint(11, 100)
            num_4 = random.randint(0, 10)
            return f'{num_1} + {num_2} + {num_3} + {num_4}', num_1 + num_2 + num_3 + num_4
    elif type == '-':
        if lvl == 1:
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'{num_1} - {num_2}', num_1 - num_2
        if lvl == 2:
            num_1 = random.randint(11, 50)
            num_2 = random.randint(11, 50)
            num_3 = random.randint(0, 10)
            return f'{num_1} - {num_2} - {num_3}', num_1 - num_2 - num_3
        if lvl == 3:
            num_1 = random.randint(100, 500)
            num_2 = random.randint(100, 500)
            num_3 = random.randint(11, 100)
            num_4 = random.randint(0, 10)
            return f'{num_1} - {num_2} - {num_3} - {num_4}', num_1 - num_2 - num_3 - num_4
    elif type == '*':
        if lvl == 1:
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'{num_1} * {num_2}', num_1 * num_2
        if lvl == 2:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(0, 10)
            return f'{num_1} * {num_2}', num_1 * num_2
        if lvl == 3:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            return f'{num_1} * {num_2}', num_1 * num_2
    elif type == ':':
        if lvl == 1:
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'{num_1 * num_2} : {num_1}', num_2
        if lvl == 2:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(0, 10)
            return f'{num_1 * num_2} : {num_2}', num_1
        if lvl == 3:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            return f'{num_1 * num_2} : {num_1}', num_2


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect('/')
        flash('Неправильная почта или пароль', 'error')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    db_sess = db_session.create_session()

    app.run(host='0.0.0.0', port=5000)
