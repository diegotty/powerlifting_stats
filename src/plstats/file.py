import cv2
import numpy as np
import time
import mediapipe as mp
from math import sqrt


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#body recognition
def mpStream():
    ignore, frame = video.read()
    # frame = cv2.flip(frame, 1)
        
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
        
    results = pose.process(image)
        
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                mp_drawing.DrawingSpec(color=(0, 0, 0), thickness = 2, circle_radius = 2), 
                                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness = 2, circle_radius = 2)) 
    return image

#box drawing
def drawBox(frame, bbox):
    x, y, w, h, = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(frame, (x,y), ((x+w), (y+h)), (0,0,0), 3, 1)    

#mouse double click
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        barPos.append([x,y])
        print(x, " ",y)
        print('number of points selected: ', len(barPos))
        
        
def findCircle(x1, y1, x2, y2, x3, y3) :
    x12 = x1 - x2
    x13 = x1 - x3
 
    y12 = y1 - y2
    y13 = y1 - y3
 
    y31 = y3 - y1
    y21 = y2 - y1
 
    x31 = x3 - x1
    x21 = x2 - x1
 
    # x1^2 - x3^2
    sx13 = pow(x1, 2) - pow(x3, 2)
 
    # y1^2 - y3^2
    sy13 = pow(y1, 2) - pow(y3, 2)
    sx21 = pow(x2, 2) - pow(x1, 2)
    sy21 = pow(y2, 2) - pow(y1, 2)
 
    f = (((sx13) * (x12) + (sy13) *
          (x12) + (sx21) * (x13) +
          (sy21) * (x13)) // (2 *
          ((y31) * (x12) - (y21) * (x13))))
             
    g = (((sx13) * (y12) + (sy13) * (y12) +
          (sx21) * (y13) + (sy21) * (y13)) //
          (2 * ((x31) * (y12) - (x21) * (y13))))
 
    c = (-pow(x1, 2) - pow(y1, 2) -
         2 * g * x1 - 2 * f * y1)
 
    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
    # where centre is (h = -g, k = -f) and
    # radius r as r^2 = h^2 + k^2 - c
    h = -g
    k = -f
    sqr_of_r = h * h + k * k - c
 
    # r is the radius
    r = round(sqrt(sqr_of_r), 5)
 
    print("Centre = (", h, ", ", k, ")")
    print("Radius = ", r);
    center = [h,k]
    radius = r
    return center, radius     
        
        

# video input
video = cv2.VideoCapture('powerlifting\\squat.mp4')
width = video.get(cv2.CAP_PROP_FRAME_WIDTH )
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT )
print(height)
print(width)
fps = video.get(cv2.CAP_PROP_FPS)
print(fps)
delay = int(1000/fps)


#selecting bar
# cv2.namedWindow('select bar !')
# cv2.setMouseCallback('select bar !', click_event)
# barPos = []
# ignore, frame = video.read()
# cv2.imshow('select bar !', frame)
# while True:
#     k = cv2.waitKey(0)
#     if k == ord('\r'):
#         print("last pos: ",barPos[0]," ",barPos[1])
#         break
# cv2.destroyWindow('select bar !')


# selecting 2 points from the bar
cv2.namedWindow('select 3 points on the bar !')
cv2.setMouseCallback('select 3 points on the bar !', click_event)
barPos = []
ignore, frame = video.read()
cv2.imshow('select 3 points on the bar !', frame)
while True:
    k = cv2.waitKey(0)
    if k == ord('\r') and len(barPos) == 3:
        break
    if k == ord('\b'):
        barPos.pop()
        print('number of points selected: ', len(barPos))
    
cv2.destroyWindow('select 3 points on the bar !')
center, radius = findCircle(barPos[0][0], barPos[0][1], barPos[1][0], barPos[1][1], barPos[2][0], barPos[2][1])

