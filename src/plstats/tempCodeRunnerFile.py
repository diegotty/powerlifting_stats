
selecting bar
cv2.namedWindow('select bar !')
cv2.setMouseCallback('select bar !', click_event)
barPos = []
ignore, frame = video.read()
cv2.imshow('select bar !', frame)
while True:
    k = cv2.waitKey(0)
    if k == ord('\r'):
        print("last pos: ",barPos[0]," ",barPos[1])
        break
cv2.destroyWindow('select bar !')