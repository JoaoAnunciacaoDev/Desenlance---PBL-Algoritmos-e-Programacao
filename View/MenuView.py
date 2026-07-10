import tkinter as tk

from Model.Constants import (
    COLOR_ACCENT,
    COLOR_ACCENT_HOVER,
    COLOR_BACKGROUND,
    COLOR_BORDER_OFF,
    COLOR_BORDER_ON,
    COLOR_CARD,
    COLOR_LETTER,
    COLOR_RIGHT,
    COLOR_TEXT_MUTED,
    COLOR_WRONG,
    COLOR_WRONG_PLACE,
    FONT_BUTTON,
    FONT_LABEL,
    FONT_MENU_TITLE,
    FONT_SUBTITLE,
)


class MenuView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLOR_BACKGROUND)
        self.start_game_handler = None
        self.current_mode = 1
        self.num_rounds = 3

        self._create_widgets()

    def _create_widgets(self):
        self.card_frame = tk.Frame(
            self, bg=COLOR_CARD, padx=40, pady=30, relief="solid", borderwidth=1, highlightthickness=0
        )
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center")

        lbl_title = tk.Label(self.card_frame, text="DESENLANCE", font=FONT_MENU_TITLE, bg=COLOR_CARD, fg=COLOR_LETTER)
        lbl_title.pack(pady=(0, 5))

        lbl_subtitle = tk.Label(
            self.card_frame,
            text="O jogo de palavras estilo Wordle",
            font=FONT_SUBTITLE,
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
        )
        lbl_subtitle.pack(pady=(0, 25))

        lbl_mode = tk.Label(self.card_frame, text="MODO DE JOGO", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER)
        lbl_mode.pack(anchor="w", pady=(0, 5))

        mode_frame = tk.Frame(self.card_frame, bg=COLOR_CARD)
        mode_frame.pack(fill="x", pady=(0, 20))

        self.btn_mode_1 = tk.Button(
            mode_frame,
            text="1 Jogador",
            font=FONT_BUTTON,
            relief="flat",
            bd=0,
            height=1,
            width=12,
            activebackground=COLOR_ACCENT,
            activeforeground=COLOR_LETTER,
            command=lambda: self._set_mode(1),
        )
        self.btn_mode_1.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_mode_2 = tk.Button(
            mode_frame,
            text="2 Jogadores",
            font=FONT_BUTTON,
            relief="flat",
            bd=0,
            height=1,
            width=12,
            activebackground=COLOR_ACCENT,
            activeforeground=COLOR_LETTER,
            command=lambda: self._set_mode(2),
        )
        self.btn_mode_2.pack(side="right", expand=True, fill="x", padx=(5, 0))

        self.names_frame = tk.Frame(self.card_frame, bg=COLOR_CARD)
        self.names_frame.pack(fill="x", pady=(0, 15))

        self.lbl_p1 = tk.Label(
            self.names_frame, text="NOME DO JOGADOR 1", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER
        )
        self.lbl_p1.pack(anchor="w", pady=(0, 3))
        self.entry_p1 = tk.Entry(
            self.names_frame,
            font=("Segoe UI", 12),
            bg=COLOR_BACKGROUND,
            fg=COLOR_LETTER,
            insertbackground=COLOR_LETTER,
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER_OFF,
            highlightcolor=COLOR_BORDER_ON,
        )
        self.entry_p1.pack(fill="x", pady=(0, 15))
        self.entry_p1.insert(0, "Jogador 1")

        self.frame_p2_input = tk.Frame(self.names_frame, bg=COLOR_CARD)
        self.lbl_p2 = tk.Label(
            self.frame_p2_input, text="NOME DO JOGADOR 2", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER
        )
        self.lbl_p2.pack(anchor="w", pady=(0, 3))
        self.entry_p2 = tk.Entry(
            self.frame_p2_input,
            font=("Segoe UI", 12),
            bg=COLOR_BACKGROUND,
            fg=COLOR_LETTER,
            insertbackground=COLOR_LETTER,
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER_OFF,
            highlightcolor=COLOR_BORDER_ON,
        )
        self.entry_p2.pack(fill="x")
        self.entry_p2.insert(0, "Jogador 2")

        lbl_rounds = tk.Label(
            self.card_frame, text="NÚMERO DE RODADAS", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER
        )
        lbl_rounds.pack(anchor="w", pady=(0, 5))

        rounds_frame = tk.Frame(self.card_frame, bg=COLOR_CARD)
        rounds_frame.pack(fill="x", pady=(0, 25))

        btn_dec = tk.Button(
            rounds_frame,
            text="-",
            font=FONT_BUTTON,
            relief="flat",
            bd=0,
            width=3,
            bg=COLOR_BACKGROUND,
            fg=COLOR_LETTER,
            activebackground=COLOR_BORDER_OFF,
            activeforeground=COLOR_LETTER,
            command=self._decrement_rounds,
        )
        btn_dec.pack(side="left")
        self._bind_hover(btn_dec, COLOR_BORDER_OFF, COLOR_BACKGROUND)

        self.lbl_rounds_val = tk.Label(
            rounds_frame, text=str(self.num_rounds), font=FONT_BUTTON, bg=COLOR_CARD, fg=COLOR_LETTER, width=6
        )
        self.lbl_rounds_val.pack(side="left", padx=10)

        btn_inc = tk.Button(
            rounds_frame,
            text="+",
            font=FONT_BUTTON,
            relief="flat",
            bd=0,
            width=3,
            bg=COLOR_BACKGROUND,
            fg=COLOR_LETTER,
            activebackground=COLOR_BORDER_OFF,
            activeforeground=COLOR_LETTER,
            command=self._increment_rounds,
        )
        btn_inc.pack(side="left")
        self._bind_hover(btn_inc, COLOR_BORDER_OFF, COLOR_BACKGROUND)

        self.btn_start = tk.Button(
            self.card_frame,
            text="COMEÇAR JOGO",
            font=FONT_BUTTON,
            bg=COLOR_ACCENT,
            fg=COLOR_LETTER,
            relief="flat",
            bd=0,
            height=2,
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground=COLOR_LETTER,
            command=self._on_start_click,
        )
        self.btn_start.pack(fill="x", pady=(0, 20))
        self._bind_hover(self.btn_start, COLOR_ACCENT_HOVER, COLOR_ACCENT)

        inst_frame = tk.Frame(self.card_frame, bg=COLOR_CARD)
        inst_frame.pack(fill="x")

        lbl_inst_title = tk.Label(
            inst_frame, text="COMO JOGAR", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED
        )
        lbl_inst_title.pack(anchor="w", pady=(0, 8))

        rules = [
            (COLOR_RIGHT, "Letra correta no lugar correto"),
            (COLOR_WRONG_PLACE, "Letra na palavra, mas no lugar errado"),
            (COLOR_WRONG, "Letra não faz parte da palavra"),
        ]

        for color, text in rules:
            r_row = tk.Frame(inst_frame, bg=COLOR_CARD)
            r_row.pack(anchor="w", pady=3)

            sq = tk.Frame(
                r_row, width=16, height=16, bg=color, highlightthickness=1, highlightbackground=COLOR_BORDER_OFF
            )
            sq.pack(side="left", padx=(0, 8))
            sq.pack_propagate(False)

            tk.Label(r_row, text=text, font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_LETTER).pack(side="left")

        self._set_mode(1)

    def _set_mode(self, mode):
        self.current_mode = mode
        if mode == 1:
            self.btn_mode_1.config(bg=COLOR_ACCENT, fg=COLOR_LETTER)
            self.btn_mode_2.config(bg=COLOR_BACKGROUND, fg=COLOR_LETTER)
            self._bind_hover(self.btn_mode_1, COLOR_ACCENT_HOVER, COLOR_ACCENT)
            self._bind_hover(self.btn_mode_2, COLOR_BORDER_OFF, COLOR_BACKGROUND)
            self.frame_p2_input.pack_forget()
        else:
            self.btn_mode_1.config(bg=COLOR_BACKGROUND, fg=COLOR_LETTER)
            self.btn_mode_2.config(bg=COLOR_ACCENT, fg=COLOR_LETTER)
            self._bind_hover(self.btn_mode_1, COLOR_BORDER_OFF, COLOR_BACKGROUND)
            self._bind_hover(self.btn_mode_2, COLOR_ACCENT_HOVER, COLOR_ACCENT)
            self.frame_p2_input.pack(fill="x")

    def _decrement_rounds(self):
        if self.num_rounds > 1:
            self.num_rounds -= 1
            self.lbl_rounds_val.config(text=str(self.num_rounds))

    def _increment_rounds(self):
        if self.num_rounds < 20:
            self.num_rounds += 1
            self.lbl_rounds_val.config(text=str(self.num_rounds))

    def _bind_hover(self, btn, hover_bg, normal_bg):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))

    def _on_start_click(self):
        p1 = self.entry_p1.get().strip() or "Jogador 1"
        p2 = self.entry_p2.get().strip() or "Jogador 2"
        if self.current_mode == 1:
            p2 = "Computador"

        if self.start_game_handler:
            self.start_game_handler(self.current_mode, p1, p2, self.num_rounds)

    def bind_controller(self, start_game_handler):
        self.start_game_handler = start_game_handler
