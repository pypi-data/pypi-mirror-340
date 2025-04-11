import customtkinter as ctk

from test2va.bridge import check_file_exists, save_profile
from test2va.gui.root.windows.parse_window.button_frame.button import SaveProfButtonWidget
from test2va.gui.shared import def_java_entry, def_udid_entry, def_api_entry

corner_rad = 0
border_width = 0
fg = "transparent"

cols = [1]
rows = [1]

button_row = 0
sticky = "nsew"
padx = 5

done_col = 0


class SaveProfButtonFrameWidget(ctk.CTkFrame):
    def __init__(self, parent, entry, label):
        super().__init__(parent, corner_radius=corner_rad, border_width=border_width, fg_color=fg)

        self.root = self.winfo_toplevel().root
        self.entry = entry
        self.label = label

        for i in range(len(rows)):
            self.grid_rowconfigure(i, weight=rows[i])

        for i in range(len(cols)):
            self.grid_columnconfigure(i, weight=cols[i])

        self.save = SaveProfButtonWidget(self, text="Done", command=self.parse_only)
        self.save.grid(row=button_row, column=done_col, sticky=sticky, padx=padx)

    def parse_only(self):
        if not self.entry.get():
            self.label.configure(text="⚠️ Please enter/browse a Java file path")
            return

        if not check_file_exists(self.entry.get()):
            self.label.configure(text="⚠️ Please enter a valid Java file path")
            return

        caps = self.root.format_caps()

        save_profile(self.entry.get(), i_frame.apk_entry.input.get(), caps, i_frame.udid_entry.input.get(),
                     i_frame.api_entry.input.get(), j_path, j_code)

        self.root.prof_list_ref.populate_profiles()

        self.label.configure(text="✔️ Profile saved successfully")

    def done(self):
        self.root.sav_prof_open = False
        self.winfo_toplevel().destroy()
