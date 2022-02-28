"""
Main python file for our flask project
-test
@author: Felix Estrella
"""

from ast import For
from distutils.log import error
from random import randint
from flask import Flask, render_template, request
import requests
from Form_Data import Form_Data

app = Flask(__name__)

# Put in your the api_key here
api_key = ''
headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
params = {}

@app.route("/")
def home():
    #general_api()
    return render_template('home.html', error = error)

@app.route('/', methods =["GET", "POST"])
def get_form():
    # Create form object
    fd = Form_Data()
    # Get info from form
    fd.set_term(request.form.get('term'))
    fd.set_location(request.form.get('location'))
    fd.set_latitude(request.form.get('latitude'))
    fd.set_longitude(request.form.get('longitude'))
    fd.set_radius(request.form.get('radius'))
    fd.set_categories(request.form.get('categories'))
    fd.set_price(request.form.get('price'))
    # Set params
    fill_params(fd)
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    data = response.json()
    randBusiness = data['businesses'][randint(0,len(data['businesses']) - 1)]
    print(randBusiness['image_url'])
    return render_template('home.html', error = error, name = randBusiness['name'], imgUrl = randBusiness['image_url'])

def fill_params(fd):
    params['term'] = fd.term
    params['location'] = fd.location
    params['latitude'] = fd.latitude
    params['longitude'] = fd.longitude
    params['radius'] = fd.radius
    params['categories'] = fd.categories
    params['price'] = fd.price
    params['limit'] = 50

def general_api():
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    print(response.status_code)
    data = response.json() # It is a dictionary
    print(data.keys()) # Keys are ['businesses', 'total', 'region']
    print(data['businesses'][0])

if __name__ == "__main__":
    app.run()


