from flask_app import Flask, app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():
    db_name = 'thought_dashboard'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    def full_name(self):
        return(f"{self.first_name} {self.last_name}")

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def create_user(cls, form_data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(hashed_pw)s)"
        return connectToMySQL(cls.db_name).query_db(query, form_data)


    @staticmethod
    def user_validation(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address! Please enter a valid email address")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.db_name).query_db(query, form_data)
        if len(results) != 0:
            flash("Email already exists. Please log in")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Confirm password does not match")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])