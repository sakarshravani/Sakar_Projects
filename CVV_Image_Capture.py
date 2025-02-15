import cv2
import numpy as np
import mediapipe as mp
from datetime import datetime

# Initialize MediaPipe Pose and Holistic
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Video source
video_path = '5features_ch03_20241009094643.mp4'
cap = cv2.VideoCapture(video_path)

# Define constants and thresholds
roi_x, roi_y, roi_width, roi_height = 1300, 70, 90, 150  # Train motion ROI
standing_threshold = 0.3       # Threshold for ALP posture
door_threshold_x = (0.63, 0.80)  # Left shoulder range for door detection
gesture_threshold_y = 0.3      # Threshold for hand gesture
train_motion_diff_threshold = 500

# Function to capture screenshot
def take_screenshot(frame, feature_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{feature_name}_{timestamp}.png"
    cv2.imwrite(filename, frame)
    print(f"Screenshot saved: {filename}")

# Function for train motion detection (for display only)
def detect_train_motion(prev_gray_roi, current_roi):
    gray_roi = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(prev_gray_roi, gray_roi)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    motion_pixels = cv2.countNonZero(thresh)
    motion_state = "in Motion" if motion_pixels > train_motion_diff_threshold else "at HALT"
    return gray_roi, motion_state

# Function for ALP posture detection
def detect_alp_posture(results, frame_height):
    if results.pose_landmarks:
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        return "ALP Standing" if shoulder_y < standing_threshold else "ALP Sitting"
    return None

# Function for ALP door proximity detection
def detect_alp_near_door(results, frame_width):
    if results.pose_landmarks:
        left_shoulder_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * frame_width
        if door_threshold_x[0] * frame_width <= left_shoulder_x <= door_threshold_x[1] * frame_width:
            return "ALP near the door"
        else:
            return "ALP away from the door"
    return None

# Updated function for hand gesture detection
def detect_hand_gesture(results, frame):
    h, w, _ = frame.shape
    # Check for left hand landmarks
    if hasattr(results, 'left_hand_landmarks') and results.left_hand_landmarks:
        left_wrist_y = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].y
        if left_wrist_y < gesture_threshold_y:
            # Use pose landmarks for angle calculation (if available)
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

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Second point (vertex)
    c = np.array(c)  # Third point
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))  # Clip to avoid numerical errors
    return np.degrees(angle)

# Initialize for train motion detection
ret, prev_frame = cap.read()
if not ret:
    print("Error: Unable to read the video.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

prev_roi = prev_frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
prev_gray_roi = cv2.cvtColor(prev_roi, cv2.COLOR_BGR2GRAY)

# Variables to store previous states for combined conditions
prev_alp_standing_near_door = False
prev_left_hand_raised = False

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_holistic.Holistic(static_image_mode=False, min_detection_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_height, frame_width, _ = frame.shape
        current_roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
        
        # Train motion detection (for display only)
        prev_gray_roi, train_motion_state = detect_train_motion(prev_gray_roi, current_roi)
        cv2.putText(frame, f"Train State: {train_motion_state}", (10, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Convert frame to RGB for processing
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

        # Hand gesture detection (pass the current frame as well)
        hand_gesture = detect_hand_gesture(results_holistic, frame)
        cv2.putText(frame, f"Gesture: {hand_gesture}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 255, 55), 2)
        
        # Draw a circle at the tip of the left index finger (landmark 8) if available
        if results_holistic.left_hand_landmarks:
            landmark = results_holistic.left_hand_landmarks.landmark[8]  # Landmark 8 (index finger tip)
            cx, cy = int(landmark.x * frame_width), int(landmark.y * frame_height)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Combined condition: ALP Standing near the door
        current_alp_standing_near_door = (alp_posture == "ALP Standing" and alp_door == "ALP near the door")
        if current_alp_standing_near_door and not prev_alp_standing_near_door:
            take_screenshot(frame, "ALP_Standing_Near_the_Door")
        
        # Condition for left hand raised
        current_left_hand_raised = (hand_gesture == "Left Hand Raised")
        if current_left_hand_raised and not prev_left_hand_raised:
            take_screenshot(frame, "Left_Hand_Raised")
        
        # Update previous states for combined conditions
        prev_alp_standing_near_door = current_alp_standing_near_door
        prev_left_hand_raised = current_left_hand_raised

        # Display the frame
        cv2.imshow('Combined Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
