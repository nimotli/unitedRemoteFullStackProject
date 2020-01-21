from app import app,db
import app.models as models
from flask import jsonify,make_response
import jwt #for the jwt token needed for auth
import datetime #for token experation

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