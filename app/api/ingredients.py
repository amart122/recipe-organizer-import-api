from flask import Blueprint, jsonify, request
from flask import current_app
from middleware import firebase_login
from app.api.models.ingredient import Ingredient
from app import db

ingredients_blueprint = Blueprint('ingredients', __name__)

@ingredients_blueprint.route('/ingredients', methods=['GET'])
@firebase_login
def get_ingredients(user):
  ingredients = Ingredient.query.filter_by(user_id=user.id).all()
  return jsonify([{
    "name": ingredient.name,
    "id": int(ingredient.local_id)
    }
    for ingredient in ingredients
  ])

@ingredients_blueprint.route('/ingredients', methods=['POST'])
@firebase_login
def add_ingredients(user):
  data = request.get_json()
  for ingredient in data:
    new_ingredient = Ingredient(name=ingredient['name'], local_id=ingredient['local_id'], user_id=user.id)
    db.session.add(new_ingredient)
  db.session.commit()
  return jsonify({'message': 'Ingredient added successfully'})
