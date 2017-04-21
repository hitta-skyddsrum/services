from flask import Blueprint, request, jsonify, abort

mod_shelters = Blueprint('shelters', __name__, url_prefix='/api/v1/shelters')

@mod_shelters.route('/', methods=['GET'])
def index():
    from models import Shelter, Position

    long = request.args.get('long')
    lat = request.args.get('lat')

    if not long and not lat:
        return "Bad query params", 401

    shelters = Shelter.findNearby(Position(long=long, lat=lat), 10)

    return jsonify(shelters)


@mod_shelters.route('/<int:id>', methods=['GET'])
def get(id):
    from models import Shelter
    shelter = Shelter.query.filter_by(id=id).first()

    dictShelt = shelter.serialize()

    return jsonify(dictShelt)


@mod_shelters.route('/<int:id>/hospitals', methods=['GET'])
def getHospitals(id):
    from models import Shelter, Hospital

    shelter = Shelter.query.filter_by(id=id).first()
    hospitals = Hospital.findNearby(shelter.position)

    if hospitals is False:
        return abort(404)

    return jsonify(hospitals)

