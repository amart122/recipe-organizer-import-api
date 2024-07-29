import firebase_admin
from flask import Flask, request
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
  from .api.models.user import User
  from .api.models.ingredient import Ingredient
  from .api.models.recipe import Recipe
  from .api.models.recipe_ingredient import RecipeIngredient

  from .api.routes import api_blueprint
  from .api.ingredients import ingredients_blueprint
  from .api.recipes import recipes_blueprint
  from .api.users import users_blueprint
  app.register_blueprint(api_blueprint, url_prefix='/api')
  app.register_blueprint(users_blueprint, url_prefix='/api')
  app.register_blueprint(ingredients_blueprint, url_prefix='/api/storage')
  app.register_blueprint(recipes_blueprint, url_prefix='/api/storage')

  @app.after_request
  def add_cors_header(response):
    response.headers.add("Access-Control-Allow-Origin", app.config['ALLOWED_HOSTS'])

    if(request.method == 'OPTIONS'):
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH')
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

  return app