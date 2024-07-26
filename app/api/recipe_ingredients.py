from app import db

class RecipeIngredients(db.Model):
  __tablename__ = 'recipe_ingredients'
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
  ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)

  def __repr__(self):
    return f'<RecipeIngredients {self.recipe_id}-{self.ingredient_id}>'