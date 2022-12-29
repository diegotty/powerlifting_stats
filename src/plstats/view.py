import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from rep import Rep


ratio = 25
class View:
    video = []
    videoHeight = 0
    videoWidth = 0
    videoPath = ''
    def __init__(self):
        pass   
    
    def selectFile(self):
        root = tk.Tk()
        root.withdraw()
        filePath = filedialog.askopenfilename()
        return filePath
    
    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            param.append([x,y])
            print(x,",",y)
            print('number of points selected:', len(param))
    
    def selectPoints(self, video):
        barPoints = []
        self.video = video
        self.videoWidth = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.videoHeight = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        cv2.namedWindow('select 3 points on the bar !')
        cv2.setMouseCallback('select 3 points on the bar !', self.click_event, barPoints)
        ignore, frame = self.video.read()
        cv2.imshow('select 3 points on the bar !', frame)
        while True:
            k = cv2.waitKey(0)
            if k == ord('\r') and len(barPoints) == 3:
                break
            if k == ord('\b'):
                barPoints.pop()
                print('number of points selected:', len(barPoints))
        
        cv2.destroyWindow('select 3 points on the bar !')
        barPoints = [[581, 90],[602,70],[560,71]]
        return barPoints

    def debugSelectPoints(self, video):
        barPoints = []
        self.video = video
        self.videoWidth = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.videoHeight = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        barPoints = [[581, 90],[602,70],[560,71]]
        return barPoints
        
    
    def showClip(self, tracker, center, reps):
        while True:
            ignore, frame = self.video.read()
            if not ignore:
                break
            # printing path
            success, bbox = tracker.update(frame)
            cv2.circle(frame, (center[0], center[1]), radius=0, color=(0, 0, 255), thickness=10)
            for point in range(len(reps[0].path)):
                cv2.circle(frame, (int(reps[0].path[point][0]), int(reps[0].path[point][1])), radius = 1, color=(0,0,0), thickness = 3)           
            # verifying tracking    
            if success:
                self.drawBox(frame, bbox)
                reps[0].path.append([int(bbox[0]+ratio), int(bbox[1]+ratio)])      
            else:
                pass
                #print("lost")  
                
            cv2.imshow('sbd', frame)        
            k = cv2.waitKey(int(1000/self.video.get(cv2.CAP_PROP_FPS)))        
            if k == ord('q'):
                break
            elif k == ord('p'):
                cv2.waitKey(0)
                if k == ord('p'):
                    cv2.waitKey(1)        
        self.video.release()  
        cv2.destroyAllWindows()   
    
    def drawBox(self, frame, bbox):
        x, y, w, h, = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x,y), ((x+w), (y+h)), (0,0,0), 3, 1)  


    def showPath(self, rep):    
        blackImg = np.zeros([self.videoHeight, self.videoWidth])
        #drawing paths/points
        for point in range(len(rep.path)):
            cv2.circle(blackImg, (int(rep.path[point][0]), int(rep.path[point][1])), radius = 1, color=(255,255,255), thickness = 1) 
        for point in range(len(rep.lowPoints)):
            cv2.circle(blackImg, (int(rep.lowPoints[point][0]), int(rep.lowPoints[point][1])), radius = 1, color=(255,0,0), thickness = 10)
        cv2.circle(blackImg, (rep.endPoint[0], rep.endPoint[1]), radius = 1, color=(0,255,0), thickness = 5)
        cv2.circle(blackImg, (rep.depthPoint[0], rep.depthPoint[1]), radius = 1, color=(0,255,0), thickness = 5)
        cv2.circle(blackImg, (rep.startPoint[0], rep.startPoint[1]), radius = 1, color=(0,255,0), thickness = 5) 
        cv2.imshow('path !', blackImg)
        k = cv2.waitKey(0)
        if k == ord('q'):
            cv2.destroyWindow('path !')