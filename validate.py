
# Return True if float is actually a float, False otherwise
def is_valid_float(i):
    if i == None or i == '':
        return False
    try:
        j = float(i)
    except ValueError:
        return False
    return True

# Return True if int is actually an int, False otherwise
def is_valid_int(i):
    if i == None or i == '':
        return False
    try:
        j = int(i)
    except ValueError:
        return False
    return True

# Return a string containing which prices we want to include (formatted to specification of Fusion API)
def parse_price(price):
    price_setting = ''
    for i in range(int(price) - 1):
        price_setting += str(i + 1) + ','
    price_setting += price
    return price_setting