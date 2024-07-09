from flask import Blueprint, jsonify, request
from .scraper import RecipeOrganizerImporter
from flask import current_app as app

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/import-recipe', methods=['GET'])
def import_recipe():
  url = request.args.get('url')
  if not url:
    response = jsonify({"error": "URL is required"})
    response.status_code = 400
    response.headers.add("Access-Control-Allow-Origin", app.config['ALLOWED_HOSTS'])
    return response

  recipe = RecipeOrganizerImporter().scrape_recipe(url)
  response = jsonify(recipe)
  response.status_code = 200
  response.headers.add("Access-Control-Allow-Origin", app.config['ALLOWED_HOSTS'])
  return response