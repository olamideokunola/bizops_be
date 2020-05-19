class Product:
    id = None
    name = None
    group = None
    title = None
    price = None
    prices = []
    date = None
    units = []

    def __init__(self, id=None, name=None, price=None, prices=[], date=None):
        self.id = id
        self.name = name
        self.title = name
        self.date = date
        self.price = price
        self.prices = prices

    def set_current_price(self, amount=None):
        self.price = amount

    def add_price(self, amount=None, fromDate = None, toDate=None, currency=None, active=None):
        if amount != None:
            price = Price(amount=amount, fromDate=fromDate, toDate=toDate, currency=currency, active=active)
            if self.prices == None:
                self.prices = []
            # add the new price only it was not existing
            if len([price for price in self.prices if price.amount == amount]) == 0:
                self.prices.append(price)
                return "Price already exists!"
            else:
                # if price exist change the active status
                for price in self.prices:
                    if price.amount == amount:
                        price.active = active

    def set_default_price(self, amount=None, fromDate = None, toDate=None, currency=None, active=None):
        self.price = Price(amount=amount, fromDate=fromDate, toDate=toDate, currency=currency, active=active)

class Price:
    id = None
    fromDate = None
    toDate = None
    amount = None
    currency = None
    active = None
    def __init__(self, id=None, fromDate=None, toDate=None, amount=None, currency = None, active=None):
        self.id = id
        self.fromDate = fromDate
        self.toDate = toDate
        self.amount = amount
        self.currency = currency
        self.active = active

class Unit:
    id=None
    shortDesc=None
    longDesc=None
    active=None

    def __init__(self, shortDesc=None, longDesc=None, id=None, active=False):
        self.id = id
        self.shortDesc = shortDesc
        self.longDesc = longDesc
        self.active = active