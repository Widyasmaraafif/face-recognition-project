from deepface import DeepFace
import cv2
import os
from datetime import datetime
import pandas as pd

def markAttendance(name):
    now = datetime.now()
    timeString = now.strftime('%H:%M:%S')
    with open('attendance.csv', 'a') as f:
        f.write(f'\n{name},{timeString}')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imwrite("frame.jpg", frame)

    try:
        result = DeepFace.find(
            img_path="frame.jpg",
            db_path="dataset",
            enforce_detection=False
        )

        if len(result[0]) > 0:
            name = os.path.basename(result[0].iloc[0]['identity']).split(".")[0]
            markAttendance(name)
            print("Detected:", name)

    except:
        pass

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()