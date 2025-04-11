import os
from tkinter import filedialog
import tkinter as tk

import customtkinter as ctk
from test2va.gui.root.pages.home_page.input_frame.browse import java_browse

from test2va.gui.root.pages.home_page.input_frame.entry.browse import HomeEntryBrowseWidget

from test2va.gui.root.windows.parse_window.button_frame import SaveProfButtonFrameWidget
from test2va.gui.root.windows.parse_window.entry import SaveProfEntryWidget
from test2va.gui.root.windows.parse_window.label import SaveProfLabelWidget
from test2va.gui.shared import entry_padx

icon_path = os.path.join(os.path.dirname(__file__), "../../assets", "openmoji-android.ico")
size_x = 400
size_y = 115
resize_x = False
resize_y = False
title = "Test2VA Parse Only"
attributes = ("-topmost", True)

rows = 2
r_weight = 1

cols = [20, 1]
colspan = 2
c_weight = 1

label_col = 0
label_row = 0
label_sticky = "nsew"
label_padx = entry_padx
label_pady = 5

entry_col = 0
entry_row = 1
entry_sticky = "nsew"
entry_padx = 5

button_col = 0
button_row = 2
button_sticky = "sew"
button_pady = 5


class ParseOnlyWinWidget(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.root = parent

        self.iconbitmap(icon_path)
        self.geometry(f"{size_x}x{size_y}")
        self.resizable(resize_x, resize_y)
        self.title(title)
        self.attributes(*attributes)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        for i in range(len(cols)):
            self.grid_columnconfigure(i, weight=cols[i])
        self.grid_rowconfigure(rows, weight=r_weight)

        self.label = SaveProfLabelWidget(self)
        self.label.grid(row=label_row, column=label_col, sticky=label_sticky, padx=label_padx, pady=label_pady, columnspan=2)

        self.entry = SaveProfEntryWidget(self)
        self.entry.grid(row=entry_row, column=entry_col, sticky=entry_sticky, padx=entry_padx)

        self.browse = HomeEntryBrowseWidget(self, lambda: self.browse_cmd())
        self.browse.grid(row=entry_row, column=1, padx=entry_padx)

        self.button_frame = SaveProfButtonFrameWidget(self, self.entry, self.label)
        self.button_frame.grid(row=button_row, column=button_col, sticky=button_sticky, pady=button_pady, columnspan=2)

    def on_closing(self):
        self.root.parse_only_win_open = False
        self.destroy()

    def browse_cmd(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Java files", "*.java")]
        )

        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)
            self.entry.xview(tk.END)
