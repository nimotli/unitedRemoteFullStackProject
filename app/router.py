#a router that contains all the needed routes for the API
from app import app
from flask import render_template,request,make_response,jsonify
import app.controllers.userController as userController
import app.controllers.shopController as shopController
from functools import wraps
import jwt
import app.models as models

#a decorator that make a route need an access token for it to work
def needToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'accessToken' in request.headers:
            token = request.headers['accessToken']
            print('the token is :',token[0:10])
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        print("will decode the token using",app.config['SECRET_KEY'])
        data = jwt.decode(token, app.config['SECRET_KEY'])
        print('token decoded')
        currentUser = models.User.query.filter_by(public_id=data['public_id']).first()
        print('got the current user',currentUser)

        return f(currentUser, *args, **kwargs)

    return decorated

#Get all users
@app.route('/user',methods=['GET'])
@needToken
def getUsers(current_user):
    return userController.getAllUsers()
    
#Create a user
@app.route('/user',methods=['POST'])
def createUser():
    data = request.form
    return userController.createUser(data)
#Get a user
@app.route('/user/<userId>',methods=['GET'])
@needToken
def getUser(userId):
    return userController.getOneUser(userId)
#Delete a user
@app.route('/user/<userId>',methods=['DELETE'])
@needToken
def deleteUser(userId):
    return userController.deleteUser(userId)

#sign up page
@app.route('/signup',methods=['GET'])
def signup():
    return render_template('register.html')
#home page : it contains signin form and the shops
@app.route('/home',methods=['GET'])
def login():
    return render_template('login.html')
#sign in route
@app.route('/home',methods=['POST'])
def signin():
    auth = request.form
    return userController.login(auth)
#Create a shop
@app.route('/shop',methods=['POST'])
def createShop():
    data = request.form
    return shopController.createShop(data)
#Get all shops
@app.route('/shop',methods=['GET'])
@needToken
def getShops(current_user):
    token = request.headers['accessToken']
    return shopController.getAllShops(token)
#like a shop
@app.route('/like',methods=['POST'])
@needToken
def likeShop(current_user):
    token = request.headers['accessToken']
    shopId = request.form['shopId']
    return shopController.likeShop(token,shopId)
#get all user shops-for debug
@app.route('/userShop',methods=['GET'])
@needToken
def getUserShops(current_user):
    token = request.headers['accessToken']
    return shopController.getAllUserShops()

