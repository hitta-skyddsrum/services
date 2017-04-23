# coding: utf-8
import os
from flask import Flask, jsonify
from HittaSkyddsrum.shelters.controllers import mod_shelters
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://" + \
                                        os.environ.get("MYSQL_DATABASE_USER") + ":" + \
                                        os.environ.get("MYSQL_DATABASE_PASSWORD") + "@" + \
                                        os.environ.get("MYSQL_DATABASE_HOST") + "/" + \
                                        os.environ.get("MYSQL_DATABASE_DB")

db = SQLAlchemy(app)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_DATABASE_USER'] = os.environ.get("MYSQL_DATABASE_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get("MYSQL_DATABASE_PASSWORD")
app.config['MYSQL_DATABASE_DB'] = os.environ.get("MYSQL_DATABASE_DB")
app.config['MYSQL_DATABASE_HOST'] = os.environ.get("MYSQL_DATABASE_HOST")
app.config['APPLICATION_ROOT'] = '/api/v1'
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(mod_shelters, url_prefix='/api/v1/shelters')

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': 'Kunde inte hittas'})

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Någonting gick fel, försök igen'})
