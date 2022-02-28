
class Form_Data:
    def __init__(self):
        self.term = None
        self.location = None
        self.latitude = None
        self.longitude = None
        self.radius = None
        self.categories = None
        self.price = None

    def set_term(self, term):
        self.term = term
    
    def get_term(self):
        return self.term

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_latitude(self):
        return self.latitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def get_longitude(self):
        return self.longitude

    def set_radius(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius

    def set_categories(self, categories):
        self.categories = categories

    def get_categories(self):
        return self.categories

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price