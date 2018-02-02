import unittest
import json
from flask import jsonify
from flask_testing import TestCase
from HittaSkyddsrum import db, app
from HittaSkyddsrum.shelters.models import Shelter

class SheltersTest(TestCase):

    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_shelters_by_coordinates(self):
        close_shelter = Shelter(position_long=18.200, position_lat=59.46)
        db.session.add(close_shelter)
        db.session.commit()
        response = self.client.get('/api/v1/shelters/?lat=59.3618&lon=18.1205̈́')

        self.assert200(response)
        response_text = response.get_data(as_text=True)
        shelters = json.loads(response_text)
        self.assertEquals(shelters, [close_shelter.serialize()])

    def test_get_single_shelter(self):
        shelter = Shelter(address='Langgatan 1', municipality='Hogdreva', city='Langas', slots=15, air_cleaners=99, filter_type=1, shelter_id='shelter-id-3', estate_id='Real estate', goid='Go id')
        db.session.add(shelter)
        db.session.commit()
        response = self.client.get('/api/v1/shelters/' + str(shelter.id))

        self.assertStatus(response, 200)
        self.assertEquals(json.loads(response.get_data(as_text=True)), shelter.serialize())

if __name__ == '__main__':
    unittest.main()
