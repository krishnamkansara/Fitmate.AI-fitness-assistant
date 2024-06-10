import sys
sys.dont_write_bytecode = True

from base64 import encode
import os
from matplotlib.pyplot import close 
import numpy as np
import face_recognition
import cv2
from datetime import datetime



path = 'Face Authenticated Posture Detection\Database' #folder name
images = []     
classNames = []
myList = os.listdir(path) #list all the name inside of dir
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


#face encoding
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(img)[0]
        encodeList.append(face_encoding)
    return encodeList

def markAttendance(name):
    with open('Face Authenticated Posture Detection\Entry.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f',{dtString}')
            f.close()
            Feed.release()
            cv2.destroyAllWindows()  
            exit()
            
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Video Feed
# For CSI Camera 
# Use Opencv version (4.1.1) for proper Functioning
'''
def gstreamer_pipeline(
	capture_width=1280,
	capture_height=720,
	display_width=1280,
	display_height=720,
	framerate=30,
	flip_method=0,
):
	return (
		"nvarguscamerasrc ! "
		"video/x-raw(memory:NVMM), "
		"width=(int)%d, height=(int)%d, "
		"format=(string)NV12, framerate=(fraction)%d/1 ! "
		"nvvidconv flip-method=%d ! "
		"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
		"videoconvert ! "
		"video/x-raw, format=(string)BGR ! appsink"
	      % (
			capture_width,
			capture_height,
			framerate,
			flip_method,
			display_width,
			display_height,
	  	)
  )


key=cv2.waitKey(1)
#for jetson camera
Feed=cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER) 
'''
# For Laptop
# Feed= cv2.VideoCapture(0) 
# For Phone
Feed =cv2.VideoCapture(0)

while True:
    success, img = Feed.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    #both should be for same person face
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
            # Feed.release()
            # cv2.destroyAllWindows()     
            
 

    # cv2.imshow("Feed",img)
    # if cv2.waitKey(10) & 0xFF == ord('x'):
    #     break
