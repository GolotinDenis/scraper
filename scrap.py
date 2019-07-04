from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://UoDHDfsk3r:GXBANIHkYx@remotemysql.com:3306/UoDHDfsk3r'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from model import Car
db.create_all()

sites = ('https://www.nydailynews.com/autos/types/sports-car', 'http://www.nydailynews.com/autos/types/truck')
@app.route('/scrap')
def scrapSite():
    Car.query.delete()
    for site in sites:
        response = requests.get(site).text
        scrap = BeautifulSoup(response,  features = 'html.parser')
        carsArray =scrap.find('div', {'class':'rtww'}).findChildren('a',recursive=False)
        for cars in carsArray:
            car = Car( year=cars['data-attribute-year'], 
            name=cars.findChild('h3').text.replace(cars['data-attribute-year'],''), 
            desciption=cars.findChild('p',{'class':'description'}).text,
            model = site.split('/')[-1])
            car.save()
    return 'Success';

@app.route('/')
def mainPage():
    superCar = []
    truck = []
    for car in Car.query.filter_by(model='sports-car').all():
        superCar.append({
            'name': car.name,
            'year': car.year,
            'desciption': car.desciption
        })
    for car in Car.query.filter_by(model='truck').all():
        truck.append({
            'name': car.name,
            'year': car.year,
            'desciption': car.desciption
        })
    return render_template('main.html', superCar = superCar, truck = truck)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/get_data')
def getData():
    response = []
    for car in Car.query.all():
        response.append({
            'name': car.name,
            'year': car.year,
            'desciption': car.desciption
        })
    return jsonify(response)

@app.route('/list_data/<model>')
def listData(model):
    user = request.query_string
    print(model, user)
    return model;