class Sale:
    id = None
    product = None
    quantity = None
    price = None
    currency = None
    date = None
    customer = None
    creator = None
    lastSaleTime = None

    def __init__(self, product=None, quantity=None, price=None, customer=None, currency=None, id=None, date=None, creator=None):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.price = price
        self.currency = currency
        self.date = date
        self.customer = customer
        self.creator = creator
    
    def amount(self):
        if self.quantity != None and self.quantity != None:
            return self.quantity * self.price
        else:
            return None