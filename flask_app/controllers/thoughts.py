from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.thought import Thought
from flask_app.models.user import User

@app.route('/thoughts')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_by_id(data), thoughts = Thought.get_all_thoughts_w_users())

@app.route('/thoughts/create', methods=['POST'])
def create_thought():
    if 'user_id' not in session:
        return redirect('/')
    valid = Thought.thought_validation(request.form)
    if valid:
        data = {
            'body': request.form['body'],
            'user_id': session['user_id'],
        }
        thought = Thought.create_thought(data)
        return redirect('/thoughts')
    return redirect('/thoughts')

@app.route('/thoughts/<int:thought_id>/delete')
def destroy(thought_id):
    data = {
        'id': thought_id
    }
    Thought.destroy(data)
    return redirect('/thoughts')

@app.route('/thoughts/<int:thought_id>/like')
def like(thought_id):
    data = {
        'thought_id': thought_id,
        'user_id': session['user_id']
    }
    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] += 1
    Thought.like_thought(data)
    return redirect('/thoughts')

@app.route('/thoughts/<int:thought_id>/unlike')
def unlike(thought_id):
    data = {
        'thought_id': thought_id,
        'user_id': session['user_id']
    }
    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] -= 1
    Thought.unlike_thought(data)
    return redirect('/thoughts')

