import cv2
import mediapipe as mp
import numpy as np
import datetime
import threading
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
Feed = cv2.VideoCapture(0)

# Variables for count and state
counter = 0 
state = None
last_rep_time = datetime.datetime.now()

# Track start time
start_time = datetime.datetime.now()

# Alert message variables
alert_message = ""
show_alert = False

def reset_alert():
    global show_alert
    show_alert = False

def markRepetitions(exercise, repetitions):
    with open('Face Authenticated Posture Detection\Entry.csv', 'a') as f:
        f.write(f',{repetitions}')

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while Feed.isOpened():
        ret, frame = Feed.read()
        if not ret:
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Function to calculate angle
        def calculate_angle(a, b, c):
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)

            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)

            if angle > 180.0:
                angle = 360 - angle

            return angle

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)

            # Curl counter logic
            if angle > 160:
                state = "Down"
            if angle < 30 and state == 'Down':
                state = "Up"
                current_time = datetime.datetime.now()
                time_diff = current_time - last_rep_time
                if time_diff.total_seconds() < 3:
                    alert_message = "Adopt a slower pace to reduce the risk of injury."
                    show_alert = True
                    threading.Timer(5, reset_alert).start()
                counter += 1
                last_rep_time = current_time
                print(counter)
            exercise = "Curls"
        except:
            pass

        # Render elements
        cv2.rectangle(image, (0, 0), (200, 70), (0, 0, 0), -1)
        cv2.rectangle(image, (int(image.shape[1] * 0.85), 0), (int(image.shape[1]), int(image.shape[0] * 0.05)), (0, 0, 0), -1)
        cv2.rectangle(image, (0, int(image.shape[0] - 0.05 * image.shape[0])), (200, image.shape[0]), (0, 0, 0), -1)

        # Rep data
        cv2.putText(image, 'REPS', (10, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(image, 'STATE', (int(image.shape[1] * 0.1) + 20, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, state, (int(image.shape[1] * 0.1) + 20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Exercise Name
        cv2.putText(image, exercise, (int(image.shape[1] * 0.86), 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Date Time
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(image, date_time, (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 0, 250), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(250, 250, 250), thickness=2, circle_radius=2))

        # Display alert message if required
        if show_alert:
            alert_text_size = cv2.getTextSize(alert_message, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            alert_x = image.shape[1] - alert_text_size[0] - 20
            alert_y = image.shape[0] - alert_text_size[1] - 20
            cv2.rectangle(image, (alert_x - 5, alert_y - 5), (alert_x + alert_text_size[0] + 5, alert_y + alert_text_size[1] + 5), (255, 255, 255), -1)
            cv2.putText(image, alert_message, (alert_x, alert_y + alert_text_size[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow('Feed', image)

        # Check if 30 minutes have passed
        elapsed_time = datetime.datetime.now() - start_time
        if elapsed_time.total_seconds() >= 1800:  # 30 minutes = 1800 seconds
            break

        if cv2.waitKey(1) & 0xFF == ord('x'):
            markRepetitions(exercise, counter)
            # markRepetitions(exercise, counter)
            Feed.release()
            cv2.destroyAllWindows()
            os._exit(0)  # Kill the terminal

            import Leave
            break

    
