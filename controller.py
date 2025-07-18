import pyautogui
import time
import math

class Controller:
    # Static variables for tracking state
    prev_hand = None
    last_gesture_time = 0
    
    # Gesture states
    playing_video = False
    cursor_moving = False
    zooming_in = False
    zooming_out = False
    scrolling_up = False
    scrolling_down = False
    fast_forwarding = False
    going_back = False
    timeline_forward = False
    timeline_backward = False
    
    # Hand landmarks from MediaPipe
    hand_Landmarks = None
    
    # Finger status indicators
    index_finger_up = None
    middle_finger_up = None
    ring_finger_up = None
    pinky_finger_up = None
    thumb_up = None
    
    # Combined finger states
    open_palm = None
    closed_palm = None
    
    # Screen size for mapping coordinates
    screen_width, screen_height = pyautogui.size()
    
    # Gesture cooldown in seconds - reduced for more responsive control
    GESTURE_COOLDOWN = 0.3

    @staticmethod
    def update_fingers_status():
        """Update the status of all fingers based on current hand landmarks with improved detection"""
        if Controller.hand_Landmarks is None:
            return
            
        # Improved finger up/down detection with better thresholds
        # For each finger, compare tip (knuckle) position with base position
        # A finger is considered "up" if its tip is significantly higher than its base
        
        # Define threshold for clearer detection
        threshold = 0.07
        
        # Check if fingers are up (tip position is higher than base position)
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < (Controller.hand_Landmarks.landmark[5].y - threshold)
        Controller.middle_finger_up = Controller.hand_Landmarks.landmark[12].y < (Controller.hand_Landmarks.landmark[9].y - threshold)
        Controller.ring_finger_up = Controller.hand_Landmarks.landmark[16].y < (Controller.hand_Landmarks.landmark[13].y - threshold)
        Controller.pinky_finger_up = Controller.hand_Landmarks.landmark[20].y < (Controller.hand_Landmarks.landmark[17].y - threshold)
        
        # Thumb is special as it moves more horizontally
        # Detect if thumb is extended away from palm
        thumb_tip = Controller.hand_Landmarks.landmark[4]
        thumb_base = Controller.hand_Landmarks.landmark[2]
        wrist = Controller.hand_Landmarks.landmark[0]
        
        # Calculate Euclidean distance between thumb tip and wrist
        # compared to distance between thumb base and wrist
        thumb_tip_dist = math.sqrt((thumb_tip.x - wrist.x)**2 + (thumb_tip.y - wrist.y)**2)
        thumb_base_dist = math.sqrt((thumb_base.x - wrist.x)**2 + (thumb_base.y - wrist.y)**2)
        
        # Thumb is "up" if its tip is significantly farther from wrist than its base
        Controller.thumb_up = thumb_tip_dist > (thumb_base_dist * 1.2)
        
        # Combined finger states with improved reliability
        Controller.open_palm = (Controller.index_finger_up and 
                               Controller.middle_finger_up and 
                               Controller.ring_finger_up and 
                               Controller.pinky_finger_up)
        
        Controller.closed_palm = (not Controller.index_finger_up and 
                                 not Controller.middle_finger_up and 
                                 not Controller.ring_finger_up and 
                                 not Controller.pinky_finger_up)
    
    @staticmethod
    def get_position(hand_x_position, hand_y_position):
        """Convert hand position to screen position with improved smoothing"""
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * Controller.screen_width)
        current_y = int(hand_y_position * Controller.screen_height)

        # Increased sensitivity for easier movement
        ratio = 1.5
        Controller.prev_hand = (current_x, current_y) if Controller.prev_hand is None else Controller.prev_hand
        
        # Calculate movement delta
        delta_x = current_x - Controller.prev_hand[0]
        delta_y = current_y - Controller.prev_hand[1]
        
        # Apply smoothing - more aggressive for small movements, less for large movements
        smoothing = 0.5 if max(abs(delta_x), abs(delta_y)) < 20 else 0.8
        
        # Update previous hand position with smoothing
        Controller.prev_hand = [
            Controller.prev_hand[0] + delta_x * smoothing,
            Controller.prev_hand[1] + delta_y * smoothing
        ]
        
        # Calculate new cursor position
        current_x, current_y = old_x + delta_x * ratio, old_y + delta_y * ratio

        # Boundary checks with buffer
        threshold = 10
        if current_x < threshold:
            current_x = threshold
        elif current_x > Controller.screen_width - threshold:
            current_x = Controller.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > Controller.screen_height - threshold:
            current_y = Controller.screen_height - threshold

        return (current_x, current_y)
    
    @staticmethod
    def is_cooldown_passed():
        """Check if enough time has passed since the last gesture activation"""
        current_time = time.time()
        if current_time - Controller.last_gesture_time >= Controller.GESTURE_COOLDOWN:
            Controller.last_gesture_time = current_time
            return True
        return False
    
    @staticmethod
    def detect_cursor_movement():
        """Only move cursor if index finger is up and others are down"""
        if Controller.index_finger_up and not Controller.middle_finger_up and not Controller.ring_finger_up and not Controller.pinky_finger_up:
            # Using index finger tip for movement
            point = 8  # Index finger tip
            current_x, current_y = Controller.hand_Landmarks.landmark[point].x, Controller.hand_Landmarks.landmark[point].y
            x, y = Controller.get_position(current_x, current_y)
            pyautogui.moveTo(x, y, duration=0)
            Controller.cursor_moving = True
            print("Moving Cursor")
        else:
            Controller.cursor_moving = False
    
    @staticmethod
    def detect_play_stop():
        """Open palm to play video, closed palm to stop video"""
        if Controller.open_palm and not Controller.playing_video and Controller.is_cooldown_passed():
            pyautogui.press('space')  # Play video
            Controller.playing_video = True
            print("Playing Video")
        elif Controller.closed_palm and Controller.playing_video and Controller.is_cooldown_passed():
            pyautogui.press('space')  # Stop video
            Controller.playing_video = False
            print("Stopping Video")
    
    @staticmethod
    def detect_single_click():
        """Index and middle fingers up for single click"""
        single_click_condition = (Controller.index_finger_up and 
                                Controller.middle_finger_up and 
                                not Controller.ring_finger_up and 
                                not Controller.pinky_finger_up)
    
        if single_click_condition and Controller.is_cooldown_passed():
            # Single click at current cursor position
            pyautogui.click()
            print("Clicking")

    
    @staticmethod
    def detect_zoom():
        """
        Index, middle, ring fingers up for zoom in
        All four fingers up for zoom out
        """
        zoom_in_condition = (Controller.index_finger_up and 
                            Controller.middle_finger_up and 
                            Controller.ring_finger_up and 
                            not Controller.pinky_finger_up)
        
        zoom_out_condition = Controller.open_palm
        
        if zoom_in_condition and not Controller.zooming_in and Controller.is_cooldown_passed():
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(120)  # Zoom in
            pyautogui.keyUp('ctrl')
            Controller.zooming_in = True
            print("Zooming In")
        elif not zoom_in_condition:
            Controller.zooming_in = False
            
        if zoom_out_condition and not Controller.zooming_out and Controller.is_cooldown_passed():
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-120)  # Zoom out
            pyautogui.keyUp('ctrl')
            Controller.zooming_out = True
            print("Zooming Out")
        elif not zoom_out_condition:
            Controller.zooming_out = False
    
    @staticmethod
    def detect_timeline_navigation():
        """
        Index finger pointing left for backward timeline 
        Index finger pointing right for forward timeline
        Improved detection using the direction of the pointing index finger
        """
        if Controller.index_finger_up and not Controller.middle_finger_up and not Controller.ring_finger_up and not Controller.pinky_finger_up:
            # Get wrist, index base and tip positions to determine pointing direction more accurately
            wrist_x = Controller.hand_Landmarks.landmark[0].x
            index_base_x = Controller.hand_Landmarks.landmark[5].x
            index_tip_x = Controller.hand_Landmarks.landmark[8].x
            
            # Calculate direction vector
            base_to_tip_x = index_tip_x - index_base_x
            
            # Stronger thresholds for more reliable detection
            pointing_left = base_to_tip_x < -0.05
            pointing_right = base_to_tip_x > 0.05
            
            if pointing_left and not Controller.timeline_backward and Controller.is_cooldown_passed():
                pyautogui.press('left')  # Go backward in timeline
                Controller.timeline_backward = True
                print("Timeline Backward")
            elif not pointing_left:
                Controller.timeline_backward = False
                
            if pointing_right and not Controller.timeline_forward and Controller.is_cooldown_passed():
                pyautogui.press('right')  # Go forward in timeline
                Controller.timeline_forward = True
                print("Timeline Forward")
            elif not pointing_right:
                Controller.timeline_forward = False
    
    @staticmethod
    def detect_scroll():
        """
        Thumb up for scroll up
        Thumb down for scroll down
        With improved detection of thumb orientation
        """
        thumb_tip_y = Controller.hand_Landmarks.landmark[4].y
        thumb_base_y = Controller.hand_Landmarks.landmark[2].y
        
        thumb_pointing_up = thumb_tip_y < thumb_base_y - 0.05
        thumb_pointing_down = thumb_tip_y > thumb_base_y + 0.05
        
        if thumb_pointing_up and not Controller.scrolling_up and Controller.is_cooldown_passed():
            pyautogui.scroll(150)  # Increased scroll amount for better visibility
            Controller.scrolling_up = True
            print("Scrolling Up")
        elif not thumb_pointing_up:
            Controller.scrolling_up = False
            
        if thumb_pointing_down and not Controller.scrolling_down and Controller.is_cooldown_passed():
            pyautogui.scroll(-150)  # Increased scroll amount for better visibility
            Controller.scrolling_down = True
            print("Scrolling Down")
        elif not thumb_pointing_down:
            Controller.scrolling_down = False
    
    @staticmethod
    def detect_fast_forward():
        """Ring and pinky fingers up for fast forward"""
        fast_forward_condition = (not Controller.index_finger_up and 
                                 not Controller.middle_finger_up and 
                                 Controller.ring_finger_up and 
                                 Controller.pinky_finger_up)
        
        if fast_forward_condition and not Controller.fast_forwarding and Controller.is_cooldown_passed():
            # Try multiple fast forward shortcuts as they vary by video player
            pyautogui.press('f')  # Common shortcut for full screen
            pyautogui.press('l')  # YouTube fast forward
            pyautogui.press('right', presses=5)  # Multiple right presses for bigger jumps
            
            Controller.fast_forwarding = True
            print("Fast Forward")
        elif not fast_forward_condition:
            Controller.fast_forwarding = False
    
    @staticmethod
    def detect_go_back():
        """Index and pinky fingers up for go back event"""
        go_back_condition = (Controller.index_finger_up and 
                            not Controller.middle_finger_up and 
                            not Controller.ring_finger_up and 
                            Controller.pinky_finger_up)
        
        if go_back_condition and not Controller.going_back and Controller.is_cooldown_passed():
            # Try multiple back shortcuts
            pyautogui.press('esc')  # Common shortcut for back/cancel
            pyautogui.hotkey('alt', 'left')  # Browser back
            
            Controller.going_back = True
            print("Going Back")
        elif not go_back_condition:
            Controller.going_back = False
    
    @staticmethod
    def process_hand_gestures():
        """Main method to process all hand gestures"""
        if Controller.hand_Landmarks is None:
            return
            
        # Update finger statuses first
        Controller.update_fingers_status()
        
        # Process gestures in order of priority
        Controller.detect_play_stop()
        Controller.detect_cursor_movement()
        Controller.detect_single_click()
        Controller.detect_zoom()
        Controller.detect_timeline_navigation()
        Controller.detect_scroll()
        Controller.detect_fast_forward()
        Controller.detect_go_back()