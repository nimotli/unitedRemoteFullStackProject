#the model classes needed for the project
from app import app,db# importing the current global flask object and db
from flask_sqlalchemy import SQLAlchemy # for database interractions

#creating the class models

#for the users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))

#for the shops
class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    shopType = db.Column(db.String(50))
    position = db.Column(db.String(50))
#for the interractions of the users with the shops (like,dislike)
class UserShop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    shop = db.Column(db.Integer, db.ForeignKey('shop.id'),nullable=False)
    interraction = db.Column(db.Integer)

def createDB():
    db.create_all()