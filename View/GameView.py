import tkinter as tk
import typing

from Model.Constants import (
    COLOR_ACCENT,
    COLOR_ACCENT_HOVER,
    COLOR_BACKGROUND,
    COLOR_BORDER_OFF,
    COLOR_BORDER_ON,
    COLOR_BUTTON_DEFAULT,
    COLOR_CARD,
    COLOR_CURSOR,
    COLOR_LETTER,
    COLOR_RIGHT,
    COLOR_WRONG,
    COLOR_WRONG_PLACE,
    FONT_BUTTON,
    FONT_GRID,
    FONT_KEYBOARD,
    FONT_LABEL,
    FONT_STATUS,
    FONT_TITLE,
    LETTER_STATUS,
)


class ResultModal(tk.Frame):
    def __init__(self, parent, title, message, button1_text, button1_callback, button2_text, button2_callback):
        super().__init__(parent, bg="#0B0B0C")

        # Card centralizado
        card = tk.Frame(self, bg=COLOR_CARD, padx=40, pady=30, relief="solid", borderwidth=1, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        lbl_title = tk.Label(card, text=title.upper(), font=FONT_TITLE, bg=COLOR_CARD, fg=COLOR_LETTER)
        lbl_title.pack(pady=(0, 15))

        # Mensagem
        lbl_msg = tk.Label(card, text=message, font=FONT_STATUS, bg=COLOR_CARD, fg=COLOR_LETTER, justify="center")
        lbl_msg.pack(pady=(0, 25))

        # Container de botões
        btn_frame = tk.Frame(card, bg=COLOR_CARD)
        btn_frame.pack(fill="x")

        btn1 = tk.Button(
            btn_frame,
            text=button1_text,
            font=FONT_BUTTON,
            bg=COLOR_ACCENT,
            fg=COLOR_LETTER,
            relief="flat",
            bd=0,
            height=2,
            width=15,
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground=COLOR_LETTER,
            command=button1_callback,
        )
        btn1.pack(side="left", padx=5, expand=True)
        self.bind_hover(btn1, COLOR_ACCENT_HOVER, COLOR_ACCENT)

        btn2 = tk.Button(
            btn_frame,
            text=button2_text,
            font=FONT_BUTTON,
            bg=COLOR_BACKGROUND,
            fg=COLOR_LETTER,
            relief="flat",
            bd=0,
            height=2,
            width=15,
            activebackground=COLOR_BORDER_OFF,
            activeforeground=COLOR_LETTER,
            command=button2_callback,
        )
        btn2.pack(side="right", padx=5, expand=True)
        self.bind_hover(btn2, COLOR_BORDER_OFF, COLOR_BACKGROUND)

    def bind_hover(self, btn, hover_bg, normal_bg):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))


