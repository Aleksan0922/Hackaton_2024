from flask import Flask, render_template, redirect, url_for, flash, request, make_response, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired

from PIL import ImageDraw, Image
import numpy as np
import hashlib

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


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    username = StringField('Никнейм', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


def generate_quiz(type, lvl):
    if type == '+':
        if lvl == 'easy':
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'x = {num_1} + {num_2}'
        if lvl == 'medium':
            num_1 = random.randint(11, 50)
            num_2 = random.randint(11, 50)
            num_3 = random.randint(0, 10)
            return f'x = {num_1} + {num_2} + {num_3}'
        if lvl == 'hard':
            num_1 = random.randint(100, 500)
            num_2 = random.randint(100, 500)
            num_3 = random.randint(11, 100)
            num_4 = random.randint(0, 10)
            return f'x = {num_1} + {num_2} + {num_3} + {num_4}'
    elif type == '-':
        if lvl == 'easy':
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'x = {num_1} - {num_2}'
        if lvl == 'medium':
            num_1 = random.randint(11, 50)
            num_2 = random.randint(11, 50)
            num_3 = random.randint(0, 10)
            return f'x = {num_1} - {num_2} - {num_3}'
        if lvl == 'hard':
            num_1 = random.randint(100, 500)
            num_2 = random.randint(100, 500)
            num_3 = random.randint(11, 100)
            num_4 = random.randint(0, 10)
            return f'x = {num_1} - {num_2} - {num_3} - {num_4}'
    elif type == '*':
        if lvl == 'easy':
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'x = {num_1} * {num_2}'
        if lvl == 'medium':
            num_1 = random.randint(11, 100)
            num_2 = random.randint(0, 10)
            return f'x = {num_1} * {num_2}'
        if lvl == 'hard':
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            return f'x = {num_1} * {num_2}'
    elif type == ':':
        if lvl == 'easy':
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'x = {num_1 * num_2} : {num_1}'
        if lvl == 'medium':
            num_1 = random.randint(11, 100)
            num_2 = random.randint(0, 10)
            return f'x = {num_1 * num_2} : {num_2}'
        if lvl == 'hard':
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            return f'x = {num_1 * num_2} : {num_1}'


def generate_avatar(nickname: str) -> Image:
    bytes = hashlib.md5(nickname.encode('utf-8')).digest()

    main_color = bytes[:3]
    main_color = tuple(channel // 2 + 128 for channel in main_color)

    blocks = np.array([bit == '1' for byte in bytes[3:3+9] for bit in bin(byte)[2:].zfill(8)]).reshape(6, 12)
    blocks = np.concatenate((blocks, blocks[::-1]), axis=0)

    blocks[0, :] = 0
    blocks[-1, :] = 0
    blocks[:, 0] = 0
    blocks[:, -1] = 0

    img_size = (12, 12)
    img = Image.new('RGBA', img_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for x, y in np.argwhere(blocks):
        draw.point((x, y), main_color)

    return img


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('difficulty.html')
    return render_template('index.html')


@app.route('/quest/<difficulty>', methods=['GET'])
def sign(difficulty):
    return render_template('sign.html', difficulty=difficulty)


@app.route('/quest/<difficulty>/<sign>', methods=['GET', 'POST'])
def quest(difficulty, sign):
    print(session['easy'], session['medium'], session['hard'])
    if request.method == 'POST':
        question = request.form.get('quest-question')
        user_ans = request.form.get('test-input')
        question = question.replace(':', '/')
        answer = eval(question)
        question = generate_quiz(sign, difficulty)
        if user_ans != '' and answer == int(user_ans):
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            if difficulty == 'easy':
                user.total_lvl_1 += 1
            elif difficulty == 'medium':
                user.total_lvl_2 += 1
            elif difficulty == 'hard':
                user.total_lvl_3 += 1
            db_sess.commit()
            if difficulty not in session:
                session['easy'] = 0
                session['medium'] = 0
                session['hard'] = 0
            session[difficulty] += 1
            return render_template('quest.html', question=question, answer=True)
        else:
            if difficulty in session:
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.id == current_user.id).first()
                if difficulty == 'easy':
                    if session[difficulty] > current_user.stat_lvl_1:
                        user.stat_lvl_1 = session['easy']
                        session['easy'] = 0
                elif difficulty == 'medium':
                    if session[difficulty] > current_user.stat_lvl_2:
                        user.stat_lvl_2 = session['medium']
                        session['medium'] = 0
                elif difficulty == 'hard':
                    if session[difficulty] > current_user.stat_lvl_3:
                        user.stat_lvl_3 = session['hard']
                        session['hard'] = 0
                db_sess.commit()
            return render_template('quest.html', question=question, answer=False)
    if not session.modified:
        session.modified = True
    question = generate_quiz(sign, difficulty)
    return render_template('quest.html', question=question, answer=None)


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


@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup.html', title='Sign up',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('signup.html', title='Sign up',
                                   form=form,
                                   message="Такой пользователь уже есть")
        generate_avatar(form.username.data).save(f'static/images/{form.username.data}.png')
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            email=form.email.data,
            stat_lvl_1=0,
            stat_lvl_2=0,
            stat_lvl_3=0,
            total_lvl_1=0,
            total_lvl_2=0,
            total_lvl_3=0,
            avatar=f'{form.username.data}.png'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/account', methods=['GET'])
def account():
    return render_template('me.html')


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    db_sess = db_session.create_session()

    app.run(host='0.0.0.0', port=5000)
