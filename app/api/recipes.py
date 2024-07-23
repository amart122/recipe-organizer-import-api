from flask import Blueprint, jsonify, request
from app import db
from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY

ingredients_blueprint = Blueprint('recipes', __name__)

class Recipe(db.Model):
  __tablename__ = 'recipes'
  id = db.Column(db.Integer, primary_key=True)
  local_id = db.Column(db.String(64), index=True, unique=True)
  name = db.Column(db.String(128), index=True, unique=True)
  ingredients = db.relationship('Ingredient', backref='recipes', lazy='dynamic')
  prep_time = db.Column(db.String(64))
  serving_size = db.Column(db.String(64))
  instructions = db.Column(ARRAY(db.String(256)))
  notes = db.Column(db.String(256))
  description = db.Column(db.String(256))

  def __repr__(self):
    return f'<Recipe {self.name}-{self.localId}>'
