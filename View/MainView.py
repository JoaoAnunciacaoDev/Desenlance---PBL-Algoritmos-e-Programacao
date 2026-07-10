import tkinter as tk
from tkinter import messagebox

from Model.Constants import COLOR_BACKGROUND
from View.GameView import GameView
from View.MenuView import MenuView


class MainView(tk.Tk):
    def __init__(self, title="Desenlance"):
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        super().__init__()
        self.title(title)
        self.config(bg=COLOR_BACKGROUND)
        self.resizable(True, True)

        self.active_frame = None

        self.menu_view = MenuView(self)
        self.game_view = GameView(self)

        self._center_window(800, 700)

    def _center_window(self, width: int, height: int):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        x = (window_width // 2) - (width // 2)
        y = (window_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _change_frame(self, new_frame: tk.Frame):
        if self.active_frame:
            self.active_frame.pack_forget()

        self.active_frame = new_frame
        self.active_frame.pack(fill="both", expand=True)

    def run(self):
        self.mainloop()

    def show_game_view(self):
        self._change_frame(self.game_view)

    def show_menu_view(self):
        self._change_frame(self.menu_view)

    def show_popup_info(self, title: str, msg: str):
        messagebox.showinfo(title, msg, parent=self)

    def show_popup_erro(self, title: str, msg: str):
        messagebox.showerror(title, msg, parent=self)
