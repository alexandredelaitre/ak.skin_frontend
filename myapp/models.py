from flask_login import UserMixin
from . import db

"""
        'assetid': asset['assetid'],
        'market_name': description['market_name'],
        'market_hash_name': description['market_hash_name'],
        'name': description['name'],
        'icon_url': description['icon_url'],
        'descriptions': description['descriptions'],
        'tradable': description['tradable'],
        'name_color': description['name_color'],
        'commodity': description['commodity'],
        'type': description['type'],
        'marketable': description['marketable'],
        'tags': description['tags'],
        'market_tradable_restriction': description['market_tradable_restriction'],
        'number_owned': asset['amount'],
        'tradable': description['tradable'],
"""


class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  market_name = db.Column(db.String(200))
  market_hash_name = db.Column(db.String(200))
  name = db.Column(db.String(80))
  icon_url = db.Column(db.String(300))
  descriptions = db.Column(db.JSON)
  tradable = db.Column(db.Integer)
  name_color = db.Column(db.String(80))
  commodity = db.Column(db.Integer)
  type = db.Column(db.String(80))
  marketable = db.Column(db.Integer)
  tags = db.Column(db.JSON)
  itemid = db.Column(db.String(80))

  def __repr__(self):
    return '<Item %r>' % self.name

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  steamid = db.Column(db.String(80))
  name = db.Column(db.String(80), unique=False, nullable=False)
  avatar = db.Column(db.String(80), unique=False, nullable=False)
  balance = db.Column(db.Float, unique=False, nullable=False)
  email = db.Column(db.String(80), nullable=False)
  tradeurl = db.Column(db.String(80), unique=True, nullable=False)
  
  

class UserSpecificItems(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  belongsToUser = db.Column(db.Integer, unique=False, nullable=False)
  price = db.Column(db.Float, unique=False, nullable=False)
  floatValue = db.Column(db.Float, unique=False, nullable=False)
  image = db.Column(db.String(80), unique=False, nullable=False)
  type = db.Column(db.String(80), unique=False, nullable=False) #Item type e.g AK-47, etc
  itemset = db.Column(db.String(80), unique=False, nullable=False) #Item set e.g Knives, etc
  floatType = db.Column(db.String(80), unique=False, nullable=False) #Float type e.g Factory New, etc
  tradeMadeTime = db.Column(db.String(80), unique=False, nullable=False) #Time trade was made

class Stickers(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  belongsToItem = db.Column(db.Integer, unique=False, nullable=False) 
  image = db.Column(db.String(80), unique=False, nullable=False)
  rarityType = db.Column(db.String(80), unique=False, nullable=False) #Rarity type e.g High Grade, etc
  collection = db.Column(db.String(80), unique=False, nullable=False) #Collection e.g Paris, etc

