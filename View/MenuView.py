import tkinter as tk
from Model.Constants import COLOR_BACKGROUND, COLOR_LETTER, FONT_TITLE, FONT_KEYBOARD

class MenuView(tk.Frame):

    button_p1 : tk.Button
    button_p2 : tk.Button

    def __init__(self, master):
        super().__init__(master, bg=COLOR_BACKGROUND, padx=20, pady=20)

        self.button_p1 = None
        self.button_p2 = None

        self._create_widgets()

    def _create_widgets(self):
        lbl_title = tk.Label(self, text="Desenlance", font=FONT_TITLE, bg=COLOR_BACKGROUND, fg=COLOR_LETTER)
        lbl_title.pack(pady=(20, 40))

        self.button_p1 = tk.Button(self, text="Jogador 1", font=FONT_KEYBOARD, width=20, height=2)
        self.button_p1.pack(pady=10)

        self.button_p2 = tk.Button(self, text="Jogador 2", font=FONT_KEYBOARD, width=20, height=2)
        self.button_p2.pack(pady=10)
    
    def bind_controller(self, handler_1p_click, handler_2p_click):
        if self.button_p1:
            self.button_p1.config(command=handler_1p_click)

        if self.button_p2:
            self.button_p2.config(command=handler_2p_click)