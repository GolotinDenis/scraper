import math
import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://UoDHDfsk3r:GXBANIHkYx@remotemysql.com:3306/UoDHDfsk3r'
db = SQLAlchemy(app)

from model import Car

migrate = Migrate(app, db)
db.create_all()


sites = ('https://www.nydailynews.com/autos/types/sports-car',
         'http://www.nydailynews.com/autos/types/truck')

LIMIT = 5;

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
        if hasattr(price,'text'):
            car_model.price = price.text
        else:
            car_model.price = None
        car_model.save()

    return 'Success'

# get number of cars in DB
@app.route('/api/count')
def count():
    countResult = {
        'page':  math.ceil(Car.query.filter_by(model='sports-car').count() / LIMIT) - 1,
        'page_truck': math.ceil(Car.query.filter_by(model='truck').count()  / LIMIT) - 1
    }
    return jsonify(countResult)

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
    } for car in Car.query.filter_by(model='sports-car').limit(LIMIT).offset(page*LIMIT)]

    truck = [{
        'name': car.name,
        'year': car.year,
        'desciption': car.desciption,
        'price': car.price
    } for car in Car.query.filter_by(model='truck').limit(LIMIT).offset(page_truck*LIMIT)]

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
