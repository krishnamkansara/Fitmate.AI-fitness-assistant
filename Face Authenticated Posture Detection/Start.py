import cv2
import numpy as np
import face_recognition
from datetime import datetime
import os

def load_known_faces():
    path = 'Face Authenticated Posture Detection\Database'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    encodeList = findEncodings(images)
    return encodeList, classNames

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeList.append(face_recognition.face_encodings(img)[0])
    return encodeList

def markAttendance(name, exercise_type):
    path = 'Face Authenticated Posture Detection\Entry.csv'
    with open(path, 'a') as f:  # Open the file in append mode
        now = datetime.now()
        dtString = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{name},{exercise_type},{dtString}\n')


def generate_frames(exercise_type):
    encodeListKnown, classNames = load_known_faces()
    camera = cv2.VideoCapture(0)
    attendance_marked = False
    exercise_started = False

    while True:
        success, img = camera.read()
        if not success:
            break
        else:
            img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small)
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            if not attendance_marked:
                for face_encoding, face_location in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                    name = "Unknown"
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = classNames[first_match_index]
                        markAttendance(name, exercise_type)
                        attendance_marked = True  # Mark attendance and start exercise
                        exercise_started = True
                        break  # Stop processing once attendance is marked

            if attendance_marked and exercise_started:
                # Depending on the exercise type, call the respective module's function
                if exercise_type == "Curls":
                    import Curls
                    Curls.track_curls(img)  # Assuming track_curls is a function to track curls exercise
                elif exercise_type == "Pushups":
                    import Pushups
                    Pushups.track_pushups(img)
                elif exercise_type == "Deadlifts":
                    import Deadlifts
                    Deadlifts.track_deadlifts(img)
                elif exercise_type == "Squats":
                    import Squats
                    Squats.track_squats(img)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
