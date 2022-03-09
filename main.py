"""
Main python file for our flask project

@author: Felix Estrella, Jackson Goth, Shivani Ganesh, Eric Bal
"""

from distutils.log import error
from random import randint
from flask import Flask, render_template, request
import requests, validate

app = Flask(__name__)

# Put in your the api_key here
api_key = ''
headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
# params = {}

@app.route("/")
def home():
    #general_api()
    return render_template('home.html', error = error)

@app.route('/', methods =["GET", "POST"])
def get_form():
    # Get input from the form and parse that into a dictionary for the request
    params = get_params(request.form)
    if params == None:
        return render_template('home.html', error = error, errorMsg = 'Error while parsing user input!')
    
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    data = response.json()
    if data is None or 'total' not in data.keys():
        return render_template('home.html', error = error, errorMsg = 'error when getting dictionary response from yelp')
    if data['total'] == 0:
        return render_template('home.html', error = error, errorMsg = 'no businesses found')
    randBusiness = data['businesses'][randint(0,len(data['businesses']) - 1)]
    print(randBusiness['image_url'])
    return render_template('home.html', error = error, name = randBusiness['name'], imgUrl = randBusiness['image_url'])    

# Attempts to get dictionary of valid data.  
# If valid data entered will return the dictionary, otherwise returns None
def get_params(form):
    # Get raw unvalidated input from form
    term = form.get('term')
    location = form.get('location')
    radius = form.get('radius')
    categories = form.get('categories')
    price = form.get('price')
    
    # Parse unvalidated input and store valid input in params dictionary
    params = {}
    params['term'] = term
    params['limit'] = 50 # Always limit results
    
    if location != None and location != '': # If a direct location is available, use that
        params['location'] = location
    else: # Otherwise throw an error to enter location
        return render_template('home.html', error = error, errorMsg = 'error when getting dictionary response from yelp')
    
    # For these entries if invalid data is encountered, it is just not included in params
    if validate.is_valid_float(radius): # If a radius is provided, try to use it
            params['radius'] = int(min(max(float(radius) * 1609.34, 0), 40000)) 
    if categories != None and categories != '': # If a category is provided, use it
        params['categories'] = categories
    if validate.is_valid_int(price): # If a price range is provided, try to use it
            params['price'] = validate.parse_price(price)
    
    return params

def general_api():
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    print(response.status_code)
    data = response.json() # It is a dictionary
    print(data.keys()) # Keys are ['businesses', 'total', 'region']
    print(data['businesses'][0])

if __name__ == "__main__":
    app.run()
