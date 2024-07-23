import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
  ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False