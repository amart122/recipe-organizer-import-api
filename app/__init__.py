import firebase_admin
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  
  db.init_app(app)
  migrate = Migrate(app, db)

  cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
  firebase_app = firebase_admin.initialize_app(cred)

  # Models
  from .api.users import User
  from .api.recipes import Recipe
  from .api.ingredients import Ingredient
  from .api.recipe_ingredients import RecipeIngredients

  from .api.routes import api_blueprint
  from .api.ingredients import ingredients_blueprint
  app.register_blueprint(api_blueprint, url_prefix='/api')
  app.register_blueprint(ingredients_blueprint, url_prefix='/api/storage')

  return app