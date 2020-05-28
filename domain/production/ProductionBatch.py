class ProductionBatch:
    id=None
    productType=None
    flourQuantity=None
    date=None
    startTime=None
    endTime=None
    products=[]
    baker=None
    supervisor=None
    assistants=[]
    problems=[]

    def __init__(self, productType=None, flourQuantity=None, date=None, startTime=None, baker=None):
        self.productType = productType
        self.flourQuantity = flourQuantity
        self.date = date
        self.startTime = startTime
        self.baker = baker