class GameView(tk.Frame):
    color_map: dict[str, str]
    grid_labels: list[list[tk.Label]]
    label_score_p1: tk.Label
    label_score_p2: tk.Label
    label_match: tk.Label
    label_status: tk.Label

    frame_placar: tk.Frame
    frame_grid: tk.Frame
    frame_keyboard: tk.Frame

    frame_historico_p1: tk.Frame
    frame_historico_p2: tk.Frame
    lbl_hist_p1: tk.Label
    lbl_hist_p2: tk.Label
    listbox_hist_p1: tk.Listbox
    listbox_hist_p2: tk.Listbox

    frame_corpo: tk.Frame
    grid_container: tk.Frame
    grid_canvas: tk.Canvas
    grid_scrollbar: tk.Scrollbar
    canvas_window: int

    keyboard_buttons: dict[str, tk.Button]
    keyboard_key_colors: dict[str, str]
    active_modal: ResultModal | None
    virtual_key_handler: typing.Callable | None
    is_shaking: bool

    def __init__(self, master):
        super().__init__(master, bg=COLOR_BACKGROUND, padx=15, pady=15)

        self.color_map = {
            LETTER_STATUS["CORRECT"]: COLOR_RIGHT,
            LETTER_STATUS["WRONG_PLACE"]: COLOR_WRONG_PLACE,
            LETTER_STATUS["WRONG"]: COLOR_WRONG,
        }

        self.grid_labels = []

        self.keyboard_buttons = {}
        self.keyboard_key_colors = {}
        self.active_modal = None
        self.virtual_key_handler = None
        self.is_shaking = False

        self._create_widgets()

    def _create_widgets(self):
        self.frame_placar = tk.Frame(
            self, bg=COLOR_CARD, padx=20, pady=10, relief="solid", borderwidth=1, highlightthickness=0
        )
        self.frame_placar.pack(pady=(5, 10), fill="x", side="top")

        self.frame_placar.columnconfigure(0, weight=1, uniform="placar")
        self.frame_placar.columnconfigure(1, weight=1, uniform="placar")
        self.frame_placar.columnconfigure(2, weight=1, uniform="placar")

        self.label_score_p1 = tk.Label(
            self.frame_placar, text="Jogador 1: 0", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER
        )
        self.label_score_p1.grid(row=0, column=0, sticky="w")

        match_badge = tk.Frame(self.frame_placar, bg=COLOR_BACKGROUND, padx=10, pady=4, relief="flat")
        match_badge.grid(row=0, column=1)

        self.label_match = tk.Label(
            match_badge, text="RODADA 0/0", font=("Segoe UI", 9, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_LETTER
        )
        self.label_match.pack()

        self.label_score_p2 = tk.Label(
            self.frame_placar, text="0 : Jogador 2", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER
        )
        self.label_score_p2.grid(row=0, column=2, sticky="e")

        self.frame_keyboard = tk.Frame(self, bg=COLOR_BACKGROUND)
        self.frame_keyboard.pack(pady=10, fill="x", side="bottom")

        rows = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "←"],
        ]

        self.keyboard_buttons = {}
        for r_idx, row in enumerate(rows):
            row_frame = tk.Frame(self.frame_keyboard, bg=COLOR_BACKGROUND)
            row_frame.pack(pady=2, fill="x")

            row_frame.rowconfigure(0, weight=1)
            for c_idx in range(len(row)):
                weight = 2 if row[c_idx] in ("ENTER", "←") else 1
                row_frame.columnconfigure(c_idx, weight=weight)

            for c_idx, key in enumerate(row):
                btn = tk.Button(
                    row_frame,
                    text=key,
                    font=FONT_KEYBOARD,
                    height=2,
                    bg=COLOR_BUTTON_DEFAULT,
                    fg=COLOR_LETTER,
                    relief="flat",
                    borderwidth=0,
                    activebackground=COLOR_BORDER_ON,
                    activeforeground=COLOR_LETTER,
                    command=lambda k=key: self._on_virtual_key_click(k),
                )
                btn.grid(row=0, column=c_idx, padx=2, sticky="nsew")
                self.keyboard_buttons[key] = btn
                self.keyboard_key_colors[key] = COLOR_BUTTON_DEFAULT
                self._bind_keyboard_hover(btn)

        self.label_status = tk.Label(
            self, text="Boa Sorte!", font=FONT_STATUS, bg=COLOR_BACKGROUND, fg=COLOR_LETTER, height=2
        )
        self.label_status.pack(fill="x", pady=5, side="bottom")

        self.frame_corpo = tk.Frame(self, bg=COLOR_BACKGROUND)
        self.frame_corpo.pack(pady=10, fill="both", expand=True, side="top")

        self.frame_historico_p1 = tk.Frame(
            self.frame_corpo,
            bg=COLOR_CARD,
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
            width=150,
        )
        self.frame_historico_p1.pack(side="left", fill="both", expand=False)
        self.frame_historico_p1.pack_propagate(False)

        self.lbl_hist_p1 = tk.Label(
            self.frame_historico_p1, text="Jogador 1", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER
        )
        self.lbl_hist_p1.pack(pady=(0, 5))

        self.listbox_hist_p1 = tk.Listbox(
            self.frame_historico_p1,
            bg=COLOR_CARD,
            fg=COLOR_LETTER,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0,
            selectbackground=COLOR_CARD,
            selectforeground=COLOR_LETTER,
        )
        self.listbox_hist_p1.pack(fill="both", expand=True)

        self.frame_historico_p2 = tk.Frame(
            self.frame_corpo,
            bg=COLOR_CARD,
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
            width=150,
        )
        self.frame_historico_p2.pack(side="right", fill="both", expand=False)
        self.frame_historico_p2.pack_propagate(False)

        self.lbl_hist_p2 = tk.Label(
            self.frame_historico_p2, text="Jogador 2", font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_LETTER
        )
        self.lbl_hist_p2.pack(pady=(0, 5))

        self.listbox_hist_p2 = tk.Listbox(
            self.frame_historico_p2,
            bg=COLOR_CARD,
            fg=COLOR_LETTER,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0,
            selectbackground=COLOR_CARD,
            selectforeground=COLOR_LETTER,
        )
        self.listbox_hist_p2.pack(fill="both", expand=True)

        self.grid_container = tk.Frame(self.frame_corpo, bg=COLOR_BACKGROUND)
        self.grid_container.pack(side="left", fill="both", expand=True, padx=10)

        self.grid_scrollbar = tk.Scrollbar(self.grid_container, orient="vertical")
        self.grid_scrollbar.pack(side="right", fill="y")

        self.grid_canvas = tk.Canvas(
            self.grid_container, bg=COLOR_BACKGROUND, highlightthickness=0, yscrollcommand=self.grid_scrollbar.set
        )
        self.grid_canvas.pack(side="left", fill="both", expand=True)
        self.grid_scrollbar.config(command=self.grid_canvas.yview)

        self.frame_grid = tk.Frame(self.grid_canvas, bg=COLOR_BACKGROUND)
        self.canvas_window = self.grid_canvas.create_window((0, 0), window=self.frame_grid, anchor="nw")

        def configure_layout(event=None):
            if getattr(self, "is_shaking", False):
                return
            canvas_width = self.grid_canvas.winfo_width()
            canvas_height = self.grid_canvas.winfo_height()
            grid_width = self.frame_grid.winfo_reqwidth()
            grid_height = self.frame_grid.winfo_reqheight()

            x = max(0, (canvas_width - grid_width) / 2)
            y = max(0, (canvas_height - grid_height) / 2)

            self.grid_canvas.coords(self.canvas_window, x, y)
            self.grid_canvas.configure(
                scrollregion=(0, 0, max(canvas_width, grid_width), max(canvas_height, grid_height))
            )

        self.frame_grid.bind("<Configure>", configure_layout)
        self.grid_canvas.bind("<Configure>", configure_layout)

        def _on_mousewheel(event):
            self.grid_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.grid_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.grid_labels = []
        for i in range(6):
            labels_line = []
            frame_line = tk.Frame(self.frame_grid, bg=COLOR_BACKGROUND)
            frame_line.pack()
            for j in range(5):
                lbl = tk.Label(
                    frame_line,
                    text="",
                    width=2,
                    height=1,
                    font=FONT_GRID,
                    bg=COLOR_BACKGROUND,
                    fg=COLOR_LETTER,
                    relief="solid",
                    borderwidth=2,
                    highlightthickness=1,
                    highlightbackground=COLOR_BORDER_OFF,
                )
                lbl.pack(side="left", padx=4, pady=4)
                labels_line.append(lbl)
            self.grid_labels.append(labels_line)

    def bind_controller(self, keyboard_handler, virtual_key_handler):
        self.master.unbind("<Key>")
        self.master.unbind("<Return>")
        self.master.unbind("<BackSpace>")

        self.master.bind("<Key>", keyboard_handler)
        self.master.bind("<Return>", keyboard_handler)
        self.master.bind("<BackSpace>", keyboard_handler)

        self.virtual_key_handler = virtual_key_handler

    def _on_virtual_key_click(self, key):
        if self.virtual_key_handler:
            self.virtual_key_handler(key)

    def _bind_keyboard_hover(self, btn):
        key = btn.cget("text")

        def on_enter(e):
            hover_colors = {
                COLOR_BUTTON_DEFAULT: "#9A9C9E",
                COLOR_RIGHT: COLOR_ACCENT_HOVER,
                COLOR_WRONG_PLACE: "#C5AF4B",
                COLOR_WRONG: "#4E4E50",
            }
            current_base = self.keyboard_key_colors.get(key, COLOR_BUTTON_DEFAULT)
            btn.config(bg=hover_colors.get(current_base, current_base))

        def on_leave(e):
            current_base = self.keyboard_key_colors.get(key, COLOR_BUTTON_DEFAULT)
            btn.config(bg=current_base)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def update_status(self, text_status: str, color="white"):
        if self.label_status:
            self.label_status.config(text=text_status, fg=color)

    def update_grid_letter(self, line: int, column: int, letter: str | None = None, selected: bool = False):
        if 0 <= line < 6 and 0 <= column < 5:
            lbl = self.grid_labels[line][column]

            if letter is None:
                letter = str(lbl.cget("text"))

            bg_color = COLOR_CURSOR if selected else COLOR_BACKGROUND
            border_color = COLOR_BORDER_ON if (selected or (letter != "")) else COLOR_BORDER_OFF

            lbl.config(text=letter.upper(), bg=bg_color, fg=COLOR_LETTER, highlightbackground=border_color)

    def update_keyboard_key_color(self, letter: str, logic_status: str):
        key = letter.upper()
        if key in self.keyboard_buttons:
            btn = self.keyboard_buttons[key]
            target_color = self.color_map.get(logic_status, COLOR_WRONG)

            current_base = self.keyboard_key_colors.get(key, COLOR_BUTTON_DEFAULT)

            should_update = False
            if current_base == COLOR_BUTTON_DEFAULT:
                should_update = True
            elif current_base == COLOR_WRONG:
                should_update = True
            elif current_base == COLOR_WRONG_PLACE and target_color == COLOR_RIGHT:
                should_update = True

            if should_update:
                self.keyboard_key_colors[key] = target_color
                btn.config(bg=target_color)

    def reset_keyboard_colors(self):
        for key, btn in self.keyboard_buttons.items():
            self.keyboard_key_colors[key] = COLOR_BUTTON_DEFAULT
            btn.config(bg=COLOR_BUTTON_DEFAULT)

    def animate_row_reveal(self, line: int, result_letters: list, index: int = 0, callback=None):
        if index >= 5:
            if callback:
                callback()
            return

        letter, logic_status = result_letters[index]
        background_color = self.color_map.get(logic_status, COLOR_WRONG)
        lbl = self.grid_labels[line][index]

        lbl.config(text=letter.upper(), bg=background_color, fg=COLOR_LETTER, highlightbackground=COLOR_BORDER_OFF)

        self.update_keyboard_key_color(letter, logic_status)

        self.master.after(180, lambda: self.animate_row_reveal(line, result_letters, index + 1, callback))

    def shake_grid(self, step=0):
        offsets = [10, -10, 8, -8, 5, -5, 3, -3, 0]
        if step == 0:
            self.is_shaking = True

        if step < len(offsets):
            offset = offsets[step]

            canvas_width = self.grid_canvas.winfo_width()
            canvas_height = self.grid_canvas.winfo_height()
            grid_width = self.frame_grid.winfo_reqwidth()
            grid_height = self.frame_grid.winfo_reqheight()

            base_x = max(0, (canvas_width - grid_width) / 2)
            base_y = max(0, (canvas_height - grid_height) / 2)

            self.grid_canvas.coords(self.canvas_window, base_x + offset, base_y)
            self.update_idletasks()
            self.master.after(25, lambda: self.shake_grid(step + 1))
        else:
            self.is_shaking = False
            canvas_width = self.grid_canvas.winfo_width()
            canvas_height = self.grid_canvas.winfo_height()
            grid_width = self.frame_grid.winfo_reqwidth()
            grid_height = self.frame_grid.winfo_reqheight()
            x = max(0, (canvas_width - grid_width) / 2)
            y = max(0, (canvas_height - grid_height) / 2)
            self.grid_canvas.coords(self.canvas_window, x, y)
            self.grid_canvas.configure(
                scrollregion=(0, 0, max(canvas_width, grid_width), max(canvas_height, grid_height))
            )

    def update_scoreboard(self, score_j1: str, score_j2: str, matches: str):
        if self.label_score_p1:
            self.label_score_p1.config(text=score_j1)

        if self.label_score_p2:
            self.label_score_p2.config(text=score_j2)

        if self.label_match:
            self.label_match.config(text=matches)

    def show_score_j2(self, to_show: bool):
        if not self.label_score_p2:
            return

        if to_show:
            self.label_score_p2.grid()
        else:
            self.label_score_p2.grid_remove()

    def reset_grid(self):
        for i in range(6):
            for j in range(5):
                lbl = self.grid_labels[i][j]
                lbl.config(text="", bg=COLOR_BACKGROUND, fg=COLOR_LETTER, highlightbackground=COLOR_BORDER_OFF)

    def show_modal(self, title: str, message: str, btn1_text: str, btn1_cb, btn2_text: str, btn2_cb):
        self.hide_modal()
        self.active_modal = ResultModal(self, title, message, btn1_text, btn1_cb, btn2_text, btn2_cb)
        self.active_modal.place(x=0, y=0, relwidth=1, relheight=1)

    def hide_modal(self):
        if self.active_modal:
            self.active_modal.place_forget()
            self.active_modal.destroy()
            self.active_modal = None

    def add_attempt_to_history(self, player_index: int, word: str):
        if player_index == 0:
            self.listbox_hist_p1.insert(tk.END, f" {word.upper()}")
            self.listbox_hist_p1.yview(tk.END)
        elif player_index == 1:
            self.listbox_hist_p2.insert(tk.END, f" {word.upper()}")
            self.listbox_hist_p2.yview(tk.END)

    def reset_histories(self, p1_name: str, p2_name: str = ""):
        self.listbox_hist_p1.delete(0, tk.END)
        self.listbox_hist_p2.delete(0, tk.END)
        self.lbl_hist_p1.config(text=p1_name)
        if p2_name:
            self.lbl_hist_p2.config(text=p2_name)
            self.lbl_hist_p2.pack(pady=(0, 5))
            self.listbox_hist_p2.pack(fill="both", expand=True)
            self.frame_historico_p2.config(bg=COLOR_CARD, relief="solid", borderwidth=1, highlightthickness=0)
        else:
            self.lbl_hist_p2.pack_forget()
            self.listbox_hist_p2.pack_forget()
            self.frame_historico_p2.config(bg=COLOR_BACKGROUND, relief="flat", borderwidth=0, highlightthickness=0)

        self.frame_historico_p2.pack(side="right", fill="both", expand=False)
