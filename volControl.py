import cv2
import time
import numpy as np
import HandTrackModule as htm
import math
import osascript

#######################
wcam,hcam=640,480
######################
cp=cv2.VideoCapture(0)
cp.set(3,wcam)
cp.set(4,hcam)

detector=htm.handDetector(detectionCon = 0.7)

#for mac osascript is used to control the volume
#for windows the pycaw is used






ptime=0

while(True):
    suceess,img= cp.read()

    img= detector.findHands(img)
    lmList=detector.findPosition(img,0)

    # we want the two indexes i.e top of foreFinger and thumb
    #fore finger point is 4 and thum is 8
    if len(lmList)!=0:

        x1, y1 = lmList[4][1], lmList[4][2] #coordinate points of 4
        x2, y2 = lmList[8][1], lmList[8][2] #coordinate points of 8
        cx,cy= (x1+x2)//2 , (y1+y2)//2

        #drawing circle at two indexes i.e 4 and 8
        cv2.circle(img, (x1,y1), 10, (255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        #we are taking length between two points of point no.4 and 8
        #This length is used for varying the volume in future

        length= math.hypot((x2-x1),(y2-y1))
        print(length)
        #hand range= 50-300
        #vol range= 0-100

        vol=np.interp(length,[50,300],[0,100])

        osascript.osascript(f"set volume output volume {vol}")

        newRange=np.interp(length,[50,300],[400,150])

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 255),3)
        cv2.rectangle(img,(50,int(newRange)),(85,400),(255,0,255),cv2.FILLED)
        cv2.putText(img,f'{int(vol)}', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)












    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,F'FPS:{int(fps)}',(40, 50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)