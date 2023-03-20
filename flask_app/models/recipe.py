from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    DB = 'recipes_schema';
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under = data['under']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls, data):
        query = """INSERT INTO recipes (name, description, under, instructions, date_made, user_id)
    		VALUES (%(name)s, %(description)s, %(under)s, %(instructions)s, %(date_made)s, %(user_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_all_recipes(cls):
        query = """SELECT * FROM recipes 
                    LEFT JOIN users ON users.id = recipes.user_id;"""
        result = connectToMySQL(cls.DB).query_db(query)
        all_recipes = []
        for row in result:
            recipe = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            recipe.user = user.User(user_data) #this is similar to creating a key in recipe
            print(recipe, recipe.user)
            all_recipes.append(recipe)
        return all_recipes 
    
    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(recipe_id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        recipe_by_id = cls(result[0])
        # print(recipe_by_id)
        print(result[0])
        user_data = {
            "id" : result[0]["user_id"],
            "first_name" : result[0]["first_name"],
            "last_name" : result[0]["last_name"],
            "email" : result[0]["email"],
            "password" : result[0]["password"],
            "created_at" : result[0]["users.created_at"],
            "updated_at" : result[0]["users.updated_at"]
        }
        print(user_data)
        recipe_by_id.user = user.User(user_data) #dont need to make it a list, add it to a user item
            # print(recipe_by_id.users[0].first_name)
        return recipe_by_id
    
    @classmethod
    def update_recipe(cls, data):
        query = """UPDATE recipes 
                    SET name = %(name)s, description = %(description)s, under = %(under)s, instructions = %(instructions)s, date_made = %(date_made)s 
                    WHERE recipes.user_id = %(user_id)s and recipes.id = %(recipe_id)s;""" #shouldnt need to check for both
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) == 0:
            flash("Name must not be blank.", 'name_blank')
            is_valid = False
        if len(recipe['description']) == 0:
            flash("Description must not be blank.", 'desc_blank')
            is_valid = False
        if len(recipe['instructions']) == 0:
            flash("Instructions must not be blank.", 'inst_blank')
            is_valid = False
        if len(recipe['date_made']) == 0:
            flash("Date must not be blank.", 'Date_blank')
            is_valid = False
        if 'under' not in recipe:
            flash("Please select an option for Under 30 Minutes", 'under_blank')
            is_valid = False
        return is_valid