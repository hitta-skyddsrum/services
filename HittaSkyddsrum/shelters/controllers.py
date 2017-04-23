from flask import Blueprint, request, jsonify, abort

mod_shelters = Blueprint('shelters', __name__)

@mod_shelters.route('/', methods=['GET'])
def index():
    from models import Shelter, Position

    long = request.args.get('long')
    lat = request.args.get('lat')

    if not long and not lat:
        return jsonify({'message': 'Bad query params'}), 401

    shelters = Shelter.find_nearby(Position(long=long, lat=lat), 10)

    return jsonify([shelter.serialize() for shelter in shelters])


@mod_shelters.route('/<int:id>', methods=['GET'])
def get(id):
    from models import Shelter
    shelter = Shelter.query.get(id)

    if shelter is False:
        abort(404)

    return jsonify(shelter.serialize())


@mod_shelters.route('/<int:id>/hospitals', methods=['GET'])
def getHospitals(id):
    from models import Shelter, Hospital

    shelter = Shelter.query.filter_by(id=id).first()
    hospitals = Hospital.find_nearby(shelter.position)

    if hospitals is False:
        return abort(404)

    return jsonify([hospital.serialize() for hospital in hospitals])

