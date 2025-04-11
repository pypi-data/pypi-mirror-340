import customtkinter as ctk

from test2va.gui.root.windows.parse_window.widget import ParseOnlyWinWidget

text = "Parse"
stop_fg = "red"


class RunPageParseButtonWidget(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent, text=text, command=self.run)

        self.root = self.winfo_toplevel()
        self.og_fg = self._fg_color

        self.parse_only_win_open = False

        #self.root.run_butt_ref = self

    def run(self):
        self.root.run(parse_only=True)

