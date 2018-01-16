from HittaSkyddsrum import db
import urllib2
import json


class Position():
    def __init__(self, long, lat):
        self.long = long
        self.lat = lat

    def serialize(self):
        return {
            'long': self.long,
            'lat': self.lat
        }


class Shelter(db.Model):
    __tablename__ = "shelters"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    municipality = db.Column(db.String(255))
    city = db.Column(db.String(255))
    slots = db.Column(db.Integer())
    air_cleaners = db.Column(db.Integer())
    filter_type = db.Column(db.Integer())
    shelter_id = db.Column(db.String(255))
    estate_id = db.Column(db.String(255))
    goid = db.Column(db.String(255))
    position_long = db.Column(db.DECIMAL())
    position_lat = db.Column(db.DECIMAL())
    sweref99Position_x = db.Column(db.DECIMAL())
    sweref99Position_y = db.Column(db.DECIMAL())

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def position(self):
        return Position(self.position_long, self.position_lat)

    @staticmethod
    def find_nearby(position, amount):
        sql = """
        SELECT 
            s.*, 
            ( 
                3959 * 
                acos(
                    cos(radians(%(lat)s)) * 
                    cos(radians(position_lat)) * 
                    cos(radians(position_long) - 
                    radians(%(long)s) 
                ) +  
                    sin(radians(%(lat)s)) * 
                    sin(radians(position_lat)) 
                ) 
            ) 
            AS distance 
        FROM shelters s 
        ORDER BY distance ASC 
        LIMIT %(amount)s
    """


        shelters_execution = db.engine.execute(sql, {'lat': position.lat, 'long': position.long, 'amount': amount})

        return [Shelter(**shelterData) for shelterData in
                [dict(zip([column for column in shelters_execution.keys()], row))
                 for row in shelters_execution.fetchall()]
                ]

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'municipality': self.municipality,
            'city': self.city,
            'slots': self.slots,
            'airCleaners': self.air_cleaners,
            'filterType': self.filter_type,
            'estateId': self.estate_id,
            'goid': self.goid,
            'shelterId': self.shelter_id,
            'position': self.position.serialize()
        }


class Hospital():
    def __init__(self, hsaId, name, address, lat, long):
        self.hsaId = hsaId
        self.name = name
        self.address = address
        self.position = Position(lat=lat, long=long)

    @staticmethod
    def find_nearby(position):
        business_classification_code = 1100

        for distance in range(500, 1000, 100):
            url = "http://api.offentligdata.minavardkontakter.se/orgmaster-hsa/v1/hsaObjects?lat={0}&long={1}&distance={2}&businessClassificationCode={3}" \
                .format(position.lat, position.long, distance, business_classification_code)

            hospitals = json.load(urllib2.urlopen(url))

            if (len(hospitals) > 0):
                return [Hospital(
                    hsaId=_hospital.get('hsaId'),
                    name=_hospital.get('relativeDistinguishedName'),
                    address=_hospital.get('street'),
                    lat=_hospital.get('geoLocation').get('latitude'),
                    long=_hospital.get('geoLocation').get('longitude')
                )
                        for _hospital in hospitals]

        return False

    def serialize(self):
        return {
            'position': self.position.serialize(),
            'hsaId': self.hsaId,
            'address': self.address,
            'name': self.name
        }
