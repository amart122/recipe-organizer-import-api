import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
  ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')