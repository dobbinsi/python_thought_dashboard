from flask_app import Flask, app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Thought():
    db_name = 'thought_dashboard'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.body = db_data['body']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None
        self.num_likes = 0
    
    @classmethod
    def get_all_thoughts(cls):
        query = "SELECT * FROM thoughts;"
        return connectToMySQL(cls.db_name).query_db(query)

    @staticmethod
    def thought_validation(form_data):
        is_valid = True
        if len(form_data['body']) < 5:
            flash('Thought must be at least 5 characters')
            is_valid = False
        if len(form_data['body']) > 255:
            flash('Exceeded character limit. Max character length: 255')
            is_valid = False
        return is_valid
    
    @classmethod
    def create_thought(cls, form_data):
        query = "INSERT INTO thoughts (body, user_id) VALUES (%(body)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, form_data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM thoughts WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_thoughts_w_users(cls):
        query = "SELECT * FROM thoughts LEFT JOIN users ON thoughts.user_id = users.id;"
        thoughts = connectToMySQL(cls.db_name).query_db(query)
        results = []
        for thought in thoughts:
            data = {
                'id': thought['users.id'],
                'first_name': thought['first_name'],
                'last_name': thought['last_name'],
                'email': thought['email'],
                'password': thought['password'],
                'created_at': thought['users.created_at'],
                'updated_at': thought['users.updated_at'],
            }
            one_thought = cls(thought)
            one_thought.creator = user.User(data)
            results.append(one_thought)
        return results
    
    @classmethod
    def get_all_by_user(cls, data):
        query = "SELECT * FROM thoughts JOIN users ON users.id=user_id WHERE user_id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def like_thought(cls, data):
        query = "INSERT INTO likes (like_dislike,thought_id, user_id) VALUES (%(1)s, %(thought_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def unlike_thought(cls, data):
        query = "DELETE FROM likes WHERE thought_id=%(thought_id)s AND user_id=%(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

