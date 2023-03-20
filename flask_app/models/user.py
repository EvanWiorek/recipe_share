from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'recipes_schema';
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
    		VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @staticmethod
    def validate_user_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.DB).query_db(query,user)
        if len(user['first_name']) < 3 or len(user['last_name']) < 3:
            flash("Name should be at least 3 characters.", 'name_short')
            is_valid = False
        if any(str.isdigit(n) for n in user['first_name']) == True or any(str.isdigit(n) for n in user['last_name']) == True:
            flash("Name shouldn't contain any numbers.", 'name_no_num')
            is_valid = False
        if len(result) >= 1:
            flash("Email is already registered.", 'email_registered')
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", 'email_invalid')
            is_valid = False
        if len(user['password']) < 9:
            flash("Password needs to be at least 8 characters.", 'password_short')
            is_valid = False
        if user['password'] != user['confirm_password'] :
            flash("Passwords do not match.", 'passwords_no_match')
            return False
        return is_valid
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])
        