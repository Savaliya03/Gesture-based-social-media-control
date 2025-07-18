import cv2
import mediapipe as mp
import time
from controller import Controller

def main():
    # Initialize MediaPipe with improved settings
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,  # Only detect one hand at a time
        min_detection_confidence=0.6,  # Slightly lower to improve detection rate
        min_tracking_confidence=0.6,   # Improved tracking
        model_complexity=1            # Better accuracy
    )
    mp_draw = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera. Check if camera is connected.")
        return
        
    # Attempt to set higher resolution for better hand detection
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Set window name
    window_name = "Hand Gesture Video Controller"
    cv2.namedWindow(window_name)
    
    # Variables for FPS calculation
    previous_time = 0
    current_time = 0
    
    # Variables for UI and status tracking
    gesture_history = []
    max_history = 5
    last_status = "No hand detected"
    status_stability_counter = 0
    stability_threshold = 3
    
    print("\n" + "="*50)
    print("Hand Gesture Video Controller Started!")
    print("="*50)
    print("\nGESTURE GUIDE:")
    print("- Open palm: Play video")
    print("- Closed palm: Stop video")
    print("- Index finger up: Move cursor")
    print("- Index + Middle fingers up: single click")
    print("- Index + Middle + Ring fingers up: Zoom in")
    print("- All four fingers up: Zoom out")
    print("- Index finger pointing left/right: Timeline backward/forward")
    print("- Thumb up/down: Scroll up/down")
    print("- Ring + Pinky fingers up: Fast forward")
    print("- Index + Pinky fingers up: Go back")
    print("="*50)
    print("Press 'q' to quit, 'r' to reset controller state")
    print("="*50 + "\n")
    
    while cap.isOpened():
        # Read frame from webcam
        success, image = cap.read()
        if not success:
            print("Failed to capture image from camera.")
            break
            
        # Flip the image horizontally for a more intuitive mirror view
        image = cv2.flip(image, 1)
        
        # Improve performance by making image non-writeable
        image.flags.writeable = False
        
        # Convert image to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image with MediaPipe
        results = hands.process(image_rgb)
        
        # Make image writeable again for drawing
        image.flags.writeable = True
        
        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time) if (current_time - previous_time) > 0 else 0
        previous_time = current_time
        
        # Draw FPS on image
        cv2.putText(image, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Reset Controller.hand_Landmarks if no hands detected
        if not results.multi_hand_landmarks:
            Controller.hand_Landmarks = None
            
        # Draw status text
        status_text = "No hand detected"
        status_color = (0, 0, 255)  # Red
        
        # Check if hand(s) detected
        if results.multi_hand_landmarks:
            # Get first hand detected
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Draw landmarks on image with better visibility
            mp_draw.draw_landmarks(
                image, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # Update controller with hand landmarks
            Controller.hand_Landmarks = hand_landmarks
            
            # Process gestures
            Controller.process_hand_gestures()
            
            # Update status text
            status_text = "Hand detected"
            status_color = (0, 255, 0)  # Green
            
            # Show active gesture - more comprehensive status
            active_gestures = []
            if Controller.playing_video:
                active_gestures.append("Playing")
            if Controller.cursor_moving:
                active_gestures.append("Moving Cursor")
            if Controller.zooming_in:
                active_gestures.append("Zooming In")
            if Controller.zooming_out:
                active_gestures.append("Zooming Out")
            if Controller.scrolling_up:
                active_gestures.append("Scrolling Up")
            if Controller.scrolling_down:
                active_gestures.append("Scrolling Down")
            if Controller.timeline_forward:
                active_gestures.append("Timeline Forward")
            if Controller.timeline_backward:
                active_gestures.append("Timeline Backward")
            if Controller.fast_forwarding:
                active_gestures.append("Fast Forward")
            if Controller.going_back:
                active_gestures.append("Going Back")
                
            if active_gestures:
                status_text += " - " + ", ".join(active_gestures)
                
                # Add to gesture history
                if active_gestures[0] not in gesture_history:
                    gesture_history.append(active_gestures[0])
                    if len(gesture_history) > max_history:
                        gesture_history.pop(0)
        
        # Stabilize status display to avoid flickering
        if status_text == last_status:
            status_stability_counter += 1
        else:
            status_stability_counter = 0
            last_status = status_text
        
        # Only update displayed status if stable for a few frames
        if status_stability_counter >= stability_threshold:
            displayed_status = status_text
        else:
            displayed_status = last_status
            
        # Draw status text
        cv2.putText(image, displayed_status, (10, image.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        # Draw recent gesture history
        for i, gesture in enumerate(reversed(gesture_history)):
            cv2.putText(image, gesture, (image.shape[1] - 200, 30 + i * 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Draw finger status indicators for debugging
        if Controller.hand_Landmarks:
            finger_status = ""
            if Controller.index_finger_up:
                finger_status += "I"
            if Controller.middle_finger_up:
                finger_status += "M"
            if Controller.ring_finger_up:
                finger_status += "R"
            if Controller.pinky_finger_up:
                finger_status += "P"
            if Controller.thumb_up:
                finger_status += "T"
                
            cv2.putText(image, f"Fingers: {finger_status}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
        # Show image
        cv2.imshow(window_name, image)
        
        # Check for key presses
        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            # Reset controller state
            Controller.prev_hand = None
            Controller.playing_video = False
            Controller.cursor_moving = False
            Controller.zooming_in = False
            Controller.zooming_out = False
            Controller.scrolling_up = False
            Controller.scrolling_down = False
            Controller.fast_forwarding = False
            Controller.going_back = False
            Controller.timeline_forward = False
            Controller.timeline_backward = False
            print("Controller state reset")
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


#   venv\Scripts\activate
#   python app.py