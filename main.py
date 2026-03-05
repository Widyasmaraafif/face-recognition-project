import os
import cv2
import time
import pandas as pd
import threading
from datetime import datetime
from deepface import DeepFace

import config
from database import init_db, mark_attendance, get_recent_attendance

# Initialize database
init_db()

# Global variables for recognition
recognition_running = False
latest_frame = None
recognition_results = []
last_detected_info = "Status: Idle"
recent_logs = []
attendance_cache = {}

def recognition_worker():
    """Background worker for face recognition"""
    global recognition_running, latest_frame, recognition_results, last_detected_info, recent_logs
    
    while True:
        if latest_frame is not None and not recognition_running:
            # Check if dataset is empty
            if not os.path.exists(config.DATASET_DIR) or not os.listdir(config.DATASET_DIR):
                last_detected_info = "Status: Dataset Empty"
                time.sleep(1)
                continue
                
            recognition_running = True
            try:
                # Local copy to avoid frame changes during processing
                img_to_process = latest_frame.copy()
                
                results = DeepFace.find(
                    img_path=img_to_process, 
                    db_path=config.DATASET_DIR, 
                    enforce_detection=False,
                    model_name=config.MODEL_NAME,
                    detector_backend=config.DETECTOR_BACKEND,
                    silent=True
                )
                
                recognition_results = results
                
                # Update status
                found_match = False
                for result in results:
                    if not result.empty:
                        found_match = True
                        # Get info from first match
                        match = result.iloc[0]
                        name = os.path.basename(match['identity']).split(".")[0]
                        distance = float(match['distance'])
                        # Convert distance to confidence (approximate for SFace)
                        # SFace threshold is usually around 0.5-0.6
                        confidence = max(0, min(100, (1 - distance) * 100))
                        
                        # Mark attendance
                        markAttendance(name)
                        
                        # Update last detected status
                        current_time = datetime.now().strftime('%H:%M:%S')
                        last_detected_info = f"Last: {name} ({confidence:.1f}%) at {current_time}"
                        
                if not found_match:
                    last_detected_info = "Status: Scanning..."
                
                # Fetch recent logs from DB
                recent_logs = get_recent_attendance(3)
                
            except Exception as e:
                # print(f"Recognition thread error: {e}")
                pass
            finally:
                recognition_running = False
        
        time.sleep(0.1) # Small delay to prevent CPU max-out

def markAttendance(name):
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if already marked within cooldown
    if name in attendance_cache:
        last_seen = attendance_cache[name]
        if (time.time() - last_seen) < config.ATTENDANCE_COOLDOWN:
            return
            
    # Update cache
    attendance_cache[name] = time.time()
    
    # Record to DB
    if mark_attendance(name):
        print(f"Recorded attendance in DB: {name} at {current_time}")
    
    # Record to CSV (Legacy support)
    file_path = config.CSV_LOG_FILE
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['Name', 'Time'])
        df.to_csv(file_path, index=False)
        
    df = pd.DataFrame([[name, current_time]], columns=['Name', 'Time'])
    df.to_csv(file_path, mode='a', header=False, index=False)

# Start recognition thread
thread = threading.Thread(target=recognition_worker, daemon=True)
thread.start()

cap = cv2.VideoCapture(0)
print(f"Initializing AI System using {config.MODEL_NAME} with Threading...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Update the frame for recognition thread
    latest_frame = frame.copy()
    
    # Draw results from the background thread
    for result in recognition_results:
        if not result.empty:
            match = result.iloc[0]
            name = os.path.basename(match['identity']).split(".")[0]
            
            # Get coordinates
            x = int(match['source_x'])
            y = int(match['source_y'])
            w = int(match['source_w'])
            h = int(match['source_h'])
            
            # Draw rectangle and name
            distance = float(match['distance'])
            confidence = max(0, min(100, (1 - distance) * 100))
            label = f"{name} ({confidence:.0f}%)"
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

    # Draw Status Bar (Top)
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
    cv2.putText(frame, last_detected_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Draw History (Bottom Right)
    if recent_logs:
        h_frame, w_frame, _ = frame.shape
        start_y = h_frame - (len(recent_logs) * 30) - 20
        cv2.rectangle(frame, (w_frame - 250, start_y - 30), (w_frame, h_frame), (0, 0, 0), -1)
        cv2.putText(frame, "Recent Logs:", (w_frame - 240, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        for i, (name, timestamp) in enumerate(recent_logs):
            log_time = timestamp.split(" ")[1] if " " in timestamp else timestamp
            text = f"{name} - {log_time}"
            cv2.putText(frame, text, (w_frame - 240, start_y + (i * 30) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Show video feed
    cv2.imshow("Face Recognition Attendance System (Threaded)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()