from handDetector import HandDetector
import cv2
import math
import numpy as np
import time
import firebase_admin
from firebase_admin import credentials,db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{"databaseURL":""})

ref = db.reference("/")
# users_ref = ref.child('instruction')
# ref = db.reference("/")
# print(ref.get())


handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)
Takeoff = False
pause_recognition = False
pause_start_time = 0

while True:
   status, image = webcamFeed.read()
   handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
   instruction = ""
   state = False
   

   if len(handLandmarks) != 0:
      if handLandmarks[4][1] > handLandmarks[3][1] and handLandmarks[8][2] < handLandmarks[6][2] and handLandmarks[20][2] < handLandmarks[18][2] and handLandmarks[12][2] < handLandmarks[10][2] and handLandmarks[16][2] < handLandmarks[14][2] and state == False:
         instruction = "Landing"
         print("landing")
         state = True
      if handLandmarks[4][1] > handLandmarks[3][1] and handLandmarks[8][2] < handLandmarks[6][2] and handLandmarks[20][2] < handLandmarks[18][2] and state == False: 
         instruction = "Take Off"
         print("take off")
         state = True
         Takeoff = True

      if handLandmarks[8][2] < handLandmarks[6][2] and handLandmarks[12][2] < handLandmarks[10][2] and handLandmarks[16][2] > handLandmarks[14][2] and state == False:
         instruction = "Backward"
         print("Backward")
         state = True
      if handLandmarks[8][2] < handLandmarks[6][2] and handLandmarks[12][2] < handLandmarks[10][2] and handLandmarks[16][2] < handLandmarks[14][2] and state == False:
         instruction = "Stop"
         print("Stop")
         state = True
      if handLandmarks[8][2] < handLandmarks[6][2] and handLandmarks[20][2] < handLandmarks[18][2] and state == False:   
         instruction = "Left"
         print("left")    
         state = True

      if handLandmarks[4][1] > handLandmarks[3][1] and handLandmarks[8][2] < handLandmarks[6][2] and state == False:     
         instruction = "Right"
         print("right")
         state = True

      if handLandmarks[8][2] < handLandmarks[6][2] and state == False:
         instruction = "Forward"
         print("Forward")
         state = True
      if Takeoff == True and state == False:
         instruction = "Hover"
         print("Hover")
         state = True
      if instruction != "":
         ref.push({
            "instruction": instruction
         })

      
   

   cv2.putText(image, instruction, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
   cv2.imshow("Volume", image)
   cv2.waitKey(1)

