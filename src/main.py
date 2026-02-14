
import os
import sys

# Ensure src defines the project root context if needed, but running this file directly adds its dir to path.
# However, for clarity:
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import customtkinter as ctk
from ui import ScreenRecorderApp

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    app = ScreenRecorderApp()
    app.mainloop()