#creating tracker
tracker = cv2.legacy.TrackerMOSSE_create()
ratio = 30
roi = [center[0]- ratio, center[1]- ratio, (ratio*2) , (ratio*2)]
tracker.init(frame, roi)
path = []
path.append([barPos[0],barPos[1]])

#showing video
objDetector = cv2.createBackgroundSubtractorMOG2()
with mp_pose.Pose(min_detection_confidence = 0.95, min_tracking_confidence = 0.95) as pose:
    while True:
        ignore, frame = video.read()
        # cv2.imshow('sbd', mpStream())
        if not ignore:
            break
        #printing path
        success, bbox = tracker.update(frame)
        cv2.circle(frame, (barPos[0], barPos[1]), radius=0, color=(0, 0, 255), thickness=10)
        for point in range(len(path)):
            cv2.circle(frame, (int(path[point][0]), int(path[point][1])), radius = 1, color=(0,0,0), thickness = 3)
        
        #verifying tracking    
        if success:
            drawBox(frame, bbox)
            #print(bbox[0]+ratio, bbox[1]+ratio)
            path.append([int(bbox[0]+ratio), int(bbox[1]+ratio)])      
        else:
            print("lost")  
              
        cv2.imshow('sbd', frame)
        
        k = cv2.waitKey(delay)
        
        if k == ord('q'):
            break
        elif k == ord('p'):
            cv2.waitKey(0)
            if k == ord('p'):
                cv2.waitKey(1)
        
        
video.release()  
cv2.destroyAllWindows()    

isLiftValild = True
lowPoints = []
depthPoint = [0,0,0]

#finding low points and depth point
for i in range(1, (len(path)-1)):
    if path[i][1] > path[i+1][1] and path[i-1][1] <= path[i][1]:
        lowPoints.append([path[i][0], path[i][1]])
        if path[i][1] > depthPoint[1]:
            depthPoint[0] = path[i][0]
            depthPoint[1] = path[i][1]
            depthPoint[2] = i

#finding start point
startPoint = [0,0,0]
startPoint[0], startPoint[1] = lowPoints[0][0], lowPoints[0][1]
for i in range(0, len(lowPoints)):
    if lowPoints[i][1] == depthPoint[1]:
        break
    if lowPoints[i][1] < startPoint[1]:
        startPoint[0], startPoint[1], startPoint[2] = lowPoints[i][0], lowPoints[i][1], i
        
#finding end point       
endPoint = [0,0,0]   
for i in range(depthPoint[2], len(path)):
    if path[i][1] <= startPoint[1]:
        endPoint[0],endPoint[1], endPoint[2] = path[i][0], path[i][1], i
        break
    
#finding rep time
eccentricTime = (depthPoint[2] - startPoint[2]) * 0.033
concentricTime = (endPoint[2] - depthPoint[2]) * 0.033

print('eccentric: ', eccentricTime)
print('concentric: ', concentricTime)


print("points:", len(path))
print("start point: ", startPoint)
print('depth point: ', depthPoint)
print('end point:', endPoint)           
 
#making black image    
blackImg = np.zeros(shape=[int(height), int(width), 3])
#drawing paths/points
for point in range(len(path)):
    cv2.circle(blackImg, (int(path[point][0]), int(path[point][1])), radius = 1, color=(255,255,255), thickness = 1) 
for point in range(len(lowPoints)):
    cv2.circle(blackImg, (int(lowPoints[point][0]), int(lowPoints[point][1])), radius = 1, color=(255,0,0), thickness = 10)
cv2.circle(blackImg, (endPoint[0], endPoint[1]), radius = 1, color=(0,255,0), thickness = 5)
cv2.circle(blackImg, (depthPoint[0], depthPoint[1]), radius = 1, color=(0,255,0), thickness = 5)
cv2.circle(blackImg, (startPoint[0], startPoint[1]), radius = 1, color=(0,255,0), thickness = 5)

#showing image    
cv2.imshow('path !', blackImg)
k = cv2.waitKey(0)
if k == ord('q'):
    cv2.destroyWindow('path !')
    
print("first")    
    
