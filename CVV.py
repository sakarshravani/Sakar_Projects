import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Pose and Holistic
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Load the video
video_path = '5features_ch03_20241009094643.mp4'
cap = cv2.VideoCapture(video_path)

# Define constants and thresholds
roi_x, roi_y, roi_width, roi_height = 1300, 70, 90, 150  # Train motion ROI
standing_threshold = 0.3      # Threshold for ALP posture
door_threshold_x = (0.63, 0.80)  # Left shoulder range for door detection
gesture_threshold_y = 0.3  # Threshold for hand gesture
train_motion_diff_threshold = 500

# Function for train motion detection
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

# Function for hand gesture detection
def detect_hand_gesture(results, frame_height):
    if results.pose_landmarks:
        h, w, _ = frame.shape
        landmarks = results.pose_landmarks.landmark
        
        # Get coordinates
        shoulder = [landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].x * w,
                    landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].y * h]
        elbow = [landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].x * w,
                 landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].y * h]
        wrist = [landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x * w, 
                 landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].y * h]

        if hasattr(results, 'left_hand_landmarks') and results.left_hand_landmarks:
            left_wrist_y = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].y
            if left_wrist_y < gesture_threshold_y:
                if calculate_angle(shoulder, elbow, wrist) > 120:
                    return "Left Hand Raised"
        
        if hasattr(results, 'right_hand_landmarks') and results.right_hand_landmarks:
            right_wrist_y = results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].y
            if right_wrist_y < gesture_threshold_y:
                if calculate_angle(shoulder, elbow, wrist) > 120:
                    return "Right Hand Raised"
    
    return None

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

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_holistic.Holistic(static_image_mode=False, min_detection_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_height, frame_width, _ = frame.shape
        current_roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
        
        # Train motion detection
        prev_gray_roi, train_motion_state = detect_train_motion(prev_gray_roi, current_roi)
        cv2.putText(frame, f"Train State: {train_motion_state}", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # ALP posture and door detection
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_pose = pose.process(image_rgb)
        alp_posture = detect_alp_posture(results_pose, frame_height)
        alp_door = detect_alp_near_door(results_pose, frame_width)

        #if alp_posture:
        cv2.putText(frame, f"Posture: {alp_posture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #if alp_door:
        cv2.putText(frame, f"At Door: {alp_door}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 145, 0), 2)

        # Hand gesture detection
        results_holistic = holistic.process(image_rgb)
        hand_gesture = detect_hand_gesture(results_holistic, frame_height)
        #if hand_gesture:
        cv2.putText(frame, f"Gesture: {hand_gesture}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 255, 55), 2)
        
        # Draw a circle at the tip of the index finger (landmark 8)
        if results_holistic.left_hand_landmarks:  # Check for left hand landmarks
            landmark = results_holistic.left_hand_landmarks.landmark[8]  # Landmark 8 (index finger tip)
            cx, cy = int(landmark.x * frame_width), int(landmark.y * frame_height)  # Pixel coordinates
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # Green circle

        # Display the frame
        cv2.imshow('Combined Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()




