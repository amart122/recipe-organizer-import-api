from flask import Blueprint, jsonify, request
from app import db
from flask import current_app

ingredients_blueprint = Blueprint('ingredients', __name__)

class Ingredient(db.Model):
  __tablename__ = 'ingredients'  
  id = db.Column(db.Integer, primary_key=True)
  local_id = db.Column(db.String(64), index=True, unique=True)
  name = db.Column(db.String(64), index=True, unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def __repr__(self):
    return f'<Ingredient {self.name}-{self.local_id}>'
