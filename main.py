"""
Main python file for our flask project. This is where all the application
routing happens and where the html files are rendered.

@author: Felix Estrella, Jackson Goth, Shivani Ganesh, and Eric Bal
"""

from distutils.log import error
from random import randint, shuffle
from flask import Flask, render_template, request
import requests, validate
from form_data import Form_Data
from restaurant import Restaurant
from copy import deepcopy

app = Flask(__name__)

# Put in your the api_key here
api_key = 'Iu6RMASUHPZgnXkTKsopdmBGiQK9ht97MCXkyFX_ciEltMPd3YcleBYZHmMcmlrwSmdJqAf_YOv7-CuzP6L64k1Vo64fLATAqoKVYAGwJ3ddbmQ1YmAzBku_Y9sKYnYx'
headers = {'Authorization': 'Bearer {}'.format(api_key)} # Will keep the headers in a dictionary
search_api_url = 'https://api.yelp.com/v3/businesses/search' # The search api url
# params = {}
fd = Form_Data() # Used to keep track of the form data that is entered by the user
saved_restaurants = [] # Keeps track of the saved restaruants
current_restaurant = None # Keeps track of the current restaurant

# Will render the home page for the application
@app.route("/")
def home():
    return render_template('home.html', error = error)

# Code will get executed when the "choose again" button is clicked
# Will grab stored user input and get a new restaurant
@app.route("/choose_again")
def choose_again():
    # Get all the global variables needed
    global current_restaurant, saved_restaurants, api_key, headers, search_api_url, fd

    # Create a dictionary for the params
    params = dict()
    params['term'] = fd.get_term() # Set the term to the stored term in fd
    params['limit'] = 50 # Set limit to 50

    # if the location is not empty, add location to params from fd
    if fd.get_location() != '':
        params['location'] = fd.get_location()
    # if the categories is not empty, add categories to params from fd
    if fd.get_categories() != '':
        params['categories'] = fd.get_categories()
    # if the radius is not empty, add radius to params from fd. Radius need to be converted to meters
    if fd.get_radius() != '':
        params['radius'] = int(min(max(float(fd.get_radius()) * 1609.34, 0), 40000))
    # if the price is not empty, add price to params from fd
    if fd.get_price() != '':
        params['price'] = fd.get_price()

    # Send a get request to the yelp api and store results
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    # Convert response to a json object
    data = response.json()

    # If the response came back empty or is missing the total key alert user
    if data is None or 'total' not in data.keys():
        return render_template('restaurant.html', error = True, saved = saved_restaurants, len = len(saved_restaurants))
    # If a total of zero restauants comes back alert user
    if data['total'] == 0:
        return render_template('restaurant.html', error = True, saved = saved_restaurants, len = len(saved_restaurants))
    
    # Create a set to elimanted duplicate restaurants
    seen = set()
    # Used to store non-duplicated restaurants
    filtered_restaurants = []
    # Add non-duplicate restaurants to the filtered_restaurants list
    for restaurant in data['businesses']:
        if restaurant['name'] not in seen:
            seen.add(restaurant['name'])
            filtered_restaurants.append(restaurant)

    
    cur = 0 # Used to index list
    choose = None # Stores the current restaurant for the loop
    shuffle(filtered_restaurants) # Randomize filtered_restaurants
    # Ensure that the new restaurant choosen will not be the previous one shown
    while choose is not current_restaurant and cur <= len(filtered_restaurants) - 1:
        rand_restaurant = filtered_restaurants[cur]
        choose = fill_restaurant(rand_restaurant)
        cur += 1
    current_restaurant = deepcopy(choose) # Copy the new restaurant

    return render_template('restaurant.html', restaurant = choose, saved = saved_restaurants, len = len(saved_restaurants))

# Used to save the current restaurant shown to the saved_restaurant list
@app.route('/saved')
def save_restaurant():
    # Get global variables needed for method
    global current_restaurant, saved_restaurants

    # Ensure there is a current restaurant to save and it is not in the list already
    if current_restaurant != None and current_restaurant not in saved_restaurants:
        saved_restaurants.append(deepcopy(current_restaurant))

    return render_template('restaurant.html', restaurant = current_restaurant, saved = saved_restaurants, len = len(saved_restaurants))

# Clear all the saved restaurants
# Is executed when the "clear saved" button is executed
@app.route('/clear_all')
def clear_restuarants():
    # Get the gloabl variable of saved_restaurants
    global saved_restaurants
    saved_restaurants = [] # Set list to empty list

    return render_template('restaurant.html', restaurant = current_restaurant, saved = saved_restaurants, len = len(saved_restaurants))

