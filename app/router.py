from app import app
from flask import render_template,request,make_response
import app.controllers.userController as userController

@app.route('/signup',methods=['GET'])
def signup():
    return render_template('index.html')

#Get all users
@app.route('/user',methods=['GET'])
def getUsers():
    return userController.getAllUsers()
#Create a user
@app.route('/user',methods=['POST'])
def createUser():
    data = request.form
    return userController.createUser(data)
#Get a user
@app.route('/user/<userId>',methods=['GET'])
def getUser(userId):
    return userController.getOneUser(userId)
#Delete a user
@app.route('/user/<userId>',methods=['DELETE'])
def deleteUser(userId):
    return userController.deleteUser(userId)


@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def signin():
    auth = request.form
    return userController.login(auth)