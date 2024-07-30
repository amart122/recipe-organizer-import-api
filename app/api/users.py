from app import db
from flask import Blueprint, jsonify, request
from middleware import firebase_login
from .models.user import User

users_blueprint = Blueprint('user', __name__)

@users_blueprint.route('/user/sync', methods=['GET'])
@firebase_login
def get_sync(user):
  return jsonify({
    "lastSynced": user.last_synced
  })

@users_blueprint.route('/user/sync', methods=['PATCH'])
@firebase_login
def update_sync(user):
  data = request.get_json()
  user.last_synced = data['lastSynced']
  db.session.commit()
  return jsonify({
    "lastSynced": user.last_synced
  })
