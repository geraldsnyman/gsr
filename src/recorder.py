import os
import time
import threading
import datetime
import cv2
import mss
import numpy as np
import json
from PIL import Image
from pynput import keyboard

class ScreenRecorder:
    def __init__(self, output_dir="recordings"):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(self.base_dir, output_dir)
        self.config_file = os.path.join(self.base_dir, "config.json")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.running = False
        self.recording_thread = None
        self.listener = None
        
        # Default settings
        self.fps = 10
        self.sensitivity = 50 
        self.quality = 100 
        self.tile_divisions = 1 
        self.capture_on_keystroke = False
        self.key_pressed = False
        
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
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_settings(self):
        data = {
            "fps": self.fps,
            "sensitivity": self.sensitivity,
            "quality": self.quality,
            "tile_divisions": self.tile_divisions,
            "capture_on_keystroke": self.capture_on_keystroke,
            "output_dir": self.output_dir
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

    def _start_keyboard_listener(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

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
                    
                    # Handle Transparency / Garbage Colors
                    # MSS returns BGRA. Some Linux compositors leave "magic purple" (255,0,255) 
                    # in the RGB channels of fully, transparent pixels (Alpha=0).
                    # Simple conversion to BGR reveals this purple bar.
                    # Fix: Mask out pixels where Alpha is 0 (or low).
                    
                    if frame.shape[2] == 4:
                        # Split channels
                        b, g, r, a = cv2.split(frame)
                        
                        # Create a mask where alpha is valid (e.g. > 0)
                        # We can simply multiply B,G,R by the normalized Alpha, 
                        # OR just set BGR to 0 where Alpha is 0.
                        # Setting to 0 (Black) is faster and safer for "recording".
                        
                        # Fast operation: use numpy boolean indexing or bitwise
                        # But simplest openCV way:
                        frame_bgr = cv2.merge((b, g, r))
                        # Black out transparent pixels
                        frame_bgr[a == 0] = 0
                    else:
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    
                    should_save = False
                    
                    # Check Keystroke Trigger
                    if self.capture_on_keystroke and self.key_pressed:
                        should_save = True
                        self.key_pressed = False # Reset trigger

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

