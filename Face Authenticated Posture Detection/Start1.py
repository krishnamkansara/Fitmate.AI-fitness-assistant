import sys
import os
import cv2
import numpy as np
import face_recognition
from datetime import datetime
import pandas as pd  # Import pandas for data handling
import Curls, Pushups, Deadlifts, Squats  # Import modules for exercises

sys.dont_write_bytecode = True

# Path to the face database
path = 'Face Authenticated Posture Detection\Database'

# Load known faces
def load_known_faces():
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    encodeList = findEncodings(images)
    return encodeList, classNames

# Find encodings for known faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeList.append(face_recognition.face_encodings(img)[0])
    return encodeList

# Mark attendance and add the new entry at the end of the file
def markAttendance(name, exercise_type):
    path = 'Face Authenticated Posture Detection\Entry.csv'
    with open(path, 'r+') as f:
        lines = f.readlines()
        lines.reverse()
        nameList = [line.strip().split(',')[0] for line in lines if line.strip()]
        now = datetime.now()
        dtString = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{name},{exercise_type},{dtString}\n')

    # Calculate total time spent from the CSV
    df = pd.read_csv(path)

    # Store original formats of 'Entry Time' and 'Exit Time'
    original_entry_time = df['Entry Time'].copy()
    original_exit_time = df['Exit Time'].copy()

    # Temporarily convert 'Entry Time' and 'Exit Time' to datetime format
    df['Entry Time'] = pd.to_datetime(df['Entry Time'])
    df['Exit Time'] = pd.to_datetime(df['Exit Time'])

    # Calculate the total time
    df['Total Time'] = df['Exit Time'] - df['Entry Time']

    # Format 'Total Time' to show only hours, minutes, and seconds
    df['Total Time'] = df['Total Time'].dt.components.apply(
        lambda x: f"{int(x['hours']):02}:{int(x['minutes']):02}:{int(x['seconds']):02}", axis=1)

    # Restore the original formats of 'Entry Time' and 'Exit Time'
    df['Entry Time'] = original_entry_time
    df['Exit Time'] = original_exit_time

    # Save the DataFrame with the new 'Total Time' column back to the same CSV file
    df.to_csv(path, index=False)

# Generate frames for the video feed and handle attendance and exercise tracking
def generate_frames(exercise_type):
    encodeListKnown, classNames = load_known_faces()
    camera = cv2.VideoCapture(0)
    attendance_marked = False
    exercise_started = False

    while True:
        success, img = camera.read()
        if not success:
            break

        img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = classNames[first_match_index]
                markAttendance(name, exercise_type)
                attendance_marked = True
                break

        if attendance_marked:
            if exercise_type == "Curls":
                Curls.track_curls(img)
            elif exercise_type == "Pushups":
                Pushups.track_pushups(img)
            elif exercise_type == "Deadlifts":
                Deadlifts.track_deadlifts(img)
            elif exercise_type == "Squats":
                Squats.track_squats(img)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

if __name__ == "__main__":
    exercise_type = "Curls"  # Example to start with Curls, replace it with the actual method to get exercise type
    for frame in generate_frames(exercise_type):
        # Example to display frame using OpenCV, adjust according to your needs
        img = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)
        cv2.imshow('Feed', img)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break

    cv2.destroyAllWindows()
