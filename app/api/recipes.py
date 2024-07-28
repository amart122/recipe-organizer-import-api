from flask import Blueprint, jsonify, request
from app import db
from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY
from middleware import firebase_login
from .ingredients import Ingredient
from .recipe_ingredients import RecipeIngredients

recipes_blueprint = Blueprint('recipes', __name__)

class Recipe(db.Model):
  __tablename__ = 'recipes'
  id = db.Column(db.Integer, primary_key=True)
  local_id = db.Column(db.String(64), index=True, unique=True)
  name = db.Column(db.String(128), index=True, unique=True)
  prep_time = db.Column(db.String(64))
  serving_size = db.Column(db.String(64))
  instructions = db.Column(ARRAY(db.String(256)))
  notes = db.Column(db.String(256))
  description = db.Column(db.String(256))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  ingredients = db.relationship('Ingredient', secondary='recipe_ingredients', backref='recipes')

  def __repr__(self):
    return f'<Recipe {self.name}-{self.local_id}>'

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

    for new_ingredient in recipe['ingredients']:
      ingredient = Ingredient.query.filter_by(local_id=str(new_ingredient['id'])).first()
      if not ingredient:
        pass

      recipe_ingredient = RecipeIngredients.query.get((new_recipe.id, ingredient.id))
      if recipe_ingredient:
        new_meta = recipe_ingredient.meta
        new_meta['meta'].append((new_ingredient['quantity'], new_ingredient['unit']))
        recipe_ingredient.meta = new_meta
      else:
        recipe_ingredient = RecipeIngredients(recipe_id=new_recipe.id, ingredient_id=ingredient.id, meta={'meta': [(new_ingredient['quantity'], new_ingredient['unit'])]})
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