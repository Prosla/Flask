from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
    current_app
)

from app.weather import weather
from app.weather.forms import CityForm
from weather.getting_weather import main as getting_weather
from app.weather.models import Country, City
from flask_paginate import Pagination, get_page_parameter
from app.main.utils import parse_range_from_paginator


@weather.route('/weather', methods=['GET', 'POST'])
def index():
    """Weather page"""
    form = CityForm()
    city_weather = None
    country = None
    city_name = None

    if form.validate_on_submit():
        api_key = current_app.config['WEATHER_API_KEY']
        city_name = form.city_name.data
        city_weather = getting_weather(city_name, api_key)
        if 'error' in city_weather:
            flash(city_weather['error'])
            return redirect(url_for('weather.index'))
        country = Country.select().where(Country.code == city_weather['country']).first()
        city_weather['country'] = country.name

    return render_template(
        'weather/get_weather.html',
        title='Get city weather',
        form=form,
        city_name=city_name,
        country=country,
        city_weather=city_weather
    )


@weather.route('/weather/add/city', methods=['POST'])
def add_city():
    """Add city to monitoring"""
    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')

        city_instance = City(
            name=city,
            country=country
        )
        city_instance.save()
        flash(f'City: {city} added to db')

    return redirect(url_for('weather.index'))


@weather.route('/show_cities')
def show_cities():
    """Show cities information"""
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    cities = City.select()
    pagination = Pagination(page=page, total=cities.count(), search=search, record_name='users')
    start, stop = parse_range_from_paginator(pagination.info)
    return render_template(
        'weather/show_cities.html',
        title='Show cities',
        users=cities[start:stop],
        pagination=pagination,
    )


@weather.route('/delete_cities', methods=['POST'])
def delete_cities():
    """Delete selected cities"""
    if request.method == 'POST':
        message = 'Deleted: '
        selectors = list(map(int, request.form.getlist('selectors')))

        if not selectors:
            flash('Nothing to delete')
            return redirect(url_for('weather.show_cities'))

        for selector in selectors:
            city = City.get(City.id == selector)
            message += f'{city.name} '
            city.delete_instance()

        flash(message)
        return redirect(url_for('weather.show_cities'))
