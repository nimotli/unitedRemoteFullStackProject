from app import app
from flask import render_template,request,make_response,jsonify
import app.controllers.userController as userController
from functools import wraps

def needToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'accessToken' in request.headers:
            token = request.headers['accessToken']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            currentUser = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(currentUser, *args, **kwargs)

    return decorated

#Get all users
@app.route('/user',methods=['GET'])
@needToken
def getUsers():
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


@app.route('/signup',methods=['GET'])
def signup():
    return render_template('register.html')

@app.route('/signin',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/signin',methods=['POST'])
def signin():
    auth = request.form
    return userController.login(auth)