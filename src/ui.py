import sys
import tkinter as tk
import customtkinter as ctk
import os
from tkinter import filedialog
from recorder import ScreenRecorder

try:
    from importlib.metadata import version
    __version__ = version("gsr")
except Exception:
    __version__ = "1.0.3"

# ── Color Palette ──────────────────────────────────────────────
BG_DARK       = "#1a1a2e"     # Main background
CARD_BG       = "#16213e"     # Card/section background
CARD_BORDER   = "#0f3460"     # Subtle card border
TEXT_PRIMARY  = "#e0e0e0"     # Primary text
TEXT_SECONDARY= "#8892a0"     # Secondary/muted text
ACCENT_GREEN  = "#2CC985"     # Start / active accent
ACCENT_GREEN_H= "#229966"     # Green hover
ACCENT_RED    = "#C92C2C"     # Stop / recording accent
ACCENT_RED_H  = "#992222"     # Red hover
SLIDER_FG     = "#2CC985"     # Slider filled portion
SLIDER_BG     = "#2a2a4a"     # Slider track bg
SLIDER_BTN    = "#e0e0e0"     # Slider button color

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ScreenRecorderApp(ctk.CTk):
    def __init__(self):
        super().__init__(className="GSR")
        self.title(f"Gerald's Screen Recorder (v{__version__})")
        self.geometry("550x580")
        self.minsize(450, 580)
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)

        # Set Icon
        try:
            from PIL import Image, ImageTk
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, "assets", "icon.png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                self.icon_photo = ImageTk.PhotoImage(img)
                self.wm_iconphoto(True, self.icon_photo)
                self.call('wm', 'iconphoto', self._w, self.icon_photo)
        except Exception as e:
            print(f"Could not load icon: {e}")

        # ── Initialize Recorder ────────────────────────────────
        self.recorder = ScreenRecorder()
        self.is_recording = False
        self.screen_w, self.screen_h = self.recorder.get_screen_resolution()

        # Tile divisors calculation
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
        self.divisors = sorted([n for n in common if (self.screen_w // n) >= min_tile_width])
        target_width = 960
        best_div = min(self.divisors, key=lambda x: abs((self.screen_w // x) - target_width))
        default_index = self.divisors.index(best_div)
        num_steps = max(1, len(self.divisors) - 1)

        # ── Layout: outer frame uses pack for simplicity ───────
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # ── Header ─────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=24, pady=(18, 6), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        self.label_title = ctk.CTkLabel(
            header, text=f"GSR v{__version__}",
            font=("Roboto", 28, "bold"), text_color=TEXT_PRIMARY, anchor="w"
        )
        self.label_title.grid(row=0, column=0, sticky="w")

        self.status_var = tk.StringVar(value="Ready")
        self.label_status = ctk.CTkLabel(
            header, textvariable=self.status_var,
            font=("Roboto", 13), text_color=TEXT_SECONDARY, anchor="w"
        )
        self.label_status.grid(row=0, column=1, padx=(12, 0), sticky="w")

        # Resolution display with label and hover tooltip
        res_frame = ctk.CTkFrame(header, fg_color=CARD_BG, corner_radius=6)
        res_frame.grid(row=0, column=2, sticky="e")

        res_icon = ctk.CTkLabel(
            res_frame, text="🖥", font=("Roboto", 12), width=20,
            text_color=TEXT_SECONDARY, anchor="e"
        )
        res_icon.grid(row=0, column=0, padx=(8, 2), pady=4)

        res_label = ctk.CTkLabel(
            res_frame, text=f"{self.screen_w} × {self.screen_h}",
            font=("Roboto", 11, "bold"), text_color=TEXT_SECONDARY, anchor="e"
        )
        res_label.grid(row=0, column=1, padx=(0, 8), pady=4)

        # Tooltip for resolution
        self._res_tooltip = None
        def show_res_tooltip(event):
            if self._res_tooltip:
                return
            x = res_frame.winfo_rootx()
            y = res_frame.winfo_rooty() + res_frame.winfo_height() + 4
            self._res_tooltip = tk.Toplevel(self)
            self._res_tooltip.wm_overrideredirect(True)
            self._res_tooltip.wm_geometry(f"+{x}+{y}")
            tip_label = tk.Label(
                self._res_tooltip,
                text="Primary screen capture resolution.\nThis is the full area being recorded.",
                bg="#2a2a4a", fg="#e0e0e0", font=("Roboto", 10),
                padx=10, pady=6, justify="left", relief="solid", bd=1
            )
            tip_label.pack()
        def hide_res_tooltip(event):
            if self._res_tooltip:
                self._res_tooltip.destroy()
                self._res_tooltip = None
        res_frame.bind("<Enter>", show_res_tooltip)
        res_frame.bind("<Leave>", hide_res_tooltip)
        res_icon.bind("<Enter>", show_res_tooltip)
        res_icon.bind("<Leave>", hide_res_tooltip)
        res_label.bind("<Enter>", show_res_tooltip)
        res_label.bind("<Leave>", hide_res_tooltip)

        # ── Main Content Area (Fixed layout) ───────────────────
        self._inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._inner_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self._inner_frame.grid_columnconfigure(0, weight=3)   # Capture gets more space
        self._inner_frame.grid_columnconfigure(1, weight=1)   # Triggers column
        content_row = 0

        # ─── Row 0: Capture (left) + Triggers (right) ──────────
        capture_card = self._make_card(self._inner_frame, "Capture", cols=3)
        capture_card.grid(row=content_row, column=0, padx=(20, 6), pady=(8, 4), sticky="nsew")

        triggers_card = self._make_card(self._inner_frame, "Triggers")
        triggers_card.grid(row=content_row, column=1, padx=(6, 20), pady=(8, 4), sticky="nsew")
        # Triggers only needs 1 column for switches
        triggers_card.grid_columnconfigure(0, weight=1)
        triggers_card.grid_columnconfigure(1, weight=0)
        content_row += 1

        # ── Populate Capture Card ──────────────────────────────
        # Sensitivity
        self.label_sens, self.slider_sens, self.val_sens = self._make_slider(
            capture_card, "Sensitivity", self.recorder.sensitivity,
            0, 100, self.update_sensitivity_lbl, r=0
        )

        # Tile Size
        current_index = 0
        if self.recorder.tile_divisions in self.divisors:
            current_index = self.divisors.index(self.recorder.tile_divisions)
        else:
            current_index = default_index
            self.recorder.set_tile_divisions(self.divisors[current_index])

        init_tw, init_th = self.recorder.get_tile_resolution()
        self.label_tile, self.slider_tile, self.val_tile = self._make_slider(
            capture_card, "Tile Size", current_index,
            0, num_steps, self.update_tile_lbl, r=1, steps=num_steps
        )
        self.val_tile.configure(text=f"{init_tw}×{init_th}")

        # FPS
        self.label_fps, self.slider_fps, self.val_fps = self._make_slider(
            capture_card, "FPS", self.recorder.fps,
            1, 60, self.update_fps_lbl, r=2, steps=59
        )

        # Quality
        self.label_qual, self.slider_qual, self.val_qual = self._make_slider(
            capture_card, "Quality", self.recorder.quality,
            1, 100, self.update_qual_lbl, r=3, steps=99
        )

        # ── Populate Triggers Card (single column of switches) ─
        self.check_key = self._make_switch(triggers_card, "Keystroke", self.recorder.capture_on_keystroke, self.toggle_key_capture, r=0)
        self.check_click = self._make_switch(triggers_card, "Click", self.recorder.capture_mouse_click, self.toggle_mouse_click, r=1)
        self.check_scroll = self._make_switch(triggers_card, "Scroll", self.recorder.capture_mouse_scroll, self.toggle_mouse_scroll, r=2)
        self.check_move = self._make_switch(triggers_card, "Move", self.recorder.capture_mouse_move, self.toggle_mouse_move, r=3)

        # ─── Card: Cursor (compact, spans both columns) ────────
        cursor_card = ctk.CTkFrame(
            self._inner_frame, fg_color=CARD_BG, corner_radius=10,
            border_width=1, border_color=CARD_BORDER
        )
        cursor_card.grid(row=content_row, column=0, columnspan=2, padx=20, pady=4, sticky="ew")
        cursor_card.grid_columnconfigure(0, weight=0)  # "Size" label
        cursor_card.grid_columnconfigure(1, weight=1)  # slider (stretches)
        cursor_card.grid_columnconfigure(2, weight=0)  # value
        cursor_card.grid_columnconfigure(3, weight=0)  # spacer
        cursor_card.grid_columnconfigure(4, weight=0)  # icon buttons
        content_row += 1

        # Card title
        cursor_title = ctk.CTkLabel(
            cursor_card, text="Cursor", font=("Roboto", 14, "bold"),
            text_color=TEXT_PRIMARY, anchor="w"
        )
        cursor_title.grid(row=0, column=0, columnspan=5, padx=12, pady=(10, 2), sticky="w")

        # Size label
        size_label = ctk.CTkLabel(
            cursor_card, text="Size", font=("Roboto", 13),
            text_color=TEXT_SECONDARY, anchor="w"
        )
        size_label.grid(row=1, column=0, padx=(12, 6), pady=(4, 10), sticky="w")

        # Size slider
        self.slider_csize = ctk.CTkSlider(
            cursor_card, from_=5, to=50, number_of_steps=45,
            command=self.update_csize_lbl,
            fg_color=SLIDER_BG, progress_color=ACCENT_GREEN,
            button_color=SLIDER_BTN, button_hover_color="#ffffff",
            height=16, corner_radius=8
        )
        self.slider_csize.set(self.recorder.cursor_size)
        self.slider_csize.grid(row=1, column=1, padx=4, pady=(4, 10), sticky="ew")
        self._setup_slider_keys(self.slider_csize, self.update_csize_lbl, step=1)

        # Size value
        self.val_csize = ctk.CTkLabel(
            cursor_card, text=str(self.recorder.cursor_size),
            font=("Roboto", 13, "bold"), text_color=TEXT_PRIMARY,
            anchor="e", width=30
        )
        self.val_csize.grid(row=1, column=2, padx=(4, 0), pady=(4, 10), sticky="e")

        # Spacer between value and icons
        spacer = ctk.CTkLabel(cursor_card, text="", width=16)
        spacer.grid(row=1, column=3, padx=0, pady=0)

        # Style icons: none, dot, target, pointer
        # 🚫 = none/off, ● = dot, ◎ = target, ▲ = pointer (bold)
        self._cursor_icon_map = {
            "🚫": "none",
            "●": "dot",
            "◎": "target",
            "▲": "pointer",
        }
        self._cursor_style_to_icon = {v: k for k, v in self._cursor_icon_map.items()}

        # Determine initial selection
        if self.recorder.show_cursor:
            initial_icon = self._cursor_style_to_icon.get(self.recorder.cursor_style, "●")
        else:
            initial_icon = "🚫"

        # Wrap segmented button in a frame for tooltip binding
        # (CTkSegmentedButton does not support .bind())
        style_wrapper = ctk.CTkFrame(cursor_card, fg_color="transparent")
        style_wrapper.grid(row=1, column=4, padx=(0, 12), pady=(4, 10), sticky="e")

        self.seg_cstyle = ctk.CTkSegmentedButton(
            style_wrapper, values=["🚫", "●", "◎", "▲"],
            command=self.update_cstyle,
            font=("Roboto", 14), width=180,
            selected_color=ACCENT_GREEN,
            selected_hover_color=ACCENT_GREEN_H,
            unselected_color=CARD_BG,
            unselected_hover_color=SLIDER_BG,
            border_width=1,
        )
        self.seg_cstyle.set(initial_icon)
        self.seg_cstyle.pack(padx=2, pady=2)

        # Tooltip for cursor style icons
        self._cursor_tooltip = None
        def show_cursor_tooltip(event):
            if self._cursor_tooltip:
                return
            x = style_wrapper.winfo_rootx()
            y = style_wrapper.winfo_rooty() + style_wrapper.winfo_height() + 4
            self._cursor_tooltip = tk.Toplevel(self)
            self._cursor_tooltip.wm_overrideredirect(True)
            self._cursor_tooltip.wm_geometry(f"+{x}+{y}")
            tip_label = tk.Label(
                self._cursor_tooltip,
                text="🚫 None  ● Dot  ◎ Target  ▲ Pointer",
                bg="#2a2a4a", fg="#e0e0e0", font=("Roboto", 10),
                padx=10, pady=6, justify="left", relief="solid", bd=1
            )
            tip_label.pack()
        def hide_cursor_tooltip(event):
            try:
                x, y = style_wrapper.winfo_pointerxy()
                x1 = style_wrapper.winfo_rootx()
                y1 = style_wrapper.winfo_rooty()
                x2 = x1 + style_wrapper.winfo_width()
                y2 = y1 + style_wrapper.winfo_height()
                # If pointer is still within the bounds of the wrapper, do not hide (e.g. over a child widget)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return
            except Exception:
                pass
            if self._cursor_tooltip:
                self._cursor_tooltip.destroy()
                self._cursor_tooltip = None
        def bind_tooltip_events(widget):
            try:
                widget.bind("<Enter>", show_cursor_tooltip, add="+")
                widget.bind("<Leave>", hide_cursor_tooltip, add="+")
            except Exception:
                pass
            for child in widget.winfo_children():
                bind_tooltip_events(child)
                
        # Wait slightly for CTkSegmentedButton child canvases to be built before binding
        self.after(50, lambda: bind_tooltip_events(style_wrapper))

        # ─── Card: Output (spans both columns) ─────────────────
        output_card = self._make_card(self._inner_frame, "Output")
        output_card.grid(row=content_row, column=0, columnspan=2, padx=20, pady=(4, 8), sticky="ew")
        content_row += 1

        out_offset = getattr(output_card, '_content_row_offset', 0)
        self.dir_var = tk.StringVar(value=os.path.abspath(self.recorder.output_dir))
        dir_path_label = ctk.CTkLabel(
            output_card, textvariable=self.dir_var, text_color=TEXT_SECONDARY,
            font=("Roboto", 11), wraplength=380, justify="left", anchor="w"
        )
        dir_path_label.grid(row=0 + out_offset, column=0, padx=12, pady=(8, 16), sticky="ew")

        self.btn_dir = ctk.CTkButton(
            output_card, text="Browse…", width=90, height=28,
            command=self.select_directory,
            fg_color=CARD_BORDER, hover_color=SLIDER_BG,
            font=("Roboto", 12), corner_radius=6
        )
        self.btn_dir.grid(row=0 + out_offset, column=1, padx=12, pady=(8, 16), sticky="e")

        # ── Record Button (fixed at bottom) ────────────────────
        self.btn_record = ctk.CTkButton(
            self, text="START RECORDING", command=self.toggle_recording,
            fg_color=ACCENT_GREEN, hover_color=ACCENT_GREEN_H,
            height=52, font=("Roboto", 16, "bold"), corner_radius=12,
            text_color="#ffffff"
        )
        self.btn_record.grid(row=2, column=0, padx=24, pady=(8, 20), sticky="ew")

        # Handle Protocol for X button
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ── Card Factory ───────────────────────────────────────────
    def _make_card(self, parent, title, cols=2):
        card = ctk.CTkFrame(
            parent, fg_color=CARD_BG, corner_radius=10,
            border_width=1, border_color=CARD_BORDER
        )
        # For 3-col cards: [label (fixed), slider (stretch), value (fixed)]
        if cols == 3:
            card.grid_columnconfigure(0, weight=0)
            card.grid_columnconfigure(1, weight=1)
            card.grid_columnconfigure(2, weight=0)
        else:
            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=1)

        card._num_cols = cols

        title_label = ctk.CTkLabel(
            card, text=title, font=("Roboto", 14, "bold"),
            text_color=TEXT_PRIMARY, anchor="w"
        )
        title_label.grid(row=0, column=0, columnspan=cols, padx=12, pady=(10, 2), sticky="w")

        card._content_row_offset = 1
        return card

    def _make_slider(self, card, label_text, initial, from_, to_, cmd, r, steps=None):
        offset = getattr(card, '_content_row_offset', 0)
        actual_row = r + offset
        num_cols = getattr(card, '_num_cols', 2)

        # Label (column 0)
        label = ctk.CTkLabel(
            card, text=label_text, font=("Roboto", 13),
            text_color=TEXT_SECONDARY, anchor="w"
        )
        label.grid(row=actual_row, column=0, padx=(12, 6), pady=10, sticky="w")

        slider_kwargs = dict(
            from_=from_, to=to_, command=cmd,
            fg_color=SLIDER_BG, progress_color=ACCENT_GREEN,
            button_color=SLIDER_BTN, button_hover_color="#ffffff",
            height=16, corner_radius=8
        )
        if steps is not None:
            slider_kwargs["number_of_steps"] = steps

        if num_cols == 3:
            # 3-column layout: [label, slider, value]
            slider = ctk.CTkSlider(card, **slider_kwargs)
            slider.set(initial)
            slider.grid(row=actual_row, column=1, padx=4, pady=10, sticky="ew")

            value_label = ctk.CTkLabel(
                card, text=str(int(initial)), font=("Roboto", 13, "bold"),
                text_color=TEXT_PRIMARY, anchor="e", width=60
            )
            value_label.grid(row=actual_row, column=2, padx=(4, 12), pady=10, sticky="e")
            
            # Setup arrow keys
            step_size = (to_ - from_) / steps if steps else 1
            self._setup_slider_keys(slider, cmd, step=step_size)
            
            return label, slider, value_label
        else:
            # 2-column layout: [label, slider] (used by Cursor card etc.)
            label.configure(text=f"{label_text}  ·  {int(initial)}")
            slider = ctk.CTkSlider(card, **slider_kwargs)
            slider.set(initial)
            slider.grid(row=actual_row, column=1, padx=12, pady=10, sticky="ew")

            # Setup arrow keys
            step_size = (to_ - from_) / steps if steps else 1
            self._setup_slider_keys(slider, cmd, step=step_size)

            return label, slider, None

    def _make_switch(self, card, label_text, initial, cmd, r, c=0, colspan=1):
        offset = getattr(card, '_content_row_offset', 0)
        actual_row = r + offset

        # Label on the left
        label = ctk.CTkLabel(
            card, text=label_text, font=("Roboto", 13),
            text_color=TEXT_SECONDARY, anchor="w"
        )
        label.grid(row=actual_row, column=c, padx=(12, 4), pady=10, sticky="w")

        # Toggle on the right (no text)
        switch = ctk.CTkSwitch(
            card, text="", command=cmd, width=46,
            progress_color=ACCENT_GREEN, button_color=SLIDER_BTN,
            button_hover_color="#ffffff", fg_color=SLIDER_BG,
        )
        if initial:
            switch.select()
        # Place switch in next column
        switch_col = c + colspan
        switch.grid(row=actual_row, column=switch_col, padx=(0, 12), pady=10, sticky="e")
        return switch


    def on_closing(self):
        if self.is_recording:
            self.stop_recording()
        self.recorder.save_settings()
        self.quit()

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recorder.start_recording()
        self.is_recording = True
        self.btn_record.configure(text="STOP RECORDING", fg_color=ACCENT_RED, hover_color=ACCENT_RED_H)
        self.status_var.set("Recording…")
        self.label_status.configure(text_color=ACCENT_RED)

    def stop_recording(self):
        self.recorder.stop_recording()
        self.is_recording = False
        self.btn_record.configure(text="START RECORDING", fg_color=ACCENT_GREEN, hover_color=ACCENT_GREEN_H)
        saved_dir = self.recorder.current_session_dir
        saved_name = os.path.basename(saved_dir) if saved_dir else "output"
        self.status_var.set(f"Saved {self.recorder.frame_count} frames → {saved_name}")
        self.label_status.configure(text_color=TEXT_SECONDARY)

    def _setup_slider_keys(self, slider, command, step=1):
        slider.bind("<Button-1>", lambda e: slider.focus_set())
        def on_left(event):
            try:
                val = slider.get() - step
                min_val = getattr(slider, "_from_", 0)
                if val < min_val: val = min_val
                slider.set(val)
                command(val)
            except Exception:
                pass
        def on_right(event):
            try:
                val = slider.get() + step
                max_val = getattr(slider, "_to", 100)
                if hasattr(slider, "_to_"): max_val = slider._to_
                if val > max_val: val = max_val
                slider.set(val)
                command(val)
            except Exception:
                pass
        slider.bind("<Left>", on_left)
        slider.bind("<Right>", on_right)
        if hasattr(slider, "_canvas"):
            slider._canvas.bind("<Button-1>", lambda e: slider.focus_set())
            slider._canvas.bind("<Left>", on_left)
            slider._canvas.bind("<Right>", on_right)

    def select_directory(self):
        directory = filedialog.askdirectory(initialdir=self.recorder.output_dir)
        if directory:
            self.recorder.set_output_dir(directory)
            self.dir_var.set(directory)

    def toggle_key_capture(self):
        enabled = bool(self.check_key.get())
        self.recorder.set_capture_on_keystroke(enabled)
        self.recorder.save_settings()

    def toggle_mouse_click(self):
        self.recorder.capture_mouse_click = bool(self.check_click.get())
        self.recorder.save_settings()

    def toggle_mouse_scroll(self):
        self.recorder.capture_mouse_scroll = bool(self.check_scroll.get())
        self.recorder.save_settings()

    def toggle_mouse_move(self):
        self.recorder.capture_mouse_move = bool(self.check_move.get())
        self.recorder.save_settings()


    def update_sensitivity_lbl(self, value):
        sens = int(value)
        self.val_sens.configure(text=str(sens))
        self.recorder.set_sensitivity(sens)

    def update_tile_lbl(self, value):
        index = int(value + 0.5)
        if index < 0: index = 0
        if index >= len(self.divisors): index = len(self.divisors) - 1
        divs = self.divisors[index]
        self.recorder.set_tile_divisions(divs)
        tw, th = self.recorder.get_tile_resolution()
        self.val_tile.configure(text=f"{tw}×{th}")

    def update_fps_lbl(self, value):
        fps = int(value)
        self.val_fps.configure(text=str(fps))
        self.recorder.set_fps(fps)

    def update_qual_lbl(self, value):
        qual = int(value)
        self.val_qual.configure(text=f"{qual}%")
        self.recorder.set_quality(qual)

    def update_csize_lbl(self, value):
        size = int(value)
        self.val_csize.configure(text=str(size))
        self.recorder.cursor_size = size
        self.recorder.save_settings()

    def update_cstyle(self, icon):
        style = self._cursor_icon_map.get(icon, "dot")
        if style == "none":
            self.recorder.show_cursor = False
        else:
            self.recorder.show_cursor = True
            self.recorder.cursor_style = style
        self.recorder.save_settings()


if __name__ == "__main__":
    app = ScreenRecorderApp()
    app.mainloop()
