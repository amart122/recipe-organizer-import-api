from recipe_scrapers import scrape_me
from recipe_scrapers._exceptions import WebsiteNotImplementedError
from quantulum3 import parser
import math
import random
import pdb

class RecipeOrganizerImporter:
  @staticmethod
  def scrape_recipe(url):
    try:
      scraper = scrape_me(url)
      formatted_recipe = RecipeOrganizerImporter.format_recipe(scraper)

      return formatted_recipe
    except WebsiteNotImplementedError:
      return {"error": "Website not implemented"}

  @staticmethod
  def format_recipe(scraper):
    formatted_ingredient = RecipeOrganizerImporter.format_ingredients(scraper.ingredients())
    new_ingredients = [{"id": ingredient["id"], "name": ingredient["name"]} for ingredient in formatted_ingredient]

    pdb.set_trace()

    formatted_recipe = {
      "id": RecipeOrganizerImporter.get_id(),
      "name": recipe,
      "ingredients": formatted_ingredient,
      "instructions": scraper.instructions,
      "prepTime": 0,
      "servingSize": 0,
      "notes": "",
      "description": ""
    }

    return formatted_recipe, new_ingredients

  @staticmethod
  def format_ingredients(ingredients):
    formatted_ingredients = []
    for ingredient in ingredients:
      parsed_ingredient = RecipeOrganizerImporter.parse_ingredient(ingredient)
      
      formatted_ingredient = {
        "id": RecipeOrganizerImporter.get_id(),
        "name": parsed_ingredient['name'],
        "quantity": parsed_ingredient['quantity'],
        "unit": parsed_ingredient['unit'],
      }
      formatted_ingredients.append(formatted_ingredient)

    return formatted_ingredients

  @staticmethod
  def get_id():
    return  math.floor(random.random() * 1000000000)

  @staticmethod
  def parse_ingredient(ingredient):
    quant = [quant for quant in  parser.parse(ingredient) if quant.unit.name != "dimensionless"]
    quantity = quant[0].value if len(quant) > 0 else ''
    unit = quant[0].unit.name if len(quant) > 0 and quant[0].unit else ''
    name = "xx"

    return {
      "name": name,
      "unit": unit,
      "quantity": quantity,
      "raw": ingredient
    }


    # pattern = re.compile(r'(\d*\.?\d+\/?\d*)?\s*(\w+)?\s*([^,]+)(?:,\s*(.*))?')
    # match = pattern.match(ingredient)
    
    # if match:
    #   quantity = match.group(1) if match.group(1) else ''
    #   unit = match.group(2) if match.group(2) else ''
    #   ingredient = match.group(3) if match.group(3) else ''
    #   extra_info = match.group(4) if match.group(4) else ''

    #   return {
    #     "quantity": quantity.strip(),
    #     "unit": unit.strip(),
    #     "ingredient": ingredient.strip(),
    #     "extra_info": extra_info.strip()
    #   }
    # else:
    #   return None