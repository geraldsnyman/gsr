#!/usr/bin/env python3
import os
import sys

def create_desktop_entry():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    icon_path = os.path.join(base_dir, "assets", "icon.png")
    run_script = os.path.join(script_dir, "run.sh")
    
    desktop_file_content = f"""[Desktop Entry]
Name=Gerald's Screen Recorder
Comment=A simple screen recorder application
Exec={run_script}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Utility;Recorder;
StartupWMClass=GSR
"""

    desktop_path = os.path.expanduser("~/.local/share/applications/gsr.desktop")
    
    try:
        os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
        with open(desktop_path, "w") as f:
            f.write(desktop_file_content)
        
        # Make executable just in case
        os.chmod(desktop_path, 0o755)
        print(f"Created desktop entry at: {desktop_path}")
        # Update desktop database
        os.system("update-desktop-database ~/.local/share/applications")
    except Exception as e:
        print(f"Failed to create desktop entry: {e}")

if __name__ == "__main__":
    create_desktop_entry()
