"""
This will be used to keep track of certian restruant data to be displayed in Flask. The
Restraunt object will make it much easier to only pass into Flask the information we want 
rather than the entire dictionary which is passed obtained from yelp.

@author: Felix Estrella
"""

class Restaurant(object):
    def __init__(self, name = '', phone = '', price = '', url = '', location = ''):
        self.name = name
        self.phone = phone
        self.price = price
        self.url = url
        self.location = location
    
    def set_name(self, name):
        self.name = name

    def get_name(self, name):
        return self.name

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location