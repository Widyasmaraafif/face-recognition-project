import os
import cv2
import base64
import numpy as np
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from deepface import DeepFace

import config
from database import init_db, mark_attendance, get_recent_attendance

# Initialize Flask and Database
app = Flask(__name__)
CORS(app)
init_db()

# Attendance cache
attendance_cache = {}

def process_frame(img_base64):
    """Processes a base64 encoded frame for face recognition"""
    try:
        # Decode base64 to image
        img_data = base64.b64decode(img_base64.split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Recognition using DeepFace
        results = DeepFace.find(
            img_path=frame, 
            db_path=config.DATASET_DIR, 
            enforce_detection=False,
            model_name=config.MODEL_NAME,
            detector_backend=config.DETECTOR_BACKEND,
            silent=True
        )
        
        recognition_data = []
        for result in results:
            if not result.empty:
                match = result.iloc[0]
                name = os.path.basename(match['identity']).split(".")[0]
                distance = float(match['distance'])
                confidence = max(0, min(100, (1 - distance) * 100))
                
                # Get coordinates
                x, y, w, h = int(match['source_x']), int(match['source_y']), int(match['source_w']), int(match['source_h'])
                
                recognition_data.append({
                    "name": name,
                    "confidence": round(confidence, 1),
                    "box": [x, y, w, h]
                })
                
                # Mark attendance with cooldown
                handle_attendance(name)
        
        return recognition_data
    except Exception as e:
        # print(f"Processing error: {e}")
        return []

def handle_attendance(name):
    """Marks attendance with cooldown logic"""
    now = time.time()
    if name in attendance_cache:
        if (now - attendance_cache[name]) < config.ATTENDANCE_COOLDOWN:
            return
    
    attendance_cache[name] = now
    mark_attendance(name)
    print(f"Recorded attendance for {name} via Web")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "No image data"}), 400
    
    results = process_frame(data['image'])
    recent_logs = get_recent_attendance(5)
    
    return jsonify({
        "results": results,
        "recent_logs": [{"name": r[0], "time": r[1].split(" ")[1]} for r in recent_logs]
    })

if __name__ == '__main__':
    # Use 0.0.0.0 to allow external access (important for online/LAN)
    app.run(host='0.0.0.0', port=5000, debug=False)
