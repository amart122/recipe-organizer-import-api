from app import db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(64), index=True, unique=True, nullable=False)
  email = db.Column(db.String(64), index=True, unique=True)
  last_synced = db.Column(db.DateTime)

  def __repr__(self):
    return f'<Ingredient {self.uid}>'
