
import signal
import sys
import os
import urllib.request
import time
import argparse
from recorder import ScreenRecorder

# GUI imports inside main check to allow faster CLI startup or optional deps
# content of ui.py will be imported only if needed

try:
    from importlib.metadata import version
    __version__ = version("gsr")
except Exception:
    __version__ = "1.0.3"

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

def setup_desktop_entry():
    icon_url = "https://raw.githubusercontent.com/geraldsnyman/gsr/master/assets/icon.png"
    icon_path = os.path.expanduser("~/.local/share/icons/gsr-icon.png")
    desktop_path = os.path.expanduser("~/.local/share/applications/gsr.desktop")
    
    desktop_file_content = f"""[Desktop Entry]
Name=Gerald's Screen Recorder
Comment=A simple screen recorder application
Exec={os.path.abspath(sys.argv[0])}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Utility;Recorder;
StartupWMClass=GSR
"""
    try:
        os.makedirs(os.path.dirname(icon_path), exist_ok=True)
        print("Downloading latest icon from GitHub...")
        urllib.request.urlretrieve(icon_url, icon_path)
        
        os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
        with open(desktop_path, "w") as f:
            f.write(desktop_file_content)
        
        os.chmod(desktop_path, 0o755)
        print(f"Created desktop entry at: {desktop_path}")
        os.system("update-desktop-database ~/.local/share/applications")
        print("Desktop setup complete!")
    except Exception as e:
        print(f"Failed to create desktop entry: {e}")

def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(prog="gsr", description="Gerald's Screen Recorder (GSR)")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    
    # Core Operations
    parser.add_argument("--setup-desktop", action="store_true", help="Install Linux desktop entry and icon")
    parser.add_argument("--save", action="store_true", help="Save the provided CLI arguments to permanent GUI settings")
    
    # Capture Overrides
    parser.add_argument("-f", "--fps", type=int, help="Override FPS (1-60)")
    parser.add_argument("-s", "--sens", type=int, help="Override Sensitivity (0-100)")
    parser.add_argument("-t", "--tiles", type=int, help="Override Tile Divisions (1 = Full Screen)")
    parser.add_argument("-q", "--quality", type=int, help="Override JPEG Output Quality (1-100)")
    parser.add_argument("-o", "--output", type=str, help="Override Output Directory")
    
    # Boolean Triggers (Automatically supports --feature and --no-feature)
    parser.add_argument("--keystroke", action=argparse.BooleanOptionalAction, help="Capture on Keystroke")
    parser.add_argument("--mouse-click", action=argparse.BooleanOptionalAction, help="Capture on Mouse Click")
    parser.add_argument("--mouse-scroll", action=argparse.BooleanOptionalAction, help="Capture on Mouse Scroll")
    parser.add_argument("--mouse-move", action=argparse.BooleanOptionalAction, help="Capture on Mouse Move")
    
    # Cursor Settings
    parser.add_argument("--show-cursor", action=argparse.BooleanOptionalAction, help="Draw Cursor Overlay")
    parser.add_argument("--cursor-size", type=int, help="Override Cursor Size (5-50)")
    parser.add_argument("--cursor-style", type=str, choices=["dot", "target", "pointer"], help="Override Cursor Style")
    
    args = parser.parse_args()

    if args.setup_desktop:
        setup_desktop_entry()
        sys.exit(0)

    # Automatically run in CLI mode if any arguments are passed
    if len(sys.argv) > 1:
        print("Starting in CLI Mode...")
        global recorder_instance
        recorder_instance = ScreenRecorder()
        
        # Apply numerical/string overrides (only if explicitly passed)
        if args.fps is not None: recorder_instance.set_fps(args.fps)
        if args.sens is not None: recorder_instance.set_sensitivity(args.sens)
        if args.tiles is not None: recorder_instance.set_tile_divisions(args.tiles)
        if args.quality is not None: recorder_instance.set_quality(args.quality)
        if args.output is not None: recorder_instance.set_output_dir(args.output)
        
        # Apply boolean toggles (True/False allowed via --feature and --no-feature)
        if args.keystroke is not None: recorder_instance.set_capture_on_keystroke(args.keystroke)
        if args.mouse_click is not None: recorder_instance.capture_mouse_click = args.mouse_click
        if args.mouse_move is not None: recorder_instance.capture_mouse_move = args.mouse_move
        if args.mouse_scroll is not None: recorder_instance.capture_mouse_scroll = args.mouse_scroll
        
        # Apply Cursor settings
        if args.show_cursor is not None: recorder_instance.show_cursor = args.show_cursor
        if args.cursor_size is not None: recorder_instance.cursor_size = args.cursor_size
        if args.cursor_style is not None: recorder_instance.cursor_style = args.cursor_style
        
        if args.save:
            print("Saving CLI overrides to permanent settings...")
            recorder_instance.save_settings()
        
        print("\n=== Active Configuration ===")
        print(f"Capture  : FPS={recorder_instance.fps}, Sensitivity={recorder_instance.sensitivity}, Tiles={recorder_instance.tile_divisions}, Quality={recorder_instance.quality}")
        print(f"Triggers : Keys={recorder_instance.capture_on_keystroke}, Click={recorder_instance.capture_mouse_click}, Scroll={recorder_instance.capture_mouse_scroll}, Move={recorder_instance.capture_mouse_move}")
        print(f"Cursor   : Overlay={recorder_instance.show_cursor}, Style={recorder_instance.cursor_style}, Size={recorder_instance.cursor_size}")
        print(f"Output   : {recorder_instance.output_dir}")
        print("============================\n")
        print("Press Ctrl+C to stop recording (or Ctrl+Z to send to background).")
        
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
        
        global app_instance
        app_instance = ScreenRecorderApp()
        app_instance.mainloop()

if __name__ == "__main__":
    main()
