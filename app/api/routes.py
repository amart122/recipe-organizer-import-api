from flask import Blueprint, jsonify, request

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/import-recipe', methods=['GET'])
def import_recipe():
  url = request.args.get('url')
  if not url:
    return jsonify({"error": "URL is required"}), 400
  
  # IMPORT RECIPE
  print("URL: " + url)
  
  return jsonify({
    "recipe": {
      "id": 0,
      "name": "",
      "aliases": [""],
      "ingredients": [
        {
          "id": 1,
          "quantity": 1,
          "unit": "cup"
        }
      ],
      "prepTime": 2,
      "servingSize": 0,
      "instructions": "xx",
      "notes": "xx",
      "description": "xx"
    },
    "ingredients": [{
      "id:": 1,
      "name": "XXX",
    }]
  })