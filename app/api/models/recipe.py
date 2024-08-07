from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from .ingredient import Ingredient

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