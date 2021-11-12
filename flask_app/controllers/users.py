from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.thought import Thought

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    form_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
    }
    valid = User.user_validation(form_data)
    if valid:
        hashed_pw = bcrypt.generate_password_hash(request.form['password'])
        form_data['hashed_pw'] = hashed_pw
        user = User.create_user(form_data)
        session['user_id'] = user
        return redirect('/thoughts')
    return redirect('/')

@app.route('/user/login', methods=['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email or password")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email or password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/thoughts')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': user_id
    }
    data_main = {
        'id': session['user_id']
    }
    return render_template('user_details.html', user = User.get_by_id(data), thoughts = Thought.get_all_by_user(data), user_main = User.get_by_id(data_main))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')