import customtkinter as ctk

text = "Choose a Java Source Code File"
corner_rad = 0
anchor = "w"
justify = "left"


class SaveProfLabelWidget(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent, text=text, corner_radius=corner_rad, anchor=anchor, justify=justify)
