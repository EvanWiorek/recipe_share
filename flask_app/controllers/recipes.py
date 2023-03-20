from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/create_page')
def display_create_page():
    return render_template("create_page.html")

@app.route('/add_new_recipe', methods=['POST'])
def add_new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create_page')
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            **request.form,
            "user_id" : user_id
        }
        recipe_data = Recipe.save(data)
    else:
        return redirect('/')
    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>')
def display_recipe(recipe_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = {
            "user_id" : user_id
        }
        current_user = User.get_user_by_id(user_data)
    recipe_data = {
        "recipe_id" : recipe_id
    }
    recipe_info = Recipe.get_recipe_by_id(recipe_data)
    return render_template("recipes_show.html", recipe_info = recipe_info, current_user = current_user)

@app.route('/recipes/<int:recipe_id>/edit')
def display_update_page(recipe_id):
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            "user_id" : user_id,
            "recipe_id" : recipe_id
        }
        session['recipe_id'] = recipe_id
    current_recipe = Recipe.get_recipe_by_id(data)
    return render_template("update_recipe.html", current_recipe = current_recipe)


@app.route('/update_recipe', methods = ['POST'])
def edit_recipe():
    if 'user_id' and 'recipe_id' in session:
        user_id = session['user_id']
        recipe_id = session['recipe_id']
        data = {
            **request.form,
            "user_id" : user_id,
            "recipe_id" : recipe_id
        }
        if not Recipe.validate_recipe(request.form):
            return redirect(f'/recipes/{recipe_id}/edit')
        Recipe.update_recipe(data)
    else:
        return redirect('/')
    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    data = {
        "recipe_id" : recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')
    