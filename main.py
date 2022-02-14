"""
Main python file for our flask project

@author: Felix Estrella
"""

from distutils.log import error
from flask import Flask, render_template
import requests

app = Flask(__name__)

# Put in your the api_key
api_key = ''
headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
params = {'term': 'food', 
          'location': 'La Crosse, Wisconsin',
          'limit': 25}

@app.route("/")
def home():
    general_api()
    return render_template('home.html', error = error)

def general_api():
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    print(response.status_code)
    data = response.json() # It is a dictionary
    print(data.keys()) # Keys are ['businesses', 'total', 'region']
    print(data['businesses'][0])

if __name__ == "__main__":
    app.run()


