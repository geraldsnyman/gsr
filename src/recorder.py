import os
import time
import threading
import datetime
import cv2
import mss
import numpy as np
import json
from PIL import Image
from pynput import keyboard, mouse

class ScreenRecorder:
    def __init__(self, output_dir="recordings"):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(self.base_dir, output_dir)
        self.config_file = os.path.join(self.base_dir, "config.json")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.running = False
        self.recording_thread = None
        self.key_listener = None
        self.mouse_listener = None
        self.mouse_controller =  None
        
        # Default settings
        self.fps = 10
        self.sensitivity = 50 
        self.quality = 100 
        self.tile_divisions = 1 
        self.capture_on_keystroke = False
        
        # Mouse Settings
        self.capture_mouse_click = False
        self.capture_mouse_scroll = False
        self.capture_mouse_move = False
        self.show_cursor = False
        self.cursor_size = 10
        self.cursor_style = "dot" # dot, target, pointer
        
        self.key_pressed = False
        self.mouse_triggered = False
        self.mouse_pos = (0, 0)
        
        self.current_session_dir = None
        self.frame_count = 0
        self.monitor_index = 1 
        self._resolution = self.get_screen_resolution()
        
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.fps = data.get("fps", self.fps)
                    self.sensitivity = data.get("sensitivity", self.sensitivity)
                    self.quality = data.get("quality", self.quality)
                    self.tile_divisions = data.get("tile_divisions", self.tile_divisions)
                    self.capture_on_keystroke = data.get("capture_on_keystroke", self.capture_on_keystroke)
                    self.output_dir = data.get("output_dir", self.output_dir)
                    
                    # Mouse
                    self.capture_mouse_click = data.get("capture_mouse_click", False)
                    self.capture_mouse_scroll = data.get("capture_mouse_scroll", False)
                    self.capture_mouse_move = data.get("capture_mouse_move", False)
                    self.show_cursor = data.get("show_cursor", False)
                    self.cursor_size = data.get("cursor_size", 10)
                    self.cursor_style = data.get("cursor_style", "dot")
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_settings(self):
        data = {
            "fps": self.fps,
            "sensitivity": self.sensitivity,
            "quality": self.quality,
            "tile_divisions": self.tile_divisions,
            "capture_on_keystroke": self.capture_on_keystroke,
            "output_dir": self.output_dir,
            "capture_mouse_click": self.capture_mouse_click,
            "capture_mouse_scroll": self.capture_mouse_scroll,
            "capture_mouse_move": self.capture_mouse_move,
            "show_cursor": self.show_cursor,
            "cursor_size": self.cursor_size,
            "cursor_style": self.cursor_style
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_screen_resolution(self):
        with mss.mss() as sct:
            if self.monitor_index < len(sct.monitors):
                mon = sct.monitors[self.monitor_index]
                return (mon["width"], mon["height"])
            return (1920, 1080) # Fallback

    def start_recording(self):
        if self.running:
            return
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_session_dir = os.path.join(self.output_dir, f"session_{timestamp}")
        os.makedirs(self.current_session_dir, exist_ok=True)
        
        self.running = True
        self.frame_count = 0
        
        if self.capture_on_keystroke:
            self._start_keyboard_listener()

        self.recording_thread = threading.Thread(target=self._record_loop)
        self.recording_thread.start()
        print(f"Recording started. Saving to {self.current_session_dir}")

    def stop_recording(self):
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        if self.recording_thread:
            self.recording_thread.join()
        print("Recording stopped.")

    def set_fps(self, fps):
        self.fps = max(1, min(fps, 60))

    def set_sensitivity(self, sensitivity):
        # sensitivity comes in as 0-100 (from UI slider)
        # We need to map it to a threshold for cv2.mean(diff)
        # A higher UI value usually means "less sensitive" (only large movements trigger)
        # But commonly users think "High Sensitivity" = "Detects generated small movements"
        # Let's clarify:
        # If UI Sensitivity is HIGH (100), we detect small changes -> Threshold is LOW.
        # If UI Sensitivity is LOW (0), we ignore small changes -> Threshold is HIGH.
        
        # Mapping: 
        # UI 0 (Low Sens) -> Threshold 50 (Major changes only)
        # UI 100 (High Sens) -> Threshold 0 (Capture everything)
        # Simple linear map: Threshold = 50 * (1 - (sensitivity / 100))
        self.sensitivity = sensitivity

    def set_quality(self, quality):
        self.quality = max(1, min(quality, 100))

    def set_output_dir(self, path):
        if os.path.isdir(path):
            self.output_dir = path
        else:
            print(f"Invalid directory: {path}")

    def set_tile_divisions(self, divisions):
        self.tile_divisions = max(1, int(divisions))

    def get_tile_resolution(self):
        w, h = self._resolution
        tw = w // self.tile_divisions
        th = h // self.tile_divisions
        return tw, th
        
    
    def set_capture_on_keystroke(self, enabled):
        self.capture_on_keystroke = enabled

    def _on_press(self, key):
        self.key_pressed = True

    def _on_move(self, x, y):
        # Update mouse pos for drawing
        self.mouse_pos = (x, y)
        if self.capture_mouse_move:
            self.mouse_triggered = True

    def _on_click(self, x, y, button, pressed):
        if pressed and self.capture_mouse_click:
            self.mouse_triggered = True

    def _on_scroll(self, x, y, dx, dy):
        if self.capture_mouse_scroll:
            self.mouse_triggered = True

    def _start_input_listeners(self):
        # Keyboard
        self.key_listener = keyboard.Listener(on_press=self._on_press)
        self.key_listener.start()
        
        # Mouse
        self.mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll)
        self.mouse_listener.start()
        
        # Controller for polling position if needed for drawing immediately
        self.mouse_controller = mouse.Controller()

    def start_recording(self):
        if self.running:
            return
            
        self.running = True
        self.key_pressed = False
        self.mouse_triggered = False
        self.frame_count = 0
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_session_dir = os.path.join(self.output_dir, f"session_{timestamp}")
        
        if not os.path.exists(self.current_session_dir):
            os.makedirs(self.current_session_dir)
            
        print(f"Recording started. Saving to {self.current_session_dir}")
        
        self.recording_thread = threading.Thread(target=self._record_loop)
        self.recording_thread.start()
        
        self._start_input_listeners()

    def stop_recording(self):
        self.running = False
        if self.recording_thread:
            self.recording_thread.join()
        
        if self.key_listener:
            self.key_listener.stop()
            self.key_listener = None
            
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            
        print("Recording stopped.")

    def _get_threshold(self):
        # Invert sensitivity for threshold calculation
        # Sensitivity 100 -> Threshold 0 (Capture all)
        # Sensitivity 0 -> Threshold ~50 (Capture only drastic changes)
        return 50 * (1 - (self.sensitivity / 100.0))

    def _record_loop(self):
        prev_frame = None
        interval = 1.0 / self.fps
        
        with mss.mss() as sct:
            monitor = sct.monitors[self.monitor_index]
            
            while self.running:
                start_time = time.time()
                
                # Capture screen
                try:
                    sct_img = sct.grab(monitor)
                    frame = np.array(sct_img)
                    
                    if frame.shape[2] == 4:
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    else:
                        frame_bgr = frame

                    # Draw Cursor if enabled
                    if self.show_cursor:
                        # Get current mouse position (relative to monitor if necessary, but pynput gives global)
                        # Ensure we map global coordinates to the captured monitor area
                        mx, my = self.mouse_controller.position
                        
                        # Adjust for monitor offset
                        rel_x = mx - monitor["left"]
                        rel_y = my - monitor["top"]
                        
                        # Draw Cursor
                        cx, cy = int(rel_x), int(rel_y)
                        radius = self.cursor_size
                        color = (0, 255, 255) # Yellow/Cyan (BGR)
                        thickness = 2
                        
                        if self.cursor_style == "dot":
                            cv2.circle(frame_bgr, (cx, cy), radius, color, -1)
                            
                        elif self.cursor_style == "target":
                            # Circle
                            cv2.circle(frame_bgr, (cx, cy), radius, color, thickness)
                            # Crosshair
                            cv2.line(frame_bgr, (cx - radius - 5, cy), (cx + radius + 5, cy), color, thickness)
                            cv2.line(frame_bgr, (cx, cy - radius - 5), (cx, cy + radius + 5), color, thickness)
                            
                        elif self.cursor_style == "pointer":
                            # Simple Triangle
                            pts = np.array([
                                [cx, cy], 
                                [cx, cy + int(radius * 1.5)], 
                                [cx + int(radius * 1.2), cy + int(radius * 1.2)]
                            ], np.int32)
                            pts = pts.reshape((-1, 1, 2))
                            cv2.fillPoly(frame_bgr, [pts], color)
                    
                    should_save = False
                    
                    # Check Triggers
                    if self.capture_on_keystroke and self.key_pressed:
                        should_save = True
                        self.key_pressed = False 
                        
                    if self.mouse_triggered:
                        should_save = True
                        self.mouse_triggered = False
                    
                    if not should_save:
                        if prev_frame is None:
                            should_save = True
                        else:
                            # Calculate difference
                            diff = cv2.absdiff(prev_frame, frame_bgr)
                            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                            
                            # Tile Logic:
                            # Grid size is simply div x div
                            grid_w = self.tile_divisions
                            grid_h = self.tile_divisions
                            
                            # Resize diff to grid size using AREA interpolation (averages pixels in the block)
                            # Note: resizing uint8 to small grid averages values. Small changes (< 1.0 avg) become 0.
                            # For high sensitivity, this averaging hides details.
                            
                            # Special handling for Max Sensitivity (100) or Single Tile
                            if self.sensitivity == 100:
                                # Captures single pixel changes regardless of tile size
                                if cv2.countNonZero(gray_diff) > 0:
                                    should_save = True
                            else:
                                if self.tile_divisions == 1:
                                    # Use precise mean for full screen
                                    score = cv2.mean(gray_diff)[0]
                                else:
                                    # Use grid approach
                                    tiled_diff = cv2.resize(gray_diff, (grid_w, grid_h), interpolation=cv2.INTER_AREA)
                                    score = np.max(tiled_diff)
                                
                                threshold = self._get_threshold()
                                if score > threshold:
                                    should_save = True
                            
                    if should_save:
                        # Save frame
                        filename = os.path.join(self.current_session_dir, f"frame_{self.frame_count:05d}.jpg")
                        # Use Pillow for saving or cv2.imwrite
                        # cv2.imwrite is faster usually
                        cv2.imwrite(filename, frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, self.quality])
                        self.frame_count += 1
                        prev_frame = frame_bgr
                except Exception as e:
                    print(f"Error capturing frame: {e}")

                # Sleep to maintain FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                time.sleep(sleep_time)

