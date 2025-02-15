import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from datetime import datetime

# ----------------------------
# Initialization
# ----------------------------
# Initialize MediaPipe Pose and Holistic
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Video source (use absolute path)
video_path = '5features_ch03_20241009094643.mp4'
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Unable to open video file:", video_path)
    exit()

# Get frame rate (fps)
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30  # fallback

# Duration settings: 5 seconds before and 5 seconds after the event.
pre_event_frames = int(fps * 5)    # Pre-event buffer: last 5 seconds
post_event_frames = int(fps * 5)     # Post-event recording: next 5 seconds

# Cooldown (in seconds) so that the same event isn't recorded repeatedly
cooldown = 10
last_alp_standing_recorded = 0
last_left_hand_recorded = 0

# Define constants and thresholds
roi_x, roi_y, roi_width, roi_height = 1300, 70, 90, 150  # (Unused for event capture)
standing_threshold = 0.3
door_threshold_x = (0.63, 0.80)
gesture_threshold_y = 0.3
train_motion_diff_threshold = 500

# ----------------------------
# Pre-event Buffer & Recorders
# ----------------------------
pre_event_buffer = deque(maxlen=pre_event_frames)
event_recorders = {}  # Holds active post-event recorders

# List to hold filenames of recorded event videos
event_filenames = []

# Define codec and fourcc for VideoWriter (using mp4v)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# ----------------------------
# Utility Functions
# ----------------------------
def detect_train_motion(prev_gray_roi, current_roi):
    gray_roi = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(prev_gray_roi, gray_roi)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    motion_pixels = cv2.countNonZero(thresh)
    motion_state = "in Motion" if motion_pixels > train_motion_diff_threshold else "at HALT"
    return gray_roi, motion_state

def detect_alp_posture(results, frame_height):
    if results.pose_landmarks:
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        return "ALP Standing" if shoulder_y < standing_threshold else "ALP Sitting"
    return None

def detect_alp_near_door(results, frame_width):
    if results.pose_landmarks:
        left_shoulder_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * frame_width
        if door_threshold_x[0] * frame_width <= left_shoulder_x <= door_threshold_x[1] * frame_width:
            return "ALP near the door"
        else:
            return "ALP away from the door"
    return None

def detect_hand_gesture(results, frame):
    h, w, _ = frame.shape
    if hasattr(results, 'left_hand_landmarks') and results.left_hand_landmarks:
        left_wrist_y = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].y
        if left_wrist_y < gesture_threshold_y:
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w, 
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]
                if calculate_angle(shoulder, elbow, wrist) > 120:
                    return "Left Hand Raised"
    return "None"

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# ----------------------------
# Initial Setup for Display
# ----------------------------
ret, prev_frame = cap.read()
if not ret:
    print("Error: Unable to read the video.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

prev_roi = prev_frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
prev_gray_roi = cv2.cvtColor(prev_roi, cv2.COLOR_BGR2GRAY)

prev_alp_standing_near_door = False
prev_left_hand_raised = False

# ----------------------------
# Main Loop: Capture Event Videos
# ----------------------------
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_holistic.Holistic(static_image_mode=False, min_detection_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_height, frame_width, _ = frame.shape
        
        # Append current frame to pre-event buffer (store a copy)
        pre_event_buffer.append(frame.copy())
        
        current_roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
        
        # For display: Train motion detection (not used for event capture)
        prev_gray_roi, train_motion_state = detect_train_motion(prev_gray_roi, current_roi)
        cv2.putText(frame, f"Train State: {train_motion_state}", (10, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Process frame for pose and hand landmarks
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_pose = pose.process(image_rgb)
        results_holistic = holistic.process(image_rgb)
        
        # ALP posture and door detection
        alp_posture = detect_alp_posture(results_pose, frame_height)
        alp_door = detect_alp_near_door(results_pose, frame_width)
        cv2.putText(frame, f"Posture: {alp_posture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"At Door: {alp_door}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 145, 0), 2)
        
        # Hand gesture detection
        hand_gesture = detect_hand_gesture(results_holistic, frame)
        cv2.putText(frame, f"Gesture: {hand_gesture}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 255, 55), 2)
        
        # Draw a circle at the tip of the left index finger if available
        if results_holistic.left_hand_landmarks:
            landmark = results_holistic.left_hand_landmarks.landmark[8]
            cx, cy = int(landmark.x * frame_width), int(landmark.y * frame_height)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        
        current_time = datetime.now().timestamp()
        
        # Event 1: ALP Standing near the door
        current_alp_standing_near_door = (alp_posture == "ALP Standing" and alp_door == "ALP near the door")
        if (current_alp_standing_near_door and not prev_alp_standing_near_door and 
            (current_time - last_alp_standing_recorded > cooldown)):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ALP_Standing_Near_the_Door_{timestamp}.mp4"
            writer = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
            # Write all pre-event frames from the buffer (5 seconds before event)
            for buf_frame in pre_event_buffer:
                writer.write(buf_frame)
            event_recorders["ALP_Standing_Near_the_Door"] = {
                'writer': writer,
                'frames_remaining': post_event_frames
            }
            last_alp_standing_recorded = current_time
            event_filenames.append(filename)
            print(f"Started recording event: {filename}")
        
        # Event 2: Left Hand Raised
        current_left_hand_raised = (hand_gesture == "Left Hand Raised")
        if (current_left_hand_raised and not prev_left_hand_raised and 
            (current_time - last_left_hand_recorded > cooldown)):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Left_Hand_Raised_{timestamp}.mp4"
            writer = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
            for buf_frame in pre_event_buffer:
                writer.write(buf_frame)
            event_recorders["Left_Hand_Raised"] = {
                'writer': writer,
                'frames_remaining': post_event_frames
            }
            last_left_hand_recorded = current_time
            event_filenames.append(filename)
            print(f"Started recording event: {filename}")
        
        prev_alp_standing_near_door = current_alp_standing_near_door
        prev_left_hand_raised = current_left_hand_raised
        
        # Write current frame to active event recorders
        for event in list(event_recorders.keys()):
            recorder = event_recorders[event]
            recorder['writer'].write(frame)
            recorder['frames_remaining'] -= 1
            if recorder['frames_remaining'] <= 0:
                recorder['writer'].release()
                print(f"Finished recording event for {event}")
                del event_recorders[event]
        
        cv2.imshow('Combined Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
for event in event_recorders:
    event_recorders[event]['writer'].release()
cv2.destroyAllWindows()

# ----------------------------
# Merge Event Videos into a Summary Video
# ----------------------------
# Define the output summary filename
summary_filename = "Summary_Events.mp4"
# Create a VideoWriter for the summary video
summary_writer = cv2.VideoWriter(summary_filename, fourcc, fps, (frame_width, frame_height))

# Iterate through each event video file and write its frames to the summary video.
for filename in event_filenames:
    event_cap = cv2.VideoCapture(filename)
    if not event_cap.isOpened():
        print(f"Error: Unable to open event video file: {filename}")
        continue
    while True:
        ret, event_frame = event_cap.read()
        if not ret:
            break
        summary_writer.write(event_frame)
    event_cap.release()

summary_writer.release()
print(f"Summary video created: {summary_filename}")
