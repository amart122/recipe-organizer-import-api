from flask import Blueprint, jsonify, request
from .scraper import RecipeOrganizerImporter

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/import-recipe', methods=['GET'])
def import_recipe():
  url = request.args.get('url')
  if not url:
    return jsonify({"error": "URL is required"}), 403
  
  # IMPORT RECIPE
  recipe = RecipeOrganizerImporter().scrape_recipe(url)
  return jsonify(recipe)