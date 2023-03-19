from flask_restful import Api, Resource, reqparse
from flask import make_response, jsonify
from flask import current_app

from weather.getting_weather import main as getting_weather

from app.weather.models import City, Country


# /api/v1/countries
# GET = all_countries 200
# POST = add_city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204

class Countries(Resource):
    """API for countries"""

    def __init__(self):
        self.countries = None
        self.request = None
        self.api_key = current_app.config['WEATHER_API_KEY']
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def prepare_countries_to_json(self):
        """Prepare countries to json format"""
        countries = []
        for country in self.countries:
            country_temp = {
                'id': country.id,
                'country_code': country.code,
                'name': country.name
            }
            countries.append(country_temp)
        return countries

def init_app(app):
    with app.app_context():
        api = Api(app, decorators=[current_app.config['CSRF'].exempt])
        api.add_resource(Countries, '/api/v1/countries')