from flask import Blueprint, jsonify, request
from app import db
from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY
from middleware import firebase_login
from app.api.models.recipe import Recipe
from app.api.models.ingredient import Ingredient
from app.api.models.recipe_ingredient import RecipeIngredient

recipes_blueprint = Blueprint('recipes', __name__)

@recipes_blueprint.route('/recipes', methods=['GET'])
@firebase_login
def get_recipes(user):
  recipes = Recipe.query.filter_by(user_id=user.id).all()
  return jsonify([{
      "name": recipe.name,
      "id": int(recipe.local_id),
      "description": recipe.description,
      "preptime": recipe.prep_time,
      "servingSize": recipe.serving_size,
      "instructions": recipe.instructions,
      "notes": recipe.notes,
      "ingredients": [{"name": ingredient.name, "id": int(ingredient.local_id)} for ingredient in recipe.ingredients]
    }
    for recipe in recipes
  ])

@recipes_blueprint.route('/recipes', methods=['POST'])
@firebase_login
def create_recipes(user):
  data = request.get_json()
  for recipe in data:
    _recipe = Recipe.query.filter_by(local_id=str(recipe['id']), user_id=user.id).first()
    if _recipe:
      continue

    new_recipe = Recipe(
      name=recipe['name'],
      local_id=recipe['id'],
      prep_time=recipe['preptime'],
      serving_size=recipe['servingSize'],
      instructions=recipe['instructions'],
      notes=recipe['notes'],
      description=recipe['description'],
      user_id=user.id
    )
    db.session.add(new_recipe)
    db.session.commit()

    for new_ingredient in recipe['ingredients']:
      ingredient = Ingredient.query.filter_by(local_id=str(new_ingredient['id'])).first()
      if not ingredient:
        continue
      
      recipe_ingredient = RecipeIngredient.query.get((new_recipe.id, ingredient.id))
      if recipe_ingredient:
        new_meta = recipe_ingredient.meta
        new_meta['meta'].append((new_ingredient['quantity'], new_ingredient['unit']))
        recipe_ingredient.meta = new_meta
      else:
        recipe_ingredient = RecipeIngredient(recipe_id=new_recipe.id, ingredient_id=ingredient.id, meta={'meta': [(new_ingredient['quantity'], new_ingredient['unit'])]})
        db.session.add(recipe_ingredient)
      
      db.session.commit()

  return jsonify({'message': 'Recipes created!'})

@recipes_blueprint.route('/recipes/<recipe_id>', methods=['DELETE'])
@firebase_login
def delete_recipe(user, recipe_id):
  recipe = Recipe.query.filter_by(local_id=recipe_id, user_id=user.id).first()
  db.session.delete(recipe)
  db.session.commit()
  return jsonify({'message': 'Recipe deleted!'})