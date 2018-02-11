from flask import Blueprint, request, jsonify, abort

mod_shelters = Blueprint('shelters', __name__)

@mod_shelters.route('/api/v2/shelters/', methods=['GET'])
def index():
    from models import Shelter, Position

    long = request.args.get('long')
    lat = request.args.get('lat')

    if not long and not lat:
        return jsonify({'message': 'Bad query params'}), 401

    shelters = Shelter.find_nearby(Position(long=long, lat=lat), 10)

    return jsonify([shelter.serialize() for shelter in shelters])

@mod_shelters.route('/api/v1/shelters/', methods=['GET'])
def old_index():
    from models import Shelter, Position

    long = request.args.get('long')
    lat = request.args.get('lat')

    if not long and not lat:
        return jsonify({'message': 'Bad query params'}), 401

    shelters = Shelter.find_nearby(Position(long=long, lat=lat), 10)

    return jsonify([shelter.serialize() for shelter in shelters])

@mod_shelters.route('/api/v1/shelters/all-shelters', methods=['GET'])
def index_all():
    from models import Shelter
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))

    shelters = Shelter.query.paginate(page, per_page).items

    return jsonify([shelter.serialize() for shelter in shelters])

@mod_shelters.route('/api/v2/shelters/<string:id>', methods=['GET'])
def get(id):
    from models import Shelter
    shelter = Shelter.query.filter_by(shelter_id=id).first()

    if shelter is False:
        abort(404)
    print shelter 

    return jsonify(shelter.serialize())

@mod_shelters.route('/api/v1/shelters/<int:id>', methods=['GET'])
def getById(id):
    from models import Shelter
    shelter = Shelter.query.get(id)

    if shelter is False:
        abort(404)

    return jsonify(shelter.serialize())

@mod_shelters.route('/api/v2/shelters/<string:id>/hospitals', methods=['GET'])
def getHospitals(id):
    from models import Shelter, Hospital

    shelter = Shelter.query.filter_by(shelter_id=id).first()
    hospitals = Hospital.find_nearby(shelter.position)

    if hospitals is False:
        return abort(404)

    return jsonify([hospital.serialize() for hospital in hospitals])

@mod_shelters.route('/api/v1/shelters/<int:id>/hospitals', methods=['GET'])
def old_getHospitals(id):
    from models import Shelter, Hospital

    shelter = Shelter.query.filter_by(id=id).first()
    hospitals = Hospital.find_nearby(shelter.position)

    if hospitals is False:
        return abort(404)

    return jsonify([hospital.serialize() for hospital in hospitals])

