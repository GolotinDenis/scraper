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

limit = 5;

# Get cars info from sites
@app.route('/scrap_sites')
def scrap_sites():
    Car.query.delete()

    for car, site in car_cilce():
        carModel = Car()
        carModel.year = car['data-attribute-year']
        carModel.name = car.findChild('h3').text
        carModel.desciption = car.findChild('p', {'class': 'description'}).text
        carModel.model = site
        carModel.save()

    return 'Success'

# get number of cars in DB
@app.route('/count')
def count():
    countResult = {
        'page':  math.ceil(Car.query.filter_by(model='sports-car').count() / limit)-1,
        'pageTruck': math.ceil(Car.query.filter_by(model='truck').count()  / limit)-1
    }
    return jsonify(countResult)

# get main page
@app.route('/')
def main_page():
    page = int(request.args.get('page') or 0);
    pageTruck = int(request.args.get('pageTruck') or 0);
    print(page, pageTruck);
    super_car = [{
        'name': car.name,
        'year': car.year,
        'desciption': car.desciption
    } for car in Car.query.filter_by(model='sports-car').limit(limit).offset(page*limit)]

    truck = [{
        'name': car.name,
        'year': car.year,
        'desciption': car.desciption
    } for car in Car.query.filter_by(model='truck').limit(limit).offset(pageTruck*limit)]

    return render_template('main.html', super_car=super_car, truck=truck)


# generator for sites
def get_site():
    for site in sites:
        try:
            response = requests.get(site).text
            scrap = BeautifulSoup(response,  features='html.parser')
            yield scrap.find('div', {'class': 'rtww'}).findChildren('a', recursive=False), site.split('/')[-1]
        except (KeyError, TypeError):
            print('An error occurred while trying to parse the site.')


# generator for cars what was found at sites
def car_cilce():
    for cars, site in get_site():
        for car in cars:
            yield car, site
