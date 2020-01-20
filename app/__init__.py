from flask import Flask
from flask_sqlalchemy import SQLAlchemy # for database interractions
import os

app = Flask(__name__)

dbURI = 'sqlite:///{}/db/mainDb.db'.format(os.path.dirname(os.path.abspath(__file__)))
app.config['SECRET_KEY'] = 'secretcode'
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
db = SQLAlchemy(app)

