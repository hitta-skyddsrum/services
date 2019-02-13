from __future__ import absolute_import
from flask import Blueprint, request, jsonify, abort

mod_shelters = Blueprint('shelters', __name__)

@mod_shelters.route('/api/v3/shelters/', methods=['GET'])
def indexBbox():
    bbox = request.args.get('bbox')

    if not bbox:
        return jsonify({'message': 'Bad query params.'}), 401

    from .models import Shelter

    shelters = Shelter.find_in_bbox(bbox)

    return jsonify([shelter.serialize() for shelter in shelters])

@mod_shelters.route('/api/v2/shelters/', methods=['GET'])
def index():
    from .models import Shelter, Position

    long = request.args.get('long')
    lat = request.args.get('lat')


    if not long and not lat:
        return jsonify({'message': 'Bad query params'}), 401

    shelters = Shelter.find_nearby(Position(long=long, lat=lat), 20)

    return jsonify([shelter.serialize() for shelter in shelters])

@mod_shelters.route('/api/v2/shelters/<string:id>', methods=['GET'])
def get(id):
    from .models import Shelter
    shelter = Shelter.query.filter_by(shelter_id=id).first()

    if shelter is None:
        abort(404)

    return jsonify(shelter.serialize())

