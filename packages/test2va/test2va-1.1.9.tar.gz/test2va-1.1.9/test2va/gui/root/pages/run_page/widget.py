import customtkinter as ctk

from test2va.gui.root.pages.run_page.generator import RunPageGenButtonWidget
from test2va.gui.root.pages.run_page.mutate import RunPageMutateButtonWidget
from test2va.gui.root.pages.run_page.prediction import RunPagePredictButtonWidget
from test2va.gui.root.pages.run_page.output import RunPageOutputWidget
from test2va.gui.root.pages.run_page.parse import RunPageParseButtonWidget
from test2va.gui.root.pages.run_page.run import RunPageRunButtonWidget
from test2va.gui.shared import prof_bg, entry_padx, light_pro_bg

corner_rad = 0
border_width = 0
fg = prof_bg

# Light
light_fg = light_pro_bg

cols = 5
c_weight = 1

rows = 1
r_weight = 1

tbox_col = 0
tbox_row = 0
tbox_sticky = "nsew"

run_col = 0
run_row = 1
run_sticky = "nsew"

parse_col = 1
parse_row = 1
parse_sticky = "nsew"

predict_col = 2
predict_row = 1
predict_sticky = "nsew"

mutate_col = 3
mutate_row = 1
mutate_sticky = "nsew"

gen_col = 4
gen_row = 1
gen_sticky = "nsew"

padx = entry_padx
pady = 5

button_padx = 3


class RunPageWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=prof_bg, border_width=border_width, corner_radius=corner_rad)

        self.grid_columnconfigure(0, weight=c_weight)
        self.grid_columnconfigure(1, weight=c_weight)
        self.grid_columnconfigure(2, weight=c_weight)
        self.grid_columnconfigure(3, weight=c_weight)
        self.grid_columnconfigure(4, weight=c_weight)
        self.grid_rowconfigure(rows, weight=r_weight)

        self.output = RunPageOutputWidget(self)
        self.output.grid(row=tbox_row, column=tbox_col, sticky=tbox_sticky, padx=padx, pady=pady, columnspan=5)

        self.run = RunPageRunButtonWidget(self)
        self.run.grid(row=run_row, column=run_col, sticky=run_sticky, padx=button_padx, pady=pady)

        self.parse = RunPageParseButtonWidget(self)
        self.parse.grid(row=parse_row, column=parse_col, sticky=parse_sticky, padx=button_padx, pady=pady)

        self.prediction = RunPagePredictButtonWidget(self)
        self.prediction.grid(row=predict_row, column=predict_col, sticky=predict_sticky, padx=button_padx, pady=pady)

        self.mutate = RunPageMutateButtonWidget(self)
        self.mutate.grid(row=mutate_row, column=mutate_col, sticky=mutate_sticky, padx=button_padx, pady=pady)

        self.generate = RunPageGenButtonWidget(self)
        self.generate.grid(row=gen_row, column=gen_col, sticky=gen_sticky, padx=button_padx, pady=pady)

        if ctk.get_appearance_mode() == "Light":
            self.config_light()

    def config_light(self):
        self.configure(fg_color=light_fg)
