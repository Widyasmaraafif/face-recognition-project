import os
# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from deepface import DeepFace
import cv2
from datetime import datetime
import pandas as pd
import time

# AI Model configuration
# Alternatives: "VGG-Face" (580MB), "Facenet" (92MB), "SFace" (37MB)
MODEL_NAME = "SFace" 
DETECTOR_BACKEND = "opencv" # Faster for real-time

# Create dataset directory if not exists
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Attendance tracking dictionary to avoid duplicates
# Format: { "name": last_seen_time }
attendance_cache = {}
ATTENDANCE_COOLDOWN = 60 # seconds

def markAttendance(name):
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if already marked within cooldown
    if name in attendance_cache:
        last_seen = attendance_cache[name]
        if (time.time() - last_seen) < ATTENDANCE_COOLDOWN:
            return
            
    # Update cache
    attendance_cache[name] = time.time()
    
    # Record to CSV
    file_path = 'attendance.csv'
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['Name', 'Time'])
        df.to_csv(file_path, index=False)
        
    df = pd.DataFrame([[name, current_time]], columns=['Name', 'Time'])
    df.to_csv(file_path, mode='a', header=False, index=False)
    print(f"Recorded attendance for: {name} at {current_time}")

cap = cv2.VideoCapture(0)
frame_count = 0
process_every_n_frames = 15 # Process every 15 frames to avoid lag
last_detected_info = "Status: Idle"

print(f"Initializing AI System using {MODEL_NAME}...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame_count += 1
    
    # Process recognition periodically
    if frame_count % process_every_n_frames == 0:
        # Check if dataset is empty
        if not os.path.exists("dataset") or not os.listdir("dataset"):
            last_detected_info = "Status: Dataset Empty"
        else:
            try:
                results = DeepFace.find(
                    img_path=frame, 
                    db_path="dataset", 
                    enforce_detection=False,
                    model_name=MODEL_NAME,
                    detector_backend=DETECTOR_BACKEND,
                    silent=True
                )
                
                found_match = False
                # Draw bounding boxes and names
                for result in results:
                    if not result.empty:
                        found_match = True
                        # Get info from first match
                        match = result.iloc[0]
                        name = os.path.basename(match['identity']).split(".")[0]
                        
                        # Get coordinates (x, y, w, h)
                        x = int(match['source_x'])
                        y = int(match['source_y'])
                        w = int(match['source_w'])
                        h = int(match['source_h'])
                        
                        # Draw rectangle
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                        
                        # Update last detected status
                        current_time = datetime.now().strftime('%H:%M:%S')
                        last_detected_info = f"Last: {name} at {current_time}"
                        
                        # Mark attendance
                        markAttendance(name)
                
                if not found_match:
                    last_detected_info = "Status: Scanning..."
            except Exception as e:
                # print(f"Recognition error: {e}")
                pass

    # Draw Status Bar
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
    cv2.putText(frame, last_detected_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show video feed
    cv2.imshow("Face Recognition Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()