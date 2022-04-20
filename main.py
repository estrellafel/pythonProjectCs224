"""
Main python file for our flask project

@author: Felix Estrella, Jackson Goth, Shivani Ganesh, Eric Bal
"""

from distutils.log import error
from random import randint
from tkinter.tix import Form
from flask import Flask, render_template, request
import requests, validate
from Form_Data import Form_Data
from Restaurant import Restaurant

app = Flask(__name__)

# Put in your the api_key here
api_key = 'Iu6RMASUHPZgnXkTKsopdmBGiQK9ht97MCXkyFX_ciEltMPd3YcleBYZHmMcmlrwSmdJqAf_YOv7-CuzP6L64k1Vo64fLATAqoKVYAGwJ3ddbmQ1YmAzBku_Y9sKYnYx'
headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
# params = {}
fd = Form_Data() # Used to keep track of the form data that is entered by the user

@app.route("/")
def home():
    #general_api()
    return render_template('home.html', error = error)

@app.route("/choose_again")
def choose_again():
    params = dict()
    params['term'] = fd.get_term()
    params['limit'] = 50
    if fd.get_location() != '':
        params['location'] = fd.get_location()
    if fd.get_categories() != '':
        params['categories'] != fd.get_categories()
    if fd.get_radius() != '':
        params['radius'] = int(min(max(float(fd.get_radius()) * 1609.34, 0), 40000))
    if fd.get_price() != '':
        params['price'] = fd.get_price()

    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    data = response.json()

    if data is None or 'total' not in data.keys():
        return render_template('restaurant.html', error = True)
    if data['total'] == 0:
        return render_template('restaurant.html', error = True)
    
    seen = set()
    filtered_restaurants = []
    for restaurant in data['businesses']:
        if restaurant['name'] not in seen:
            seen.add(restaurant['name'])
            filtered_restaurants.append(restaurant)

    rand_restaurant = filtered_restaurants[randint(0, len(filtered_restaurants) - 1)]

    res = fill_restaurant(rand_restaurant)

    return render_template('restaurant.html', restaurant = res)


@app.route('/restaurant', methods =["GET", "POST"])
def get_form():
    # Get input from the form and parse that into a dictionary for the request
    params = get_params(request.form)

    if params == None:
        return render_template('home.html', error = error, errorMsg = 'Error while parsing user input!')
    elif 'location' not in params.keys():
        return render_template('home.html', error = error, errorMsg = 'No Location Provided!')

    # Fill the fd object so that it can be passed in the template
    fill_form_data(params)
    
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    data = response.json()
    if data is None or 'total' not in data.keys():
        return render_template('home.html', error = error, errorMsg = 'Unable to retrieve data from Yelp API!')
    if data['total'] == 0:
        return render_template('home.html', error = error, errorMsg = 'No Restaurants Found!')
    
    seen = set()
    filtered_restaurants = []
    for restaurant in data['businesses']:
        if restaurant['name'] not in seen:
            seen.add(restaurant['name'])
            filtered_restaurants.append(restaurant)

    rand_restaurant = filtered_restaurants[randint(0, len(filtered_restaurants) - 1)]

    res = fill_restaurant(rand_restaurant)
    return render_template('restaurant.html', restaurant = res)

@app.route('/home', methods =["GET", "POST"])
def take_back_to_home():
    return render_template('home.html', fd = fd) 

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
    
    # For these entries if invalid data is encountered, it is just not included in params
    if validate.is_valid_float(radius): # If a radius is provided, try to use it
        params['radius'] = int(min(max(float(radius) * 1609.34, 0), 40000)) 
    if categories != None and categories != '': # If a category is provided, use it
        params['categories'] = categories
    if validate.is_valid_int(price): # If a price range is provided, try to use it
        params['price'] = validate.parse_price(price)
    
    return params

""" 
    Will fill the form data object from what the user entered in the form.
    
    @input: params -> dictionary
    @output: none
"""
def fill_form_data(params):
    if 'term' in params:
        fd.term = params['term']
    else:
        fd.term = ""
    if 'location' in params:
        fd.location = params['location']
    else:
        fd.location = ""
    if 'radius' in params:
        fd.radius = round(params['radius'] / 1609.344)
    else:
        fd.radius = ""
    if 'categories' in params:
        fd.categories = params['categories']
    else:
        fd.categories = ""
    if 'price' in params:
        fd.price = params['price']
    else:
        fd.price = ""

def fill_restaurant(res):
    retRes = Restaurant(name = res['name'], phone = res['phone'], price = res['price'], url = res['url'])
    if res['location']['country'] == 'US':
        location = '{}, {}, {}, {}'.format(res['location']['address1'], res['location']['city'], res['location']['state'], res['location']['zip_code'])
    else:
        location = '{}, {}, {}'.format(res['location']['address1'], res['location']['city'], res['location']['country'])
    retRes.set_location(location)
    return retRes

def general_api():
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    print(response.status_code)
    data = response.json() # It is a dictionary
    print(data.keys()) # Keys are ['businesses', 'total', 'region']
    print(data['businesses'][0])

if __name__ == "__main__":
    app.run()
