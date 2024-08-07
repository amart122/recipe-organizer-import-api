from app import db

class RecipeIngredient(db.Model):
  __tablename__ = 'recipe_ingredients'
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
  ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
  meta = db.Column(db.JSON)

  def __repr__(self):
    return f'<RecipeIngredient {self.recipe_id}-{self.ingredient_id}>'