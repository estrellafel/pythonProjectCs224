"""
This is a Form_Data object which will mainly be used for keeping the data that the user
has entered in the form. This will help allow for fields to be set in the form if the
user has already entered the data.

@author: Felix Estrella
"""
class Form_Data(object):
    # constructor to set everything to none to start, insert data as form data is grabbed
    def __init__(self, term = '', location = '', radius = '', categories = '', price = ''):
        self.term = term
        self.location = location
        self.radius = radius
        self.categories = categories
        self.price = price

    # Will set the term, given the term paramter
    def set_term(self, term):
        self.term = term
    
    # Will return the term
    def get_term(self):
        return self.term

    # Will set the location, given the location paramter
    def set_location(self, location):
        self.location = location

    # Will return the location
    def get_location(self):
        return self.location

    # Will set the radius, given the radius paramter
    def set_radius(self, radius):
        self.radius = radius

    # Will return the radius
    def get_radius(self):
        return self.radius

    # Will set the categories, given the categories paramter
    def set_categories(self, categories):
        self.categories = categories

    # Will return the categories
    def get_categories(self):
        return self.categories

    # Will set the price, given the price paramter
    def set_price(self, price):
        self.price = price

    # Will return the price
    def get_price(self):
        return self.price