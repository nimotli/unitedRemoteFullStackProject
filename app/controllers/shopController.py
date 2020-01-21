from app import app,db
import app.models as models
from flask import jsonify,make_response
import jwt #for the jwt token needed for auth
import datetime #for token experation
import math

#a helper function thats used in sorting the shops by distance
def sortKey(elem):
    return elem['position']

#create a shop
def createShop(shop):
    returnData = None
    returnData = jsonify({'state':'success','errors':None})
    position = '{}|{}'.format(shop['x'],shop['y'])
    newShop = models.Shop(name=shop['name'],shopType=shop['shopType'],position = position)
    db.session.add(newShop)
    db.session.commit()
    return returnData
#Get all the shops that the user hasnt liked yet
def getAllShops(token):
    #decode the jwt token and use the public id of the current user stored in it to query the current user
    data = jwt.decode(token, app.config['SECRET_KEY'])
    user = models.User.query.filter_by(public_id=data['public_id']).first()
    #query all the shops and user shops
    shops = models.Shop.query.all()
    userShops = models.UserShop.query.all()
    #get all the shops that the current user has liked
    likedSp=[]
    for us in userShops:
        if us.user == user.id:
            likedSp.append(us.shop)

    userX = int(user.position.split('-')[0]) #used for calculating the distance between the shops and the users
    userY = int(user.position.split('-')[1]) #used for calculating the distance between the shops and the users
    output = []
    for shop in shops:
        if shop.id not in likedSp:
            shopsData = {}
            shopsData['id'] = shop.id
            shopsData['name'] = shop.name
            shopsData['shopType'] = shop.shopType
            shopX = int(shop.position.split('|')[0]) #used for calculating the distance between the shops and the users
            shopY = int(shop.position.split('|')[1]) #used for calculating the distance between the shops and the users
            #calculate the distance between the shop and the user
            distance = math.sqrt((userX-shopX)**2 + (userY-shopY)**2)
            shopsData['position'] = round(distance,2)
            output.append(shopsData)
    output.sort(key = sortKey)
    print('the selected shops are :',output)
    return jsonify({'shops' : output})

#like a shop
def likeShop(token,shopId):
    data = jwt.decode(token, app.config['SECRET_KEY'])
    user = models.User.query.filter_by(public_id=data['public_id']).first()
    shop = models.Shop.query.filter_by(id=shopId).first()
    newUserShop = models.UserShop(user = user.id,shop = shop.id,interraction = 1)
    db.session.add(newUserShop)
    db.session.commit()
    return jsonify({'message':'liked!'})

#get all userShops for debug purposes
def getAllUserShops():
    userShops = models.UserShop.query.all()
    output = []
    for shop in userShops:
        shopsData = {}
        shopsData['user'] = shop.user
        shopsData['shop'] = shop.shop
        shopsData['interraction'] = shop.interraction
        output.append(shopsData)
    return jsonify({'userShops' : output})