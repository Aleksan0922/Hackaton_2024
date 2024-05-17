from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


# !!! В разработке !!!
def generate_quiz(type, lvl):
    if type == '+':
        if lvl == 1:
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'{num_1} + {num_2}', num_1 + num_2
        if lvl == 2:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            return f'{num_1} + {num_2}', num_1 + num_2
        if lvl == 3:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            num_3 = random.randint(0, 10)
            return f'{num_1} + {num_2} + {num_3}', num_1 + num_2 + num_3
        if lvl == 4:
            num_1 = random.randint(1000, 100000)
            num_2 = random.randint(1000, 100000)
            return f'{num_1} + {num_2}', num_1 + num_2
        if lvl == 5:
            num_1 = random.randint(1000, 100000)
            num_2 = random.randint(1000, 100000)
            num_3 = random.randint(11, 100)
            num_4 = random.randint(0, 10)
            return f'{num_1} + {num_2} + {num_3} + {num_4}', num_1 + num_2 + num_3 + num_4
    elif type == '-':
        if lvl == 1:
            num_1 = random.randint(0, 10)
            num_2 = random.randint(0, 10)
            return f'{num_1} - {num_2}', num_1 - num_2
        if lvl == 2:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            return f'{num_1} - {num_2}', num_1 - num_2
        if lvl == 3:
            num_1 = random.randint(11, 100)
            num_2 = random.randint(11, 100)
            num_3 = random.randint(0, 10)
            return f'{num_1} - {num_2} - {num_3}', num_1 - num_2 - num_3
        if lvl == 4:
            num_1 = random.randint(1000, 100000)
            num_2 = random.randint(1000, 100000)
            return f'{num_1} - {num_2}', num_1 - num_2
        if lvl == 5:
            num_1 = random.randint(1000, 100000)
            num_2 = random.randint(1000, 100000)
            num_3 = random.randint(11, 100)
            num_4 = random.randint(0, 10)
            return f'{num_1} - {num_2} - {num_3} - {num_4}', num_1 - num_2 - num_3 - num_4
# !!! В разработке !!!


@login_manager.user_loader
def load_user(user_id):
    pass


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


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
    app.run(host='0.0.0.0', port=5000)
