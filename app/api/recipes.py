from flask import Blueprint, jsonify, request
from app import db
from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY
from middleware import firebase_login

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
    return f'<Recipe {self.name}-{self.localId}>'

@recipes_blueprint.route('/recipes', methods=['GET'])
@firebase_login
def get_recipes(user):
  recipes = Recipe.query.filter_by(user_id=user.id).all()
  return jsonify([recipe.name for recipe in recipes])