from app import db

class RecipeIngredients(db.Model):
  __tablename__ = 'recipe_ingredients'
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
  ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
  quantity = db.Column(db.Numeric(10, 2), default=0)
  unit = db.Column(db.String(50), nullable=True)
  raw = db.Column(db.String(255), nullable=True)

  def __repr__(self):
    return f'<RecipeIngredients {self.recipe_id}-{self.ingredient_id}>'