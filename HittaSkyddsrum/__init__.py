# coding: utf-8
import os
from flask import Flask, jsonify
from HittaSkyddsrum.shelters.controllers import mod_shelters
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_DATABASE_USER'] = os.environ.get("MYSQL_DATABASE_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get("MYSQL_DATABASE_PASSWORD")
app.config['MYSQL_DATABASE_DB'] = os.environ.get("MYSQL_DATABASE_DB")
app.config['MYSQL_DATABASE_HOST'] = os.environ.get("MYSQL_DATABASE_HOST")
app.config['APPLICATION_ROOT'] = '/api/v1'
app.config['JSON_AS_ASCII'] = True

CORS(app)

DB_URL = 'mysql+mysqldb://{}:{}@{}/{}'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL.format(app.config['MYSQL_DATABASE_USER'], app.config['MYSQL_DATABASE_PASSWORD'], app.config['MYSQL_DATABASE_HOST'], app.config['MYSQL_DATABASE_DB'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.register_blueprint(mod_shelters)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': 'Kunde inte hittas'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Någonting gick fel, försök igen'}), 500
