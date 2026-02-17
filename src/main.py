
import signal
import sys
import time
import argparse
from recorder import ScreenRecorder

# GUI imports inside main check to allow faster CLI startup or optional deps
# content of ui.py will be imported only if needed

recorder_instance = None
app_instance = None

def signal_handler(sig, frame):
    global recorder_instance, app_instance
    print("\nCtrl+C pressed. Exiting...")
    
    if app_instance:
        app_instance.on_closing()
    elif recorder_instance:
        if recorder_instance.running:
            recorder_instance.stop_recording()
    
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Simple Screen Recorder")
    parser.add_argument("--cli", action="store_true", help="Run in Command Line Interface mode (no GUI)")
    parser.add_argument("--fps", type=int, help="Override FPS")
    parser.add_argument("--sens", type=int, help="Override Sensitivity (0-100)")
    parser.add_argument("--tiles", type=int, help="Override Tile Divisions (e.g. 1 for Full Screen)")
    parser.add_argument("--keystroke", action="store_true", help="Enable Capture on Keystroke")
    parser.add_argument("--mouse-click", action="store_true", help="Capture on Mouse Click")
    parser.add_argument("--mouse-move", action="store_true", help="Capture on Mouse Move")
    parser.add_argument("--mouse-scroll", action="store_true", help="Capture on Mouse Scroll")
    parser.add_argument("--show-cursor", action="store_true", help="Draw Cursor Overlay")
    
    args = parser.parse_args()

    if args.cli:
        print("Starting in CLI Mode...")
        recorder_instance = ScreenRecorder()
        
        # Apply overrides
        if args.fps: recorder_instance.fps = args.fps
        if args.sens: recorder_instance.sensitivity = args.sens
        if args.tiles: recorder_instance.set_tile_divisions(args.tiles)
        if args.keystroke: recorder_instance.set_capture_on_keystroke(True)
        if args.mouse_click: recorder_instance.capture_mouse_click = True
        if args.mouse_move: recorder_instance.capture_mouse_move = True
        if args.mouse_scroll: recorder_instance.capture_mouse_scroll = True
        if args.show_cursor: recorder_instance.show_cursor = True
        
        print(f"Settings: FPS={recorder_instance.fps}, Sensitivity={recorder_instance.sensitivity}, TileDivs={recorder_instance.tile_divisions}")
        print(f"Triggers: Keys={recorder_instance.capture_on_keystroke}, Click={recorder_instance.capture_mouse_click}, Move={recorder_instance.capture_mouse_move}, Scroll={recorder_instance.capture_mouse_scroll}")
        print("Press Ctrl+C to stop recording.")
        
        recorder_instance.start_recording()
        
        # Keep main thread alive to receive signals
        while True:
            time.sleep(1)
    else:
        # GUI Mode
        import customtkinter as ctk
        from ui import ScreenRecorderApp
        
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue") 
        
        app_instance = ScreenRecorderApp()
        app_instance.mainloop()
