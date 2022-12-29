import cv2
from math import sqrt
from rep import Rep



#finding low points and depth point
class Model:
    video = []
    tracker = []
    reps = []
    pxtom = 0
    
    def setupWindow(self, filePath):
        self.video = cv2.VideoCapture('filePath')
        width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT )
        fps = self.video.get(cv2.CAP_PROP_FPS)
        delay = int(1000/fps)
    
    def debugSetupWindow(self):
        self.video = cv2.VideoCapture('C:/Users/diego/Videos/diego/2022/plstats/src/plstats/videos/bench.mp4')
        width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT )
        fps = self.video.get(cv2.CAP_PROP_FPS)
        delay = int(1000/fps)
    
    def createTracker(self, barPoints):
        center, radius = self.findCircle(barPoints)
        self.pxtom = float((radius * 2) / 0.0497)
        ingore, frame = self.video.read()
        self.tracker = cv2.legacy.TrackerMOSSE_create()
        ratio = 30
        roi = [center[0]- ratio, center[1]- ratio, (ratio*2) , (ratio*2)]
        self.tracker.init(frame, roi)
        rep = Rep()
        rep.path.append([center[0],center[1]])  
        self.reps.append(rep)
        return self.reps, center
        
      
    def calcPoints(self):
        self.reps[0].lowPoints, self.reps[0].depthPoint = self.calcLowPoints(self.reps[0])
        self.reps[0].startPoint = self.calcStartPoint(self.reps[0])
        self.reps[0].endPoint = self.calcEndPoint(self.reps[0])
        self.calcSpeed(self.reps[0])
        print('eccentric speed:',self.reps[0].eccentric[2])
        print('concentric speed:', self.reps[0].concentric[2])   
        
    
    def calcLowPoints(self, rep):
        depthPoint = [0,0,0]
        lowPoints = []
        for i in range(1, (len(rep.path)-1)):
            if rep.path[i][1] > rep.path[i+1][1] and rep.path[i-1][1] <= rep.path[i][1]:
                lowPoints.append([rep.path[i][0], rep.path[i][1]])
                if rep.path[i][1] > depthPoint[1]:
                    depthPoint[0] = rep.path[i][0]
                    depthPoint[1] = rep.path[i][1]
                    depthPoint[2] = i
        return lowPoints, depthPoint

    #finding start point
    def calcStartPoint(self, rep):
        startPoint = [0,0,0]
        startPoint[0], startPoint[1] = rep.lowPoints[0][0], rep.lowPoints[0][1]
        for i in range(0, len(rep.lowPoints)):
            if rep.lowPoints[i][1] == rep.depthPoint[1]:
                break
            if rep.lowPoints[i][1] < startPoint[1]:
                startPoint[0], startPoint[1], startPoint[2] = rep.lowPoints[i][0], rep.lowPoints[i][1], i
        return startPoint
                  
    #finding end point  
    def calcEndPoint(self, rep):     
        endPoint = [0,0,0]   
        for i in range(rep.depthPoint[2], len(rep.path)):
            if rep.path[i][1] <= rep.startPoint[1]:
                endPoint[0],endPoint[1], endPoint[2] = rep.path[i][0], rep.path[i][1], i
                break
        return endPoint
    
    def calcSpeed(self, rep):
        rep.eccentric = [0, 0, 0]
        rep.concentric = [0, 0, 0]
        
        rep.eccentric[0] = (rep.depthPoint[2] - rep.startPoint[2]) * 0.033
        rep.concentric[0] = (rep.endPoint[2] - rep.depthPoint[2]) * 0.033
        rep.eccentric[1] = (rep.startPoint[0] - rep.depthPoint[0]) / int(self.pxtom)
        rep.concentric[1] = (rep.endPoint[0] - rep.depthPoint[1]) / int(self.pxtom)
        rep.eccentric[2] = rep.eccentric[1] / rep.eccentric[0]
        rep.concentric[2] = rep.concentric[1] / rep.concentric[0]
    
      
    def findCircle(self, barPoints) :
        x12 = barPoints[0][0] - barPoints[1][0]
        x13 = barPoints[0][0] - barPoints[2][0]
        y12 = barPoints[0][1] - barPoints[1][1]
        y13 = barPoints[0][1] - barPoints[2][1]
        y31 = barPoints[2][1] - barPoints[0][1]
        y21 = barPoints[1][1] - barPoints[0][1]
        x31 = barPoints[2][0] - barPoints[0][0]
        x21 = barPoints[1][0] - barPoints[0][0]
        # x1^2 - x3^2
        sx13 = pow(barPoints[0][0], 2) - pow(barPoints[2][0], 2)
        # y1^2 - y3^2
        sy13 = pow(barPoints[0][1], 2) - pow(barPoints[2][1], 2)
        sx21 = pow(barPoints[1][0], 2) - pow(barPoints[0][0], 2)
        sy21 = pow(barPoints[1][1], 2) - pow(barPoints[0][1], 2)
        f = (((sx13) * (x12) + (sy13) *
            (x12) + (sx21) * (x13) +
            (sy21) * (x13)) // (2 *
            ((y31) * (x12) - (y21) * (x13))))       
        g = (((sx13) * (y12) + (sy13) * (y12) +
            (sx21) * (y13) + (sy21) * (y13)) //
            (2 * ((x31) * (y12) - (x21) * (y13))))
        c = (-pow(barPoints[0][0], 2) - pow(barPoints[0][1], 2) -
            2 * g * barPoints[0][0] - 2 * f * barPoints[0][1])
        h = -g
        k = -f
        sqr_of_r = h * h + k * k - c
        # r is the radius
        r = round(sqrt(sqr_of_r), 5)
        #print("Centre = (", h, ", ", k, ")")
        #print("Radius = ", r)
        center = [h,k]
        radius = r
        return center, radius     