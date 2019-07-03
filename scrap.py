from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://UoDHDfsk3r:GXBANIHkYx@remotemysql.com:3306/UoDHDfsk3r'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
from model import Car
# db.create_all()

# sites = ('https://www.nydailynews.com/autos/types/sports-car', 'http://www.nydailynews.com/autos/types/sports-car')
sites = []
for site in sites:
    response = requests.get(site).text
    scrap = BeautifulSoup(response,  features = 'html.parser')
    carsArray =scrap.find('div', {'class':'rtww'}).findChildren('a',recursive=False)
    for cars in carsArray:
        car = Car( year=cars['data-attribute-year'], name=cars.findChild('h3').text, desciption=cars.findChild('p',{'class':'description'}).text)
        car.save()

@app.route('/')
def scrapFunction():
    return 'Hello word'