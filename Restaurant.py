"""
This will be used to keep track of certian restruant data to be displayed in Flask. The
Restraunt object will make it much easier to only pass into Flask the information we want 
rather than the entire dictionary which is passed obtained from yelp.

@author: Felix Estrella
"""

class Restaurant(object):
    # Constructor to the Restaurant which will set everything to the empty string.
    # Parameters can be assigned as well
    def __init__(self, name = '', phone = '', price = '', url = '', location = ''):
        self.name = name
        self.phone = phone
        self.price = price
        self.url = url
        self.location = location
    
    # Will check for equality by name and location
    def __eq__(self, other):
        return other != None and self.name == other.name and self.location == other.location
    
    # Will return a string of name and phone
    def __str__(self):
        return self.name + ": " + self.phone
    
    # Will set the name, given the name parameter
    def set_name(self, name):
        self.name = name

    # Returns the name
    def get_name(self):
        return self.name

    # Will set the phone, given the phone parameter
    def set_phone(self, phone):
        self.phone = phone

    # Returns the phone numbers
    def get_phone(self):
        return self.phone

    # Will set the price, given the price parameter
    def set_price(self, price):
        self.price = price

    # Returns the price
    def get_price(self):
        return self.price

    # Will set the url, given the url parameter
    def set_url(self, url):
        self.url = url

    # Returns the url
    def get_url(self):
        return self.url

    # Will set the location, given the location parameter
    def set_location(self, location):
        self.location = location

    # Returns the location
    def get_location(self):
        return self.location