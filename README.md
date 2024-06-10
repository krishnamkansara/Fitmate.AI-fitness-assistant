Hello Guys, This is my first time experience of coding on " NVIDIA Jetson Nano " and I have created a #--> Face Authenticated Posture Detection Software <--#
here the steps the code follow are

@ Before running the codes install the Libraries/Modules that are given in the \\ Requirements.txt \\ file , Steps are also included in the file@

(1) Start.py - authenticated the face by matching face encodings with Database folders jpg images, if match found oepns Entry.csv and enters name from matched jpg file                 and entry date and time of user and imports Interface.py

(2) Interface.py - Gives choice for exercise and imports codes respectively

(3) exercise.py (can be any according to choice i.e. Curls.py, Deadlifts.py, Squats.py or Pushups.py) - checks posture of user using mediapipe and counts number of                     reps and state of user, once exercise done on pressing x code is closed and Leave.py is imported

(4) Leave.py - authenticates face for the final time and enter leaving time in the Entry.csv file

 ---------------------------
| ## Face Authentication ## |
 ---------------------------
Gives a Personalized experiance and is used to Get the Entry Date and Time of a User and also the Exit time after completing an exercise by entering the name and date time values in the excel sheet.

Start and Leave.py files that are executed in the beginning and end of the proceess.

So, in these program files I have used face_recognistion, opencv, Numpyd, datetime, os libraries -

here face recognition is imported to perform various operations such as -->
- face_encodings, 
- compare_faces,
- face_distance, and
- face_locations

Opencv is used to perform functions that include taking video feed from the device, loading images  and processing those images
from open cv we have used -->
- rectangle,
- VideoCapture,
- destroyallwindows,
- cvtcolor, and	
- imshow

and numpy as we all know is a basic level external library in Python used for complex mathematical operations

-this library Returns the indices of the minimum values along an axis. ... If this is set to True, the axes which are reduced are left in the result as dimensions with size one .

 -------------------------
| ## Posture Detection ## | refer to the \\ Landmarks.png \\ file for more clearance of the codes
 -------------------------
for the prototype functioning I have added .py codes for various exercises such as Curls, Deadlifts, Pushup and Squats

for these files I have used Mediapipe, Opencv and numpy

from numpy I have used functions to calculate angles and convert them to radians using 
absolute, 
arctan, and 
pi functions

Next I have used Mediapipe Pose which is a ML solution for high-fidelity body pose tracking, inferring 3D landmarks and background segmentation mask on the whole body from RGB video frames utilizing our BlazePose research that also powers the ML Kit Pose Detection API.

I have used multiple mediapipe pose functions such as

- mp_drawing = mp.solutions.drawing_utils

- mp_pose = mp.solutions.pose

- I have qalso used landmarks function that is used to extract speparate landmark points as shown in the readme.md files landmarks image

- mp_drawing.draw_landmarks to draw landmarks of the whole body and display them on the display

now, for the video feed and sunctions I have used Opencv and its multiple functions like

- cv2.rectangle(image, (0,0), (200,70), (0,0,0), -1)

- cv2.putText(image, str(counter), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

to give a display of number of reps and the state on the display screen

I am also going to add an option of posture analysis in order to check the posture of the user while performing particular exercises so as to prevent unwanted injuries and created this prototype into a full fledge software that can work like a personalized trainer and give users a better experience

For More Information Checkout my video  -- https://www.youtube.com/watch?v=JnI7tQAJJA0

                                       ------------------------------------ Thank You -----------------------------------------
