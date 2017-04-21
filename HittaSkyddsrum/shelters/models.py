from HittaSkyddsrum import db
import urllib2
import json
import types

class BaseModel:
    def __init__(self):
        self.public_attrs = []

    def __iter__(self):
        return self

    def next(self):
        if self._index is None:
            self._index = 0

        if self._index == len(self.public_attrs):
            raise StopIteration

        output = []
        output[self.public_attrs[self._index]] = self[self.public_attrs[self._index]]

        return output


class Position():
    def __init__(self, long, lat):
        self.long = long
        self.lat = lat

    def serialize(self):
        return {
            "long": self.long,
            "lat": self.lat
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

    def get(self, key):
        value = getattr(self, key)

        if isinstance(value, types.FunctionType):
            return value()

        return value

    @property
    def position(self):
        return Position(self.position_long, self.position_lat)

    @staticmethod
    def findNearby(position, amount):
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
    """

        sheltersExecution = db.engine.execute(sql, {'lat': position.lat, 'long': position.long})

        return [Shelter().serialize(dict(zip([column for column in sheltersExecution.keys()], row)))
                for row in sheltersExecution.fetchmany(amount)]

    def serialize(self, obj=None):
        if obj is None:
            obj = self

        return {
            "id": obj.get('id'),
            "address": obj.get('address'),
            "municipality": obj.get('municipality'),
            "city": obj.get('city'),
            "slots": obj.get('slots'),
            "airCleaners": obj.get('air_cleaners'),
            "filterType": obj.get('filter_type'),
            "estateId": obj.get('estate_id'),
            "goid": obj.get('goid'),
            "shelterId": obj.get('shelter_id'),
            "position": obj.get('position').serialize()
        }


class Hospital():
    @staticmethod
    def findNearby(position):
        businessClassificationCode = 1100

        for distance in range(900, 1000, 100):
            url = "http://api.offentligdata.minavardkontakter.se/orgmaster-hsa/v1/hsaObjects?lat={0}&long={1}&distance={2}&businessClassificationCode={3}" \
                .format(position.lat, position.long, distance, businessClassificationCode)

            hospitals = json.load(urllib2.urlopen(url))

            if (len(hospitals) > 0):
                return [Hospital.serialize(_hospital) for _hospital in hospitals]

        return False

    @staticmethod
    def serialize(obj):
        return {
            "position": {
                "long": obj.get("geoLocation").get("longitude"),
                "lat": obj.get("geoLocation").get("latitude")
            },
            "hsaId": obj.get("hsaId"),
            "address": obj.get("street"),
            "name": obj.get("relativeDistinguishedName")
        }
