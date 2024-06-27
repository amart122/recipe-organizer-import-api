import math
import random
import nltk
import json
from nltk.stem import WordNetLemmatizer
from flask import url_for
from recipe_scrapers import scrape_me
from recipe_scrapers._exceptions import WebsiteNotImplementedError
from quantulum3 import parser

class RecipeOrganizerImporter:
  def __init__(self):
    single_word_ingredients, multi_word_ingredients = RecipeOrganizerImporter.load_ingredients()
    self.single_word_ingredients = single_word_ingredients
    self.multi_word_ingredients = multi_word_ingredients
    self.lemmatizer = WordNetLemmatizer()

  def scrape_recipe(self, url):
    try:
      scraper = scrape_me(url)
      formatted_recipe = self.format_recipe(scraper)

      return formatted_recipe
    except WebsiteNotImplementedError:
      return {"error": "Website not implemented"}

  def format_recipe(self, scraper):
    formatted_ingredient = self.format_ingredients(scraper.ingredients())
    new_ingredients = [{"id": ingredient["id"], "name": ingredient["name"]} for ingredient in formatted_ingredient]

    formatted_recipe = {
      "id": RecipeOrganizerImporter.get_id(),
      "name": scraper.title(),
      "ingredients": formatted_ingredient,
      "instructions": scraper.instructions().split("\n"),
      "prepTime": scraper.total_time(),
      "servingSize": scraper.yields(),
      "notes": "",
      "description": scraper.title(),
    }

    return [formatted_recipe, new_ingredients]

  def format_ingredients(self, ingredients):
    formatted_ingredients = []

    for ingredient in ingredients:
      name, raw = self.parse_ingredient_name(ingredient)
      quantity, unit = self.parse_unit_quantity(ingredient)
      
      formatted_ingredient = {
        "id": RecipeOrganizerImporter.get_id(),
        "name": name,
        "quantity": quantity,
        "unit": unit,
        "raw": raw,
      }
      formatted_ingredients.append(formatted_ingredient)

    return formatted_ingredients

  def parse_unit_quantity(self, ingredient):
    quant = [quant for quant in parser.parse(ingredient) if quant.unit.name != "dimensionless"]
    quant = [quant for quant in parser.parse(ingredient)] if len(quant) == 0 else quant
    quantity = quant[0].value if len(quant) > 0 else ''
    unit = quant[0].unit.name if len(quant) > 0 and quant[0].unit and quant[0].unit.name != "dimensionless" else ''

    return (quantity, unit)

  def parse_ingredient_name(self, ingredient):
    ingredient_array = ingredient.split()
    name = ''

    for idx, word in enumerate(ingredient_array):
      ingredient_name = None

      try:
        word1 = self.process_word(word)
        word2 = self.process_word(ingredient_array[idx + 1]) if len(ingredient_array) > idx + 1 else None
        word3 = self.process_word(ingredient_array[idx + 2]) if len(ingredient_array) > idx + 2 else None

        if word3 and word1 + " " + word2 + " " + word3 in self.multi_word_ingredients:
          ingredient_name = self.multi_word_ingredients[word1 + " " + word2 + " " + word3]
        elif word2 and word1 + " " + word2 in self.multi_word_ingredients:
          ingredient_name = self.multi_word_ingredients[word1 + " " + word2]
        elif word1 in self.single_word_ingredients:
          ingredient_name = word1
      except AttributeError:
        print("AttributeError: " + word1 + " " + word2 + " " + word3)
        pass
      except KeyError:
        print("KeyError: " + word1 + " " + word2 + " " + word3)
        pass

      if ingredient_name:
        name = ingredient_name
        break

    return (name, ingredient) if name else (ingredient, ingredient)

  def process_word(self, word):
    return self.lemmatizer.lemmatize(word.replace(",", "")
              .replace(".", "")
              .replace("(", "")
              .replace(")", "")
              .replace(":", "")
              .replace(";", "")
              .replace("!", "")
              .replace("?", "")
              .replace("'", "")
              .replace('"', "")
              .lower())

  @staticmethod
  def get_id():
    return  math.floor(random.random() * 1000000000)

  @staticmethod
  def load_ingredients():
    with open('app/static/single_word_ingredients.json') as f:
      single_word_ingredients = json.load(f)
    with open('app/static/multi_word_ingredients.json') as f:
      multi_word_ingredients = json.load(f)

    return (single_word_ingredients, multi_word_ingredients)