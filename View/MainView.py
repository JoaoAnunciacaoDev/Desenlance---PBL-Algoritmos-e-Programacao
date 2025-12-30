import tkinter as tk
from tkinter import messagebox, simpledialog
from View.MenuView import MenuView
from View.GameView import GameView
from Model.Constants import COLOR_BACKGROUND

class MainView(tk.Tk):

    root : tk.Tk
    active_frame : tk.Frame
    menu_view : MenuView
    game_view : GameView

    def __init__(self, title = "Desenlance"):
        super().__init__()
        self.title(title)
        self.config(bg = COLOR_BACKGROUND)
        self.resizable(True, True)

        self.active_frame = None

        self.menu_view = MenuView(self)
        self.game_view = GameView(self)

        self._center_window(800, 600)
    
    def _center_window(self, width : float, height : float):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        
        x = ((window_width // 2) - (width // 2))
        y = ((window_height // 2) - (height // 2))

        self.geometry(f'{width}x{height}+{x}+{y}')

    def _change_frame(self, new_frame : tk.Frame):
        if self.active_frame:
            self.active_frame.pack_forget()
        
        self.active_frame = new_frame
        self.active_frame.pack(fill = "both", expand = True)

    def run(self):
        self.mainloop()

    def show_game_view(self):
        self._change_frame(self.game_view)

    def show_popup_info(self, title : str, msg : str):
        messagebox.showinfo(title, msg, parent = self)

    def show_popup_erro(self, title : str, msg : str):
        messagebox.showerror(title, msg, parent = self)
    
    def ask_string(self, title : str, msg : str) -> str | None:
        return simpledialog.askstring(title, msg, parent = self)
    
    def ask_int(self, title : str, msg : str, min_val = None, max_val = None) -> str | None:
        return simpledialog.askinteger(title, msg, parent = self, minvalue = min_val, maxvalue = max_val)