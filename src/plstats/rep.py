class Rep:
    lowPoints = []
    depth = []

    def __init__(self, path = None, lowPoints = None, startPoint = None, depthPoint = None, endPoint = None):
        self.path = []
        self.lowPoints = []
        self.startPoint = []
        self.depthPoint = []
        self.endPoint = []
        #[0] = time, [1] = distance, [2] = speed
        self.eccentric=[]
        self.concentric=[]
        
    def isValid(self):
        pass