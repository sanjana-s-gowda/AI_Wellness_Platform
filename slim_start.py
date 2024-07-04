import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial.distance import cosine
import pyttsx3
import time
import os

# Initialize Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Function to process video frame and detect poses
def detect_pose(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)
    return result

# Function to draw pose landmarks on frame
def draw_landmarks(frame, landmarks):
    mp_drawing.draw_landmarks(
        frame,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
    )

# Function to calculate similarity between two sets of landmarks
def calculate_similarity(landmarks1, landmarks2):
    # Flatten landmarks and normalize
    vec1 = np.array([[lm.x, lm.y, lm.z] for lm in landmarks1.landmark]).flatten()
    vec2 = np.array([[lm.x, lm.y, lm.z] for lm in landmarks2.landmark]).flatten()
    
    # Calculate cosine similarity
    similarity = 1 - cosine(vec1, vec2)
    return similarity

# Function to read text aloud
def read_aloud(text):
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Set voice (0 for male, 1 for female, or choose any available voice)
    engine.setProperty('voice', voices[1].id)

    # Set reduced speaking rate
    engine.setProperty('rate', 125)  # Adjust to make it slower, 125 is slower than 150
    engine.setProperty('volume', 0.9)

    engine.say(text)
    engine.runAndWait()

# Function to provide detailed feedback
def provide_feedback(reference_landmarks, user_landmarks):
    feedback = []

    # Example checks for key landmarks (shoulder, hip, and knee as an example)
    key_points = {
        "left_shoulder": 11,
        "right_shoulder": 12,
        "left_hip": 23,
        "right_hip": 24,
        "left_knee": 25,
        "right_knee": 26
    }

    for point_name, index in key_points.items():
        ref_landmark = reference_landmarks.landmark[index]
        user_landmark = user_landmarks.landmark[index]

        if abs(ref_landmark.x - user_landmark.x) > 0.1 or abs(ref_landmark.y - user_landmark.y) > 0.1:
            feedback.append(f"Adjust your {point_name.replace('_', ' ')}")

    return " and ".join(feedback) if feedback else "Pose is correct"

# Load or capture the reference pose
reference_image_path = 'reference_pose.jpg'

# Check if the reference image exists at the specified path
if not os.path.exists(reference_image_path):
    print(f"Error: Could not find the reference image at path: {reference_image_path}")
else:
    reference_image = cv2.imread(reference_image_path)

    if reference_image is None:
        print(f"Error: Could not load the reference image from path: {reference_image_path}")
    else:
        reference_result = detect_pose(reference_image)

        if reference_result.pose_landmarks:
            reference_landmarks = reference_result.pose_landmarks

            # Open video capture (webcam)
            cap = cv2.VideoCapture(0)

            last_feedback_time = 0  # Track the last time feedback was given

            try:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Detect pose
                    result = detect_pose(frame)

                    # Draw landmarks if pose is detected
                    if result.pose_landmarks:
                        draw_landmarks(frame, result.pose_landmarks)

                        # Calculate similarity with reference pose
                        similarity = calculate_similarity(reference_landmarks, result.pose_landmarks)
                        print(f'Similarity: {similarity:.2f}')

                        # Provide detailed feedback
                        feedback = provide_feedback(reference_landmarks, result.pose_landmarks)
                        print(feedback)

                        # Display feedback on the frame
                        cv2.putText(frame, feedback, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if feedback == "Pose is correct" else (0, 0, 255), 2, cv2.LINE_AA)

                        # Read aloud feedback every 20 seconds
                        current_time = time.time()
                        if current_time - last_feedback_time >= 20:
                            read_aloud(feedback)
                            last_feedback_time = current_time

                    # Display the frame
                    cv2.imshow('Pose Detection', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            finally:
                # Ensure the webcam is released and windows are closed
                cap.release()
                cv2.destroyAllWindows()
        else:
            print("Reference pose not detected.")

# Entry point for the program
if __name__ == "__main__":
    text_to_read = "Hello, Arogya here! Your voice assistant is ready to guide you."
    read_aloud(text_to_read)
