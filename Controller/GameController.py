from Model.Constants import GERAL_STATUS


class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.state_input = {"line": 0, "current_word": ["", "", "", "", ""], "cursor": 0}
        self.is_animating = False

        self.bind_events()

    def run(self):
        self.view.show_menu_view()
        self.view.run()

    def bind_events(self):
        self.view.menu_view.bind_controller(self._handler_start_game)
        self.view.game_view.bind_controller(self._handler_keyboard, self._handler_virtual_key)

    def _handler_start_game(self, mode, p1_name, p2_name, rounds):
        self.model.start_new_game(mode, rounds, p1_name, p2_name)

        self.view.game_view.show_score_j2(mode == 2)
        self.view.game_view.reset_keyboard_colors()
        self.view.game_view.reset_grid()

        p1 = self.model.players[0]
        p2 = self.model.players[1] if len(self.model.players) > 1 else ""
        self.view.game_view.reset_histories(p1, p2 if mode == 2 else "")

        self.is_animating = False
        self.state_input = {"line": 0, "cursor": 0, "current_word": ["", "", "", "", ""]}

        self._update_ui_state()
        self.view.show_game_view()

        self.view.game_view.update_grid_letter(0, 0, "", selected=True)

    def _handler_keyboard(self, event):
        if self.model.geral_status != GERAL_STATUS["PLAYING"] or self.is_animating:
            return

        if event.keysym == "BackSpace" or event.char == "\x08":
            self.process_key_input("BackSpace")
        elif event.keysym == "Return" or event.char == "\r":
            self.process_key_input("Return")
        elif event.keysym == "Left":
            self.process_key_input("Left")
        elif event.keysym == "Right":
            self.process_key_input("Right")
        elif event.char.isalpha() and len(event.char) == 1:
            self.process_key_input(event.char.upper())

    def _handler_virtual_key(self, key):
        if self.model.geral_status != GERAL_STATUS["PLAYING"] or self.is_animating:
            return

        if key == "←":
            self.process_key_input("BackSpace")
        elif key == "ENTER":
            self.process_key_input("Return")
        else:
            self.process_key_input(key)

    def process_key_input(self, key_name):
        line = self.state_input["line"]
        cursor = self.state_input["cursor"]
        current_word = self.state_input["current_word"]

        if key_name == "BackSpace":
            if current_word[cursor] != "":
                current_word[cursor] = ""
                self.view.game_view.update_grid_letter(line, cursor, "", selected=True)
            else:
                if cursor > 0:
                    self.view.game_view.update_grid_letter(line, cursor, None, selected=False)
                    self.state_input["cursor"] -= 1
                    new_cursor = self.state_input["cursor"]
                    current_word[new_cursor] = ""
                    self.view.game_view.update_grid_letter(line, new_cursor, "", selected=True)

        elif key_name == "Return":
            if "" not in current_word:
                self._handler_send_attempt()
            else:
                self.view.game_view.update_status("A palavra deve ter 5 letras!", "yellow")
                self.view.game_view.shake_grid()

        elif key_name == "Left":
            if cursor > 0:
                self.view.game_view.update_grid_letter(line, cursor, None, selected=False)
                self.state_input["cursor"] -= 1
                self.view.game_view.update_grid_letter(line, self.state_input["cursor"], None, selected=True)

        elif key_name == "Right":
            if cursor < 4:
                self.view.game_view.update_grid_letter(line, cursor, None, selected=False)
                self.state_input["cursor"] += 1
                self.view.game_view.update_grid_letter(line, self.state_input["cursor"], None, selected=True)

        elif len(key_name) == 1 and key_name.isalpha():
            letter = key_name.upper()
            current_word[cursor] = letter
            self.view.game_view.update_grid_letter(line, cursor, letter, selected=True)

            if cursor < 4:
                self.view.game_view.update_grid_letter(line, cursor, None, selected=False)
                self.state_input["cursor"] += 1
                self.view.game_view.update_grid_letter(line, self.state_input["cursor"], None, selected=True)

    def _handler_send_attempt(self):
        word = "".join(self.state_input["current_word"])
        current_player_idx = self.model.current_player_index

        result = self.model.process_attempt(word)

        if result.get("error"):
            self.view.game_view.update_status("Palavra inválida!", "#FF5555")
            self.view.game_view.shake_grid()
            return

        self.view.game_view.add_attempt_to_history(current_player_idx, word)

        self.is_animating = True
        current_line = self.state_input["line"]

        self.view.game_view.update_grid_letter(current_line, self.state_input["cursor"], None, selected=False)

        self.state_input["line"] += 1
        self.state_input["cursor"] = 0
        self.state_input["current_word"] = ["", "", "", "", ""]

        def on_reveal_finished():
            self.is_animating = False
            if result["round_status"] != "playing":
                self._update_scoreboard_only(result)
                self._handle_end_of_round(result)
            else:
                self._update_ui_state()
                if self.state_input["line"] < 6:
                    self.view.game_view.update_grid_letter(self.state_input["line"], 0, "", selected=True)

        self.view.game_view.animate_row_reveal(current_line, result["letter_results"], callback=on_reveal_finished)

    def _handle_end_of_round(self, result):
        secret = result["secret_word"]

        if result["geral_status"] == GERAL_STATUS["END"]:
            final = self.model.get_final_result()
            winner = final.get("vencedor", "Empate")
            points = final.get("pontos", 0)

            if winner == "Empate":
                msg = f"O jogo terminou em EMPATE!\nAmbos os jogadores fizeram {points} pontos.\n\nA última palavra secreta era: {secret}"
            elif self.model.game_mode == 1:
                msg = f"Fim de jogo!\nVocê terminou com {points} pontos.\n\nA última palavra secreta era: {secret}"
            else:
                msg = f"Fim de jogo! Vitória de {winner}!\nPlacar final: {points} pontos.\n\nA última palavra secreta era: {secret}"

            self.view.game_view.show_modal(
                title="Fim de Jogo",
                message=msg,
                btn1_text="Jogar Novamente",
                btn1_cb=self._action_restart_game,
                btn2_text="Voltar ao Menu",
                btn2_cb=self._action_back_to_menu,
            )
        else:
            last_player = result["player_who_played"]
            next_player = result["next_player"]
            points_won = self.model.scores.get(last_player, 0)

            msg = f"A palavra secreta era: {secret}\n\n"
            msg += f"Jogador {last_player} acumulou {points_won} pontos!\n\n"

            if self.model.game_mode == 2:
                msg += f"Vez de: {next_player} começar a próxima rodada!"
            else:
                msg += "Prepare-se para a próxima rodada."

            self.view.game_view.show_modal(
                title="Fim da Rodada",
                message=msg,
                btn1_text="Próxima Rodada",
                btn1_cb=self._action_next_round,
                btn2_text="Voltar ao Menu",
                btn2_cb=self._action_back_to_menu,
            )

    def _action_next_round(self):
        self.view.game_view.hide_modal()

        self.state_input = {"line": 0, "cursor": 0, "current_word": ["", "", "", "", ""]}
        self.view.game_view.reset_grid()
        self.view.game_view.reset_keyboard_colors()

        mode = self.model.game_mode
        p1 = self.model.players[0]
        p2 = self.model.players[1] if len(self.model.players) > 1 else ""
        self.view.game_view.reset_histories(p1, p2 if mode == 2 else "")

        self._update_ui_state()

        self.view.game_view.update_grid_letter(0, 0, "", selected=True)

    def _action_restart_game(self):
        self.view.game_view.hide_modal()

        mode = self.model.game_mode
        rounds = self.model.total_rounds
        p1 = self.model.players[0]
        p2 = self.model.players[1] if len(self.model.players) > 1 else "Computador"

        self.model.start_new_game(mode, rounds, p1, p2)

        self.state_input = {"line": 0, "cursor": 0, "current_word": ["", "", "", "", ""]}
        self.view.game_view.reset_grid()
        self.view.game_view.reset_keyboard_colors()

        self.view.game_view.reset_histories(p1, p2 if mode == 2 else "")

        self._update_ui_state()

        self.view.game_view.update_grid_letter(0, 0, "", selected=True)

    def _action_back_to_menu(self):
        self.view.game_view.hide_modal()
        self.model.reset_game()
        self.view.show_menu_view()

    def _update_scoreboard_only(self, result_dict):
        p1_name = self.model.players[0]
        p2_name = self.model.players[1] if len(self.model.players) > 1 else ""

        scores = result_dict["current_scores"]
        score_j1 = f"{p1_name}: {scores.get(p1_name, 0)}"
        score_j2 = f"{scores.get(p2_name, 0)} : {p2_name}" if p2_name else ""

        played_rounds = self.model.played_rounds
        total_rounds = self.model.total_rounds
        matches = f"RODADA {played_rounds} / {total_rounds}"

        self.view.game_view.update_scoreboard(score_j1, score_j2, matches)

    def _update_ui_state(self):
        state = self.model.get_current_state()
        p1_name = self.model.players[0]
        p2_name = self.model.players[1] if len(self.model.players) > 1 else ""

        score_j1 = f"{p1_name}: {state['scores'].get(p1_name, 0)}"
        score_j2 = f"{state['scores'].get(p2_name, 0)} : {p2_name}" if p2_name else ""
        matches = f"RODADA {state['round_number']} / {state['total_rounds']}"

        self.view.game_view.update_scoreboard(score_j1, score_j2, matches)
        self.view.game_view.update_status(f"Vez de: {state['current_player']}")
