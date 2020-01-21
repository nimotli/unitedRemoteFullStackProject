from app import app,db
import app.models as models
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask import jsonify,make_response,redirect,url_for
import jwt #for the jwt token needed for auth
import datetime #for token experation
from validate_email import validate_email

def createUser(user):
    #validate data
    errors=[]
    returnData = None
    users = models.User.query.all()
    #check if the email is unique
    for usr in users:
        if usr.email == user.email:
            errors.append('Email taken')
            break
    #check if the email is valid
    if not validate_email(user.email):
        errors.append('Email is not valid')
    #check if the password is valid
    if len(user.password) < 6:
        errors.append('Password is short')
    #check if the password and confirmation match
    if user.password != user.cPassword:
        errors.append('Password and confirmation does not match')
    #if there are any errors return the errors with a state of failure
    if len(errors) > 0:
        returnData = jsonify({'state':'failure','errors':errors})
        return returnData
    #encrypt the password
    hashedPw = generate_password_hash(user['password'],method='sha256')
    #format the position
    position = '{}-{}'.format(user['x'],user['y'])
    #instantiate the user
    newUser = models.User(public_id=str(uuid.uuid4()),name=user['name'],email=user['email'],position = position,password=hashedPw)
    #add the new user
    db.session.add(newUser)
    db.session.commit()
    #redirect to the login page
    return redirect(url_for('login'), code=302)

#get a user by its public id
def getOneUser(public_id):
    #get the user
    user = models.User.query.filter_by(public_id=public_id).first()
    #check if there are any users
    if not user:
        return jsonify({'error' : 'No user found!'})
    userData = {}
    userData['public_id'] = user.public_id
    userData['email'] = user.email
    userData['password'] = user.password
    userData['name'] = user.name
    userData['position'] = user.position
    return jsonify({'user' : userData})

#Get all the users
def getAllUsers():
    users = models.User.query.all()
    output = []
    for user in users:
        userData = {}
        userData['public_id'] = user.public_id
        userData['name'] = user.name
        userData['email'] = user.email
        userData['password'] = user.password
        userData['position'] = user.position
        output.append(userData)
    return jsonify({'users' : output})
#Delete a user by id
def deleteUser(id):
    user = models.User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'error' : 'No user found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message' : 'deleted successfully'})

#Login
def login(auth):
    #check if the needed data are present
    if not auth or not auth['email'] or not auth['password']:
        return jsonify({'message':'Login required!'}) 
    #query the user with the inserted email
    user = models.User.query.filter_by(email=auth['email']).first()
    #check if a user with the inserted email is in the database
    if not user:
        return jsonify({'message':'No user with that email!'})
    #check the password
    if check_password_hash(user.password, auth['password']):
        #create the jwt token
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'public_id' : user.public_id, 'exp' : exp}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return jsonify({'message':'wrong password'})