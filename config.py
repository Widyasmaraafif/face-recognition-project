import os

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# AI Model configuration
# Alternatives: "VGG-Face" (580MB), "Facenet" (92MB), "SFace" (37MB)
MODEL_NAME = "SFace" 
DETECTOR_BACKEND = "opencv" # Faster for real-time

# Attendance configuration
ATTENDANCE_COOLDOWN = 60 # seconds (1 minute)

# File and directory paths
DATASET_DIR = "dataset"
DB_NAME = "attendance_system.db"
CSV_LOG_FILE = "attendance.csv" # Still keep for fallback or compatibility

# Create dataset directory if not exists
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)
