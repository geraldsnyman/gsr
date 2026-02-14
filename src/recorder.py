
import os
import time
import threading
import datetime
import cv2
import mss
import numpy as np
from PIL import Image

class ScreenRecorder:
    def __init__(self, output_dir="recordings"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.running = False
        self.recording_thread = None
        
        # Default settings
        self.fps = 10
        self.sensitivity = 50 # 0-100, where 0 is very sensitive (captures small changes), 100 is least sensitive
        self.quality = 100 # JPEG Quality (0-100)
        
        self.current_session_dir = None
        self.frame_count = 0
        # self.sct will be initialized in the thread to avoid X11 threading issues
        self.monitor_index = 1 

    def start_recording(self):
        if self.running:
            return
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_session_dir = os.path.join(self.output_dir, f"session_{timestamp}")
        os.makedirs(self.current_session_dir, exist_ok=True)
        
        self.running = True
        self.frame_count = 0
        self.recording_thread = threading.Thread(target=self._record_loop)
        self.recording_thread.start()
        print(f"Recording started. Saving to {self.current_session_dir}")

    def stop_recording(self):
        self.running = False
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
                    # Convert to BGR for OpenCV processing (mss returns BGRA)
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    
                    should_save = False
                    
                    if prev_frame is None:
                        should_save = True
                    else:
                        # Calculate difference
                        valid_region = frame_bgr  # Could optimize by resizing for diff check
                        diff = cv2.absdiff(prev_frame, valid_region)
                        # Convert diff to grayscale to check intensity
                        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                        score = np.mean(gray_diff)
                        
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

