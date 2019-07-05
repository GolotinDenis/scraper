import math
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

DB_NAME = os.environ.get('DB_NAME')
PAGE_SIZE = 5;

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
db = SQLAlchemy(app)

from model import Car

migrate = Migrate(app, db)
db.create_all()


sites = ('https://www.nydailynews.com/autos/types/sports-car',
         'http://www.nydailynews.com/autos/types/truck')

# Get cars info from sites
@app.route('/api/scrap_sites')
def scrap_sites():
    Car.query.delete()

    for car, site in car_generator():
        car_model = Car()
        carPage = car['href']
        page = requests.get(car['href']).text
        price = BeautifulSoup(page,  features='html.parser').find('div', {'class': 'ra-price'})

        car_model.year = car['data-attribute-year']
        car_model.name = car.findChild('h3').text
        car_model.desciption = car.findChild('p', {'class': 'description'}).text
        car_model.model = site
        car_model.price = price.text if hasattr(price,'text') else None
        car_model.save()

    return 'Success'

# get number of cars in DB
@app.route('/api/count')
def count():
    return jsonify({
        'page':  math.ceil(Car.query.filter_by(model='sports-car').count() / PAGE_SIZE) - 1,
        'page_truck': math.ceil(Car.query.filter_by(model='truck').count()  / PAGE_SIZE) - 1
    })

# get main page
@app.route('/')
def main_page():
    page = int(request.args.get('page', 0));
    page_truck = int(request.args.get('page_truck', 0));
    super_car = [{
        'name': car.name,
        'year': car.year,
        'desciption': car.desciption,
        'price': car.price
    } for car in Car.query.filter_by(model='sports-car').limit(PAGE_SIZE).offset(page*PAGE_SIZE)]

    truck = [{
        'name': car.name,
        'year': car.year,
        'desciption': car.desciption,
        'price': car.price
    } for car in Car.query.filter_by(model='truck').limit(PAGE_SIZE).offset(page_truck*PAGE_SIZE)]

    return render_template('main.html', super_car=super_car, truck=truck)


# generator for sites
def site_generator():
    for site in sites:
        try:
            response = requests.get(site).text
            scrap = BeautifulSoup(response,  features='html.parser')
            yield scrap.find('div', {'class': 'rtww'}).findChildren('a', recursive=False), site.split('/')[-1]
        except (KeyError, TypeError):
            print('An error occurred while trying to parse the site.')


# generator for cars what was found at sites
def car_generator():
    for cars, site in site_generator():
        for car in cars:
            yield car, site
