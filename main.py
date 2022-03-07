"""
Main python file for our flask project

@author: Felix Estrella, Jackson Goth, Shivani Ganesh, Eric Bal
"""

from distutils.log import error
from random import randint
from flask import Flask, render_template, request
import requests

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
    # Get info from form
    term = request.form.get('term')
    location = request.form.get('location')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    radius = request.form.get('radius')
    # Set params
    params['term'] = term
    if location == '':
        params['latitude'] = float(latitude)
        params['longitude'] = float(longitude)
    else:
        params['location'] = location
    if radius != None and radius != '':
        params['radius'] = int(min(max(float(radius) * 1609.34, 0), 40000))
    params['limit'] = 50
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    data = response.json()
    if data is None or 'total' not in data.keys():
        return render_template('home.html', error = error, errorMsg = 'error when getting dictionary response from yelp')
    if data['total'] == 0:
        return render_template('home.html', error = error, errorMsg = 'no businesses found')
    randBusiness = data['businesses'][randint(0,len(data['businesses']) - 1)]
    print(randBusiness['image_url'])
    return render_template('home.html', error = error, name = randBusiness['name'], imgUrl = randBusiness['image_url'])


def general_api():
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    print(response.status_code)
    data = response.json() # It is a dictionary
    print(data.keys()) # Keys are ['businesses', 'total', 'region']
    print(data['businesses'][0])

if __name__ == "__main__":
    app.run()
