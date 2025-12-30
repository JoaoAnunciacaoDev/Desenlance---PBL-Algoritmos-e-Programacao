import tkinter as tk
from Model.Constants import GERAL_STATUS, COLOR_BORDER_ON, COLOR_BORDER_OFF

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.state_input = {
            "line": 0,
            "current_word": ["", "", "", "", ""],
            "cursor": 0
        }
        
        self.bind_events()

    def run(self):
        self.view.active_frame = self.view.menu_view
        self.view.active_frame.pack(fill="both", expand=True)
        self.view.run()

    def bind_events(self):
        self.view.menu_view.bind_controller(
            self._handler_start_1p, 
            self._handler_start_2p
        )
        self.view.game_view.bind_controller(self._handler_keyboard)

    def _handler_start_1p(self):
        self._setup_game(mode=1)

    def _handler_start_2p(self):
        self._setup_game(mode=2)

    def _setup_game(self, mode):
        p1 = self.view.ask_string("Nome", "Nome do Jogador 1:") or "Jogador 1"
        p2 = "Computador"
        if mode == 2:
            p2 = self.view.ask_string("Nome", "Nome do Jogador 2:") or "Jogador 2"
        
        rounds = self.view.ask_int("Partidas", "Total de partidas:", min_val=1, max_val=20) or 2
        
        self.model.start_new_game(mode, rounds, p1, p2)
        
        self.view.game_view.show_score_j2(mode == 2)
        self._update_ui_state()
        self.view.show_game_view()

    def _handler_keyboard(self, event):
        if self.model.geral_status != GERAL_STATUS["PLAYING"]:
            return

        line = self.state_input["line"]
        cursor = self.state_input["cursor"]

        if event.keysym == "BackSpace":
            if cursor > 0:
                old_cursor = cursor
                new_cursor = cursor - 1
                
                self.state_input["current_word"][old_cursor] = ""
                self.state_input["cursor"] -= 1                

                self.view.game_view.update_grid_letter(line, old_cursor, "", selected = False)
                self.view.game_view.update_grid_letter(line, new_cursor, None, selected = True)

        elif event.keysym == "Return":
            if "" not in self.state_input["current_word"]:
                self._handler_send_attempt()
                if line < 5:
                    self.view.game_view.update_grid_letter(line + 1, 0, "", selected = True)

            else:
                self.view.game_view.update_status(
                    "A palavra deve ter 5 letras!", "yellow"
                )

        elif event.keysym == "Left":
            if cursor > 0:
                self.view.game_view.update_grid_letter(line, cursor, self.state_input["current_word"][cursor], selected = False)

                self.state_input["cursor"] -= 1

                self.view.game_view.update_grid_letter(line, self.state_input["cursor"], self.state_input["current_word"][self.state_input["cursor"]], selected = True)

        elif event.keysym == "Right":
            if cursor < 4:
                self.view.game_view.update_grid_letter(line, cursor, self.state_input["current_word"][cursor], selected = False)

                self.state_input["cursor"] += 1

                self.view.game_view.update_grid_letter(line, self.state_input["cursor"], self.state_input["current_word"][self.state_input["cursor"]], selected = True)

        elif event.char.isalpha() and len(event.char) == 1:
            if cursor < len(self.state_input["current_word"]):
                letter = event.char.upper()
                self.state_input["current_word"][cursor] = letter
                self.view.game_view.update_grid_letter(line, cursor, letter, selected = False)

                if self.state_input["cursor"] < 4: self.state_input["cursor"] += 1

                if self.state_input["cursor"] < 5:
                    self.view.game_view.update_grid_letter(line, self.state_input["cursor"], self.state_input["current_word"][self.state_input["cursor"]],
                                                            selected = True)

    def _handler_send_attempt(self):
        word = "".join(self.state_input["current_word"])
        result = self.model.process_attempt(word)

        if result.get("error"):
            self.view.game_view.update_status("Palavra inválida!", "red")
            return

        self.view.game_view.update_line_result(
            self.state_input["line"], result["letter_results"]
        )

        self.state_input["line"] += 1
        self.state_input["cursor"] = 0
        self.state_input["current_word"] = ["", "", "", "", ""]

        if result["round_status"] != "playing":
            self._handle_end_of_round(result)

    def _handle_end_of_round(self, result):
        secret = result["secret_word"]
        msg = f"A palavra era: {secret}"
        self.view.show_popup_info("Fim da Rodada", msg)
        
        if result["geral_status"] == GERAL_STATUS["END"]:
            final = self.model.get_final_result()
            res_msg = f"Vencedor: {final.get('vencedor', 'Empate')} com {final.get('pontos', 0)} pontos."
            self.view.show_popup_info("Fim de Jogo", res_msg)
            self.view.quit()
        else:
            self.state_input = {"line": 0, "cursor": 0, "current_word": ["", "", "", "", ""]}
            self.view.game_view.reset_grid()
            self._update_ui_state()

    def _update_ui_state(self):
        state = self.model.get_current_state()
        p1_name = self.model.players[0]
        p2_name = self.model.players[1] if len(self.model.players) > 1 else ""
        
        score_j1 = f"{p1_name}: {state['scores'].get(p1_name, 0)}"
        score_j2 = f"{state['scores'].get(p2_name, 0)} : {p2_name}"
        matches = f"Rodada {state['round_number']} / {state['total_rounds']}"
        
        self.view.game_view.update_scoreboard(score_j1, score_j2, matches)
        self.view.game_view.update_status(f"Vez de: {state['current_player']}")