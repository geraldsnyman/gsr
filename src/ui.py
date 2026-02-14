import sys
import tkinter as tk
import customtkinter as ctk
import os
from tkinter import filedialog
from recorder import ScreenRecorder

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ScreenRecorderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simple Screen Recorder")
        self.geometry("500x600")
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Main content area expands

        # Initialize recorder
        self.recorder = ScreenRecorder()
        self.is_recording = False
        
        # Get Screen Res
        self.screen_w, self.screen_h = self.recorder.get_screen_resolution()
        
        # Calculate doubling divisors
        max_div = max(1, self.screen_w // 16) # Minimal tile width 16
        
        self.divisors = []
        import math
        def get_factors(n):
            f = set()
            for i in range(1, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    f.add(i)
                    f.add(n // i)
            return f

        w_factors = get_factors(self.screen_w)
        h_factors = get_factors(self.screen_h)
        common = sorted(list(w_factors.intersection(h_factors)))
        
        min_tile_width = 16
        self.divisors = [n for n in common if (self.screen_w // n) >= min_tile_width]
        self.divisors.sort()
        
        num_steps = max(1, len(self.divisors) - 1)

        # Title
        self.label_title = ctk.CTkLabel(self, text="Simple Screen Recorder", font=("Roboto", 24, "bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        self.label_status = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray")
        self.label_status.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Scrollable Settings Frame
        self.settings_frame = ctk.CTkScrollableFrame(self, label_text="Settings")
        self.settings_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        # 1. Screen Resolution
        self.label_res = ctk.CTkLabel(self.settings_frame, text=f"Screen: {self.screen_w}x{self.screen_h}", text_color="gray")
        self.label_res.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        # 2. Sensitivity Slider
        self.label_sens = ctk.CTkLabel(self.settings_frame, text="Sensitivity (60):", width=140, anchor="w")
        self.label_sens.grid(row=1, column=0, padx=10, pady=10)
        
        self.slider_sens = ctk.CTkSlider(self.settings_frame, from_=0, to=100, command=self.update_sensitivity_lbl)
        self.slider_sens.set(60) 
        self.slider_sens.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # 3. Tile Size Slider
        self.label_tile = ctk.CTkLabel(self.settings_frame, text=f"Tile Size ({self.screen_w}x{self.screen_h}):", width=140, anchor="w")
        self.label_tile.grid(row=2, column=0, padx=10, pady=10)
        
        self.slider_tile = ctk.CTkSlider(self.settings_frame, from_=0, to=num_steps, number_of_steps=num_steps, command=self.update_tile_lbl)
        self.slider_tile.set(num_steps) 
        self.slider_tile.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # 4. Key Capture Checkbox
        self.check_key = ctk.CTkCheckBox(self.settings_frame, text="Capture on Keystroke", command=self.toggle_key_capture)
        self.check_key.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # 5. FPS Slider
        self.label_fps = ctk.CTkLabel(self.settings_frame, text="FPS (20):", width=140, anchor="w")
        self.label_fps.grid(row=4, column=0, padx=10, pady=10)
        
        self.slider_fps = ctk.CTkSlider(self.settings_frame, from_=1, to=60, number_of_steps=59, command=self.update_fps_lbl)
        self.slider_fps.set(20)
        self.slider_fps.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # 6. Quality Slider
        self.label_qual = ctk.CTkLabel(self.settings_frame, text="Quality (100%):", width=140, anchor="w")
        self.label_qual.grid(row=5, column=0, padx=10, pady=10)
        
        self.slider_qual = ctk.CTkSlider(self.settings_frame, from_=1, to=100, number_of_steps=99, command=self.update_qual_lbl)
        self.slider_qual.set(100)
        self.slider_qual.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # 7. Output Directory
        self.label_dir_title = ctk.CTkLabel(self.settings_frame, text="Output Folder:", width=140, anchor="w")
        self.label_dir_title.grid(row=6, column=0, padx=10, pady=(15,0), sticky="nw")

        self.dir_var = tk.StringVar(value=os.path.abspath(self.recorder.output_dir))
        self.label_dir_path = ctk.CTkLabel(self.settings_frame, textvariable=self.dir_var, text_color="gray", wraplength=250, justify="left")
        self.label_dir_path.grid(row=6, column=1, padx=10, pady=(15,0), sticky="w")
        
        self.btn_dir = ctk.CTkButton(self.settings_frame, text="Browse...", width=100, command=self.select_directory)
        self.btn_dir.grid(row=7, column=1, padx=10, pady=10, sticky="e")

        # Controls (Outside Scroll Frame)
        self.btn_record = ctk.CTkButton(self, text="START RECORDING", command=self.toggle_recording, fg_color="#2CC985", hover_color="#229966", height=50, font=("Roboto", 16, "bold"))
        self.btn_record.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        # Handle Protocol for X button
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        if self.is_recording:
            self.stop_recording()
        self.quit()

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recorder.start_recording()
        self.is_recording = True
        self.btn_record.configure(text="STOP RECORDING", fg_color="#C92C2C", hover_color="#992222")
        self.status_var.set("Recording...")

    def stop_recording(self):
        self.recorder.stop_recording()
        self.is_recording = False
        self.btn_record.configure(text="START RECORDING", fg_color="#2CC985", hover_color="#229966")
        self.status_var.set("Ready")
        saved_dir = self.recorder.current_session_dir
        saved_name = os.path.basename(saved_dir) if saved_dir else "output"
        self.status_var.set(f"Saved {self.recorder.frame_count} frames to {saved_name}")
        self.label_status.configure(text_color="gray")

    def select_directory(self):
        directory = filedialog.askdirectory(initialdir=self.recorder.output_dir)
        if directory:
            self.recorder.set_output_dir(directory)
            self.dir_var.set(directory)

    def toggle_key_capture(self):
        enabled = bool(self.check_key.get())
        self.recorder.set_capture_on_keystroke(enabled)

    def update_sensitivity_lbl(self, value):
        sens = int(value)
        self.label_sens.configure(text=f"Sensitivity ({sens}):")
        self.recorder.set_sensitivity(sens)

    def update_tile_lbl(self, value):
        index = int(value + 0.5) # Round to nearest step
        if index < 0: index = 0
        if index >= len(self.divisors): index = len(self.divisors) - 1
        
        divs = self.divisors[index]
        self.recorder.set_tile_divisions(divs)
        tw, th = self.recorder.get_tile_resolution()
        self.label_tile.configure(text=f"Tile Size ({tw}x{th}):")

    def update_fps_lbl(self, value):
        fps = int(value)
        self.label_fps.configure(text=f"FPS ({fps}):")
        self.recorder.set_fps(fps)

    def update_qual_lbl(self, value):
        qual = int(value)
        self.label_qual.configure(text=f"Quality ({qual}%):")
        self.recorder.set_quality(qual)

if __name__ == "__main__":
    app = ScreenRecorderApp()
    app.mainloop()
