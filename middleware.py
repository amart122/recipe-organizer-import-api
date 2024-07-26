import firebase_admin
from flask import request, jsonify
from firebase_admin import auth
from app.api.users import User
from functools import wraps
from app import db

def firebase_login(f):
  @wraps(f)

  def decorated_function(*args, **kwargs):
    token = request.headers.get('Authorization')
    if not token:
      return jsonify({"error": "Authorization Required"}), 401

    try:
      decoded_token = auth.verify_id_token(token)
      uid = decoded_token['uid']
      email = decoded_token['email']
      user = User.query.filter_by(uid=uid).first()
      if not user:
        user = User(uid=uid, email=email)
        db.session.add(user)
        db.session.commit()
    except firebase_admin.auth.InvalidIdTokenError:
      return jsonify({"error": "Invalid Token"}), 401

    return f(user, *args, **kwargs)

  return decorated_function