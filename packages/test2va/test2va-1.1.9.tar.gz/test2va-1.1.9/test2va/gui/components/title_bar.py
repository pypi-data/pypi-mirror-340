import os
import time
from importlib.metadata import version
import tkinter as tk
from PIL import Image, ImageTk

TITLE_BG = "#0C090A"
HOVER_BG = "#1C1C1C"
ICON_SIZE = (25, 25)

ASSET_PATH = os.path.join(os.path.dirname(__file__), "../assets")


def on_hover(event):
    event.widget.config(bg=HOVER_BG)


def on_leave(event):
    event.widget.config(bg=TITLE_BG)


def start_move(root, event):
    root.x = event.x
    root.y = event.y


def stop_move(root, event):
    root.x = None
    root.y = None


def on_move(root, event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")


def on_x_click(gui):
    gui.onclose()


def on_minimize_click(gui):
    gui.root.overrideredirect(False)
    gui.root.iconify()


def on_refocus(gui):
    gui.root.overrideredirect(True)
    gui.root.deiconify()
    gui.root.unbind("<FocusIn>")


def title_bar_old(gui, parent):
    # Main title bar frame
    title_frame = tk.Frame(parent, highlightthickness=0, bg=TITLE_BG)
    title_frame.grid_rowconfigure(0, weight=1)
    title_frame.grid_columnconfigure(0, weight=1)
    title_frame.grid_columnconfigure(1, weight=500)
    title_frame.grid_columnconfigure(2, weight=1)
    title_frame.grid_columnconfigure(3, weight=1)

    # Top left icon
    title_icon_image = Image.open(os.path.join(ASSET_PATH, "openmoji-android.png")).resize(ICON_SIZE)
    title_icon_photo = ImageTk.PhotoImage(title_icon_image)
    title_icon_button = tk.Label(title_frame, image=title_icon_photo, borderwidth=0, highlightthickness=0, bg=TITLE_BG, activebackground=TITLE_BG)
    title_icon_button.image = title_icon_photo # Stop garbage collection
    title_icon_button.grid(row=0, column=0, sticky="w")

    # Title label
    title_label = tk.Label(title_frame, text=f"Test2VA {version('test2va')}", font=("Segoe UI", 11), bg=TITLE_BG, fg="white", anchor="center", justify="center")
    title_label.grid(row=0, column=1, columnspan=2, sticky="nsew")

    # Minimize button
    minimize_image = Image.open(os.path.join(ASSET_PATH, "openmoji-minus.png")).resize(ICON_SIZE)
    minimize_photo = ImageTk.PhotoImage(minimize_image)
    minimize_button = tk.Label(title_frame, borderwidth=0, highlightthickness=0, bg=TITLE_BG, activebackground=TITLE_BG)
    minimize_button.image = minimize_photo # Stop garbage collection
    minimize_button.grid(row=0, column=2, sticky="e")
    #minimize_button.bind("<Enter>", on_hover)
    #minimize_button.bind("<Leave>", on_leave)
    #minimize_button.bind("<Button-1>", lambda event: on_minimize_click(gui))

    # Close button
    close_image = Image.open(os.path.join(ASSET_PATH, "openmoji-x.png")).resize(ICON_SIZE)
    close_photo = ImageTk.PhotoImage(close_image)
    close_button = tk.Label(title_frame, image=close_photo, borderwidth=0, highlightthickness=0, bg=TITLE_BG, activebackground=TITLE_BG)
    close_button.image = close_photo # Stop garbage collection
    close_button.grid(row=0, column=3, sticky="e")
    close_button.bind("<Enter>", on_hover)
    close_button.bind("<Leave>", on_leave)
    close_button.bind("<Button-1>", lambda event: on_x_click(gui))

    title_label.bind("<ButtonPress-1>", lambda event: start_move(gui.root, event))
    title_label.bind("<ButtonRelease-1>", lambda event: stop_move(gui.root, event))
    title_label.bind("<B1-Motion>", lambda event: on_move(gui.root, event))

    return title_frame


def title_bar(gui):
    gui.root.title(f"Test2VA {version('test2va')}")

    icon_path = os.path.join(ASSET_PATH, "openmoji-android.png")
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Set the window icon
    gui.root.iconphoto(False, icon_photo)

    menu_bar = tk.Menu(gui.root)

    # Profile menu
    profile_menu = tk.Menu(menu_bar, tearoff=0)
    profile_menu.add_command(label="New Profile")
    profile_menu.add_command(label="Load Profile")

    menu_bar.add_cascade(label="Profile", menu=profile_menu)

    gui.root.config(menu=menu_bar)

