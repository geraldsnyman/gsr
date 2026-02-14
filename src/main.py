
import signal
import sys
import customtkinter as ctk
from ui import ScreenRecorderApp

app = None

def signal_handler(sig, frame):
    global app
    print("\nCtrl+C pressed. Exiting...")
    if app:
        app.on_closing()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue") 
    
    app = ScreenRecorderApp()
    app.mainloop()
