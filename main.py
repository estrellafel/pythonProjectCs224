"""
Main python file for our flask project

@author: Felix Estrella
"""

from distutils.log import error
from random import randint
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Put in your the api_key
api_key = 'Iu6RMASUHPZgnXkTKsopdmBGiQK9ht97MCXkyFX_ciEltMPd3YcleBYZHmMcmlrwSmdJqAf_YOv7-CuzP6L64k1Vo64fLATAqoKVYAGwJ3ddbmQ1YmAzBku_Y9sKYnYx'
headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
params = {}

@app.route("/")
def home():
    #general_api()
    return render_template('home.html', error = error)

@app.route('/', methods =["GET", "POST"])
def getForm():
    term = request.form.get('foodType')
    location = request.form.get('location')
    print(term + " " + location)
    params['term'] = term
    params['location'] = location
    params['limit'] = 50
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    data = response.json()
    randBusiness = data['businesses'][randint(0,len(data['businesses']) - 1)]
    return render_template('home.html', error = error, name = randBusiness['name'])


def general_api():
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    print(response.status_code)
    data = response.json() # It is a dictionary
    print(data.keys()) # Keys are ['businesses', 'total', 'region']
    print(data['businesses'][0])

if __name__ == "__main__":
    app.run()


