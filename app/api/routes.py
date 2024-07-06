from flask import Blueprint, jsonify, request
from .scraper import RecipeOrganizerImporter

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/import-recipe', methods=['GET'])
def import_recipe():
  url = request.args.get('url')
  if not url:
    response = jsonify({"error": "URL is required"})
    response.status_code = 400
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    return response
  
  recipe = RecipeOrganizerImporter().scrape_recipe(url)
  response = jsonify(recipe)
  response.status_code = 200
  response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
  return response