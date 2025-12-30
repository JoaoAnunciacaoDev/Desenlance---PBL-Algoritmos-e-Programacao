import tkinter as tk
from Model.Constants import *

class GameView(tk.Frame):

    grid_labels : list[list[tk.Label]]
    label_score_p1 : tk.Label
    label_score_p2 : tk.Label
    label_match : tk.Label
    label_status : tk.Label
    frame_placar : tk.Frame
    frame_grid : tk.Frame
    color_map : dict

    def __init__(self, master):
        super().__init__(master, bg=COLOR_BACKGROUND, padx=10, pady=10)

        self.color_map = {
            LETTER_STATUS["CORRECT"]: COLOR_RIGHT,
            LETTER_STATUS["WRONG_PLACE"]: COLOR_WRONG_PLACE,
            LETTER_STATUS["WRONG"]: COLOR_WRONG
        }

        self.grid_labels = []
        self.label_score_p1 = None
        self.label_score_p2 = None
        self.label_match = None
        self.label_status = None
        self.frame_placar = None
        self.frame_grid = None

        self._create_widgets()

    def _create_widgets(self):
        self.frame_placar = tk.Frame(self, bg=COLOR_BACKGROUND)
        self.frame_placar.pack(pady=10, fill="x", expand = True)

        self.label_score_p1 = tk.Label(self.frame_placar, text="Jogador 1: 0", font=FONT_STATUS, bg=COLOR_BACKGROUND, fg=COLOR_LETTER)
        self.label_score_p1.pack(side="left", padx=10)

        self.label_match = tk.Label(self.frame_placar, text="Rodada 0/0", font=FONT_STATUS, bg=COLOR_BACKGROUND, fg=COLOR_LETTER)
        self.label_match.pack(side="bottom", padx=10)

        self.label_score_p2 = tk.Label(self.frame_placar, text="0 : Jogador 2", font=FONT_STATUS, bg=COLOR_BACKGROUND, fg=COLOR_LETTER)
        self.label_score_p2.pack(side="right", padx=10)

        self.frame_grid = tk.Frame(self, bg=COLOR_BACKGROUND)
        self.frame_grid.pack(pady=(5, 10))

        self.grid_labels = []
        for i in range(6):
            labels_line : list[tk.Frame] = []
            frame_line : tk.Frame = tk.Frame(self.frame_grid, bg=COLOR_BACKGROUND)
            frame_line.pack()
            for j in range(5):
                lbl : tk.Label = tk.Label(frame_line, text = "", width = 4, height = 2, font = FONT_GRID, bg = COLOR_BACKGROUND, fg = COLOR_LETTER, relief = "solid",
                               borderwidth = 2, highlightthickness = 1, highlightbackground = COLOR_BORDER_ON)
                lbl.pack(side = "left", padx = 3, pady = 3)
                labels_line.append(lbl)
            self.grid_labels.append(labels_line)
        
        self.label_status = tk.Label(self, text = "Bem-vindo!", font = FONT_STATUS, bg = COLOR_BACKGROUND, fg = COLOR_LETTER, height = 2)
        self.label_status.pack(fill = "x", expand = True)


    def bind_controller(self, keyboard_handler):
        self.master.unbind("<Key>")
        self.master.unbind("<Return>")
        self.master.unbind("<BackSpace>")

        self.master.bind("<Key>", keyboard_handler)
        self.master.bind("<Return>", keyboard_handler)
        self.master.bind("<BackSpace>", keyboard_handler)

    def update_status(self, text_status : str, color = "white"):
        if self.label_status:
            self.label_status.config(text = text_status, fg = color)

    def update_grid_letter(self, line: int, column: int, letter: str, selected: bool = False):
        if 0 <= line < 6 and 0 <= column < 5:
            lbl = self.grid_labels[line][column]
            bg_color = COLOR_CURSOR if selected else COLOR_BACKGROUND
            border_color = COLOR_BORDER_ON if (selected or letter != "") else COLOR_BORDER_OFF

            lbl.config(text=letter.upper(), bg=bg_color, fg=COLOR_LETTER, highlightbackground=border_color)

    def update_line_result(self, line : int, result_letters : list):
        if 0 <= line < 6:
            for j in range(5):
                letter, logic_status = result_letters[j]
                background_color = self.color_map.get(logic_status, COLOR_WRONG)
                
                lbl = self.grid_labels[line][j]
                lbl.config(text = letter.upper(), bg = background_color, fg = COLOR_LETTER, highlightbackground = COLOR_BORDER_OFF)

    def update_scoreboard(self, score_j1 : str, score_j2 : str, matches : str):
        if self.label_score_p1:
            self.label_score_p1.config(text = score_j1)
        
        if self.label_score_p2:
            self.label_score_p2.config(text = score_j2)
        
        if self.label_match:
            self.label_match.config(text = matches)
    
    def show_score_j2(self, to_show : bool):
        if not self.label_score_p2: return

        if to_show:
            self.label_score_p2.pack(side = "right", padx = 10)
        else:
            self.label_score_p2.pack_forget()

    def reset_grid(self):
        for i in range(6):
            for j in range(5):
                lbl = self.grid_labels[i][j]
                lbl.config(text = "", bg = COLOR_BACKGROUND, fg = COLOR_LETTER, highlightbackground = COLOR_BORDER_OFF)

    