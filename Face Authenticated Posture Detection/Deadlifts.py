import cv2
import mediapipe as mp
import numpy as np
from Curls import Feed
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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
Feed= cv2.VideoCapture(0) 
# For Phone
#Feed =cv2.VideoCapture('http://172.168.8.64:8080/video')

# Curl counter variables
counter = 0 
stage = None

#Function
def calculate_angle(a,b,c):
            a = np.array(a) # First
            b = np.array(b) # Mid
            c = np.array(c) # End
                    
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
                    
            if angle >180.0:
                angle = 360-angle
                        
            return angle
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while Feed.isOpened():
        ret, frame = Feed.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            
            # Calculate angle
            angle_knee = calculate_angle(hip, knee, ankle) #Knee joint angle
            angle_hip = calculate_angle(shoulder, hip, knee)
            hip_angle = 180-angle_hip
            knee_angle = 180-angle_knee
            
            # Visualize angle
            # cv2.putText(image, str(angle_knee), 
            #                tuple(np.multiply(knee, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (79, 121, 66), 2, cv2.LINE_AA
            #                     )
            
            # cv2.putText(image, str(angle_hip), 
            #                tuple(np.multiply(hip, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )
            
            # Curl counter logic
            if angle_knee > 170:
                state = "Up"
            if angle_knee <= 90 and stage =='UP':
                state="Down"
                counter +=1
                print(counter)
            exercise= "Deadlifts"
        except:
            pass
                
        cv2.rectangle(image, (0,0), (200,70), (0,0,0), -1)
        cv2.rectangle(image, (540,0), (620,20), (0,0,0), -1)
                
        # Rep data
        cv2.putText(image, 'REPS', (10,17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                
        # Stage data
        cv2.putText(image, 'STATE', (90,17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        cv2.putText(image, state, (90,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Exercise Name
        cv2.putText(image, exercise, (550,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        
        
        # Render detections
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #                           mp_drawing.DrawingSpec(color=(0,0,250), thickness=2, circle_radius=2), 
        #                           mp_drawing.DrawingSpec(color=(250,250,250), thickness=2, circle_radius=2) 
        #                         )                
        
        cv2.imshow('Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('x'):
            import Leave
            break

    Feed.release()
    #out.release()
    cv2.destroyAllWindows()
