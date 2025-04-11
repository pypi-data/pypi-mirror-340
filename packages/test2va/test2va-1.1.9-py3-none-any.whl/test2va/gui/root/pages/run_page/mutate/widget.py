import customtkinter as ctk

text = "Mutator"
stop_fg = "red"


class RunPageMutateButtonWidget(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent, text=text, command=self.run)

        self.root = self.winfo_toplevel()
        self.og_fg = self._fg_color

        #self.root.run_butt_ref = self

    def run(self):
        success = self.root.run(mutate=True)
        if not success:
            return

