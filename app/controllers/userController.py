from app import app,db
import app.models as models
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask import jsonify,make_response
import jwt #for the jwt token needed for auth
import datetime #for token experation

def createUser(user):
    errors=[]
    #validate data
    returnData = None
    if False:
        returnData = jsonify({'state':'failure','errors':errors})
    else:
        returnData = jsonify({'state':'success','errors':None})
    hashedPw = generate_password_hash(user['password'],method='sha256')
    position = '{}-{}'.format(user['x'],user['y'])
    newUser = models.User(public_id=str(uuid.uuid4()),name=user['name'],email=user['email'],position = position,password=hashedPw)
    db.session.add(newUser)
    db.session.commit()
    return returnData

def getOneUser(public_id):
    user = models.User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'error' : 'No user found!'})
    userData = {}
    userData['public_id'] = user.public_id
    userData['email'] = user.email
    userData['password'] = user.password
    userData['name'] = user.name
    userData['position'] = user.position
    return jsonify({'user' : userData})

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

def deleteUser(id):
    user = models.User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'error' : 'No user found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message' : 'deleted successfully'})

def login(auth):
    if not auth or not auth['email'] or not auth['password']:
        return jsonify({'message':'Login required!'}) #make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = models.User.query.filter_by(email=auth['email']).first()
    if not user:
        return jsonify({'message':'No user with that email!'})#return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="No user with that email!"'})
    if check_password_hash(user.password, auth['password']):
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'public_id' : user.public_id, 'exp' : exp}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return jsonify({'message':'wrong password'})#return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="wrong password"'})