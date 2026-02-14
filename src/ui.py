
import tkinter as tk
import customtkinter as ctk
import os
import threading
from recorder import ScreenRecorder

import tkinter.filedialog as filedialog

class ScreenRecorderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simple Screen Recorder")
        self.geometry("500x450")
        self.resizable(False, False)

        # Initialize recorder
        self.recorder = ScreenRecorder()
        self.is_recording = False

        # GUI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Settings expand? No, usually not.
        
        # Title
        self.label_title = ctk.CTkLabel(self, text="Simple Screen Recorder", font=("Roboto", 24, "bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        self.label_status = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray")
        self.label_status.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Settings Frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        # Sensitivity Slider
        self.label_sens = ctk.CTkLabel(self.settings_frame, text="Sensitivity (50):", width=120, anchor="w")
        self.label_sens.grid(row=0, column=0, padx=10, pady=10)
        
        self.slider_sens = ctk.CTkSlider(self.settings_frame, from_=0, to=100, command=self.update_sensitivity_lbl)
        self.slider_sens.set(50) 
        self.slider_sens.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # FPS Slider
        self.label_fps = ctk.CTkLabel(self.settings_frame, text="FPS (10):", width=120, anchor="w")
        self.label_fps.grid(row=1, column=0, padx=10, pady=10)
        
        self.slider_fps = ctk.CTkSlider(self.settings_frame, from_=1, to=60, number_of_steps=59, command=self.update_fps_lbl)
        self.slider_fps.set(10)
        self.slider_fps.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Quality Slider
        self.label_qual = ctk.CTkLabel(self.settings_frame, text="Quality (100%):", width=120, anchor="w")
        self.label_qual.grid(row=2, column=0, padx=10, pady=10)
        
        self.slider_qual = ctk.CTkSlider(self.settings_frame, from_=1, to=100, number_of_steps=99, command=self.update_qual_lbl)
        self.slider_qual.set(100)
        self.slider_qual.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Output Directory
        self.label_dir_title = ctk.CTkLabel(self.settings_frame, text="Output:", width=120, anchor="w")
        self.label_dir_title.grid(row=3, column=0, padx=10, pady=(10,0), sticky="nw")

        self.dir_var = tk.StringVar(value=os.path.abspath(self.recorder.output_dir))
        self.label_dir_path = ctk.CTkLabel(self.settings_frame, textvariable=self.dir_var, text_color="gray", wraplength=250, justify="left")
        self.label_dir_path.grid(row=3, column=1, padx=10, pady=(10,0), sticky="w")
        
        self.btn_dir = ctk.CTkButton(self.settings_frame, text="Browse...", width=100, command=self.select_directory)
        self.btn_dir.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # Controls
        self.btn_record = ctk.CTkButton(self, text="START RECORDING", command=self.toggle_recording, fg_color="#2CC985", hover_color="#229966", height=40, font=("Roboto", 14, "bold"))
        self.btn_record.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

    def select_directory(self):
        directory = filedialog.askdirectory(initialdir=self.recorder.output_dir)
        if directory:
            self.recorder.set_output_dir(directory)
            self.dir_var.set(directory)

    def update_sensitivity_lbl(self, value):
        sens = int(value)
        self.label_sens.configure(text=f"Sensitivity ({sens}):")
        self.recorder.set_sensitivity(sens)

    def update_fps_lbl(self, value):
        fps = int(value)
        self.label_fps.configure(text=f"FPS ({fps}):")
        self.recorder.set_fps(fps)

    def update_qual_lbl(self, value):
        qual = int(value)
        self.label_qual.configure(text=f"Quality ({qual}%):")
        self.recorder.set_quality(qual)

    def toggle_recording(self):
        if not self.is_recording:
            # Start
            self.recorder.start_recording()
            self.is_recording = True
            self.btn_record.configure(text="STOP RECORDING", fg_color="#FF4B4B", hover_color="#CC3333")
            self.status_var.set("Recording in progress...")
            self.label_status.configure(text_color="#FF4B4B")
        else:
            # Stop
            self.recorder.stop_recording()
            self.is_recording = False
            self.btn_record.configure(text="START RECORDING", fg_color="#2CC985", hover_color="#229966")
            
            saved_dir = self.recorder.current_session_dir
            saved_name = os.path.basename(saved_dir) if saved_dir else "output"
            self.status_var.set(f"Saved {self.recorder.frame_count} frames to {saved_name}")
            self.label_status.configure(text_color="gray")

if __name__ == "__main__":
    app = ScreenRecorderApp()
    app.mainloop()