# Will remove a specific restaurant from the saved restaurants list
@app.route('/clear/<string:name>')
def clear_specific_restaurant(name):
    # Get the gloabl variable of saved_restaurants
    global saved_restaurants

    # Check for restaurant in list and when found remove it
    for restaurant in saved_restaurants:
        if restaurant.name == name:
            saved_restaurants.remove(restaurant)
            break

    return render_template('restaurant.html', restaurant = current_restaurant, saved = saved_restaurants, len = len(saved_restaurants))

# Code is called when the form on the home page is submitted
# Will save the form data, make yelp api call, and send user to the restaurant 
@app.route('/restaurant', methods =["GET", "POST"])
def get_form():
    # Get all of the global variables needed
    global current_restaurant, saved_restaurants, api_key, headers, search_api_url, fd
    # Get input from the form and parse that into a dictionary for the request
    params = get_params(request.form)

    # If no params are entered or location not provided alert user
    if params == None:
        return render_template('home.html', error = error, errorMsg = 'Error while parsing user input!')
    elif 'location' not in params.keys():
        return render_template('home.html', error = error, errorMsg = 'No Location Provided!')

    # Fill the fd object so that it can be passed in the template
    fill_form_data(params)
    
    # Send a get request to the yelp api and store results
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
     # Convert response to a json object
    data = response.json()

    # If the response came back empty or is missing the total key alert user
    if data is None or 'total' not in data.keys():
        return render_template('home.html', error = error, errorMsg = 'Unable to retrieve data from Yelp API!')
    # If a total of zero restauants comes back alert user
    if data['total'] == 0:
        return render_template('home.html', error = error, errorMsg = 'No Restaurants Found!')
    
    # Create a set to elimanted duplicate restaurants
    seen = set()
    # Used to store non-duplicated restaurants
    filtered_restaurants = []
    # Add non-duplicate restaurants to the filtered_restaurants list
    for restaurant in data['businesses']:
        if restaurant['name'] not in seen:
            seen.add(restaurant['name'])
            filtered_restaurants.append(restaurant)

    # Get a random restaurant from the filtered list
    rand_restaurant = filtered_restaurants[randint(0, len(filtered_restaurants) - 1)]

    # Get a restaurant object
    res = fill_restaurant(rand_restaurant)
    # Set the restaurant res to the current_restaurant
    current_restaurant = deepcopy(res)

    return render_template('restaurant.html', restaurant = res, saved = saved_restaurants, len = len(saved_restaurants))

# Will take the user back to the home page when the "back" button is pressed
@app.route('/home', methods =["GET", "POST"])
def take_back_to_home():
    global fd
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


# Will fill the form data object from what the user entered in the form.
def fill_form_data(params):
    # Get the global variable of fd which is a Form_Data object
    global fd
    
    # if term exists in params set the Form_Data fd term to it, else the empty string
    if 'term' in params:
        fd.term = params['term']
    else:
        fd.term = ""

    # if location exists in params set the Form_Data fd location to it, else the empty string
    if 'location' in params:
        fd.location = params['location']
    else:
        fd.location = ""

    # if radius exists in params set the Form_Data fd radius to it, else the empty string
    if 'radius' in params:
        fd.radius = round(params['radius'] / 1609.344) # Convert meters to miles
    else:
        fd.radius = ""

     # if categories exists in params set the Form_Data fd categories to it, else the empty string
    if 'categories' in params:
        fd.categories = params['categories']
    else:
        fd.categories = ""

     # if price exists in params set the Form_Data fd price to it, else the empty string
    if 'price' in params:
        fd.price = params['price']
    else:
        fd.price = ""

# Will return a restaurant object given a dictionary with restaurant information
def fill_restaurant(res):
    # Set initial restaurant information
    retRes = Restaurant(name = res['name'], phone = res['phone'], price = res['price'], url = res['url'])

    # If restaurant is in the US set string accordindly and is not then set differently
    if res['location']['country'] == 'US':
        location = '{}, {}, {}, {}'.format(res['location']['address1'], res['location']['city'], res['location']['state'], res['location']['zip_code'])
    else:
        location = '{}, {}, {}'.format(res['location']['address1'], res['location']['city'], res['location']['country'])
    retRes.set_location(location) # Set the location of the retRes

    return retRes

# Used to learn the yelp api
def general_api():
    params = {}
    response = requests.get(search_api_url, headers=headers, params=params, timeout=10)
    print(response.status_code)
    data = response.json() # It is a dictionary
    print(data.keys()) # Keys are ['businesses', 'total', 'region']
    print(data['businesses'][0])

# Will call for the app to run
if __name__ == "__main__":
    app.run()
