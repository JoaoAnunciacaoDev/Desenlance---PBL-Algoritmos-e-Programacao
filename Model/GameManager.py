from Model.WordBank import WordBank
from Model.RoundManager import RoundManager
from Model.Constants import *

class GameManager:

    word_bank : WordBank
    round_manager : RoundManager
    
    game_mode : int
    players : list[str]
    scores : dict[str, int]
    total_rounds: int
    played_rounds: int
    current_player_index: int
    geral_status: str

    def __init__(self, archive_path : str):
        self.word_bank = WordBank(archive_path)
        self.reset_game()

    def start_new_game(self, mode : int, total_rounds : int, p1_name : str, p2_name : str):
        self.game_mode = mode
        self.total_rounds = total_rounds
        self.players = [p1_name]
        self.scores = {p1_name: 0}

        if mode == 2:
            self.players.append(p2_name)
            self.scores[p2_name] = 0

            if self.total_rounds % 2 != 0:
                self.total_rounds += 1
            
        self.played_rounds = 0
        self.current_player_index = 0
        self.geral_status = GERAL_STATUS["PLAYING"]

        self._start_next_round()

    def reset_game(self):
        self.round_manager = None
        self.game_mode = 0
        self.players = []
        self.scores = {}
        self.total_rounds = 0
        self.played_rounds = 0
        self.current_player_index = 0
        self.geral_status = GERAL_STATUS["MENU"]

    def _start_next_round(self):
        if self.played_rounds >= self.total_rounds:
            self.geral_status = GERAL_STATUS["END"]
            self.round_manager = None
            return

        word = self.word_bank.get_random_word()
        if word == "ERRO":
            self.geral_status = GERAL_STATUS["END"]
            print("Erro: Acabaram as palavras do banco!")
            return
            
        self.round_manager = RoundManager(word, 6)
        self.played_rounds += 1

    def get_current_player_name(self) -> str:
        return self.players[self.current_player_index]

    def process_attempt(self, word : str) -> dict:
        if self.geral_status != GERAL_STATUS["PLAYING"] or not self.round_manager:
            return {"error": "jogo_nao_ativo"}
        
        if not self.word_bank.is_valid_word(word):
            return {"error": "palavra_invalida"}
        
        result_letters : list = self.round_manager.send_attempt(word)
        round_status : str = self.round_manager.get_status()
        player_who_played : str = self.get_current_player_name()

        info : dict = {
            "error": None,
            "player_who_played": player_who_played,
            "letter_results": result_letters,
            "round_status": round_status,
            "geral_status": self.geral_status,
            "secret_word": None,
            "next_player": None,
            "current_scores": None
        }

        if round_status != ROUND_STATUS["PLAYING"]:
            if round_status == ROUND_STATUS["WIN"]:
                points : int = self.round_manager.get_points()
                self.scores[player_who_played] += points
            
            info["secret_word"] = "".join(self.round_manager.secret_word)

            if self.game_mode == 2:
                self.current_player_index = 1 - self.current_player_index
            
            self._start_next_round()
            info["geral_status"] = self.geral_status
        
        info["next_player"] = self.get_current_player_name() if self.geral_status == GERAL_STATUS["PLAYING"] else None
        info["current_scores"] = self.scores

        return info

    def get_current_state(self) -> dict:
        return {
            "geral_status": self.geral_status,
            "current_player": self.get_current_player_name() if self.geral_status == GERAL_STATUS["PLAYING"] else None,
            "scores": self.scores,
            "round_number": self.played_rounds,
            "total_rounds": self.total_rounds,
            "remaining_attempts": self.round_manager.remaining_attempts if self.round_manager else 0
        }

    def get_final_result(self) -> dict:
        if self.geral_status != GERAL_STATUS["END"]:
            return {"error": "o jogo ainda não terminou"}
        
        if self.game_mode == 1:
            j1 : str = self.players[0]
            return {"vencedor:": j1, "pontos": self.scores.get(j1, 0)}
        
        j1 : str = self.players[0]
        j2 : str = self.players[1]
        p1 : int = self.scores.get(j1, 0)
        p2 : int = self.scores.get(j2, 0)
        
        if p1 > p2:
            return {"vencedor": j1, "pontos": p1}
        elif p2 > p1:
            return {"vencedor": j2, "pontos": p2}
        else:
            return {"vencedor": "Empate", "pontos": p1}


if __name__ == "__main__":

    print("\n--- Testando GameManager ---")

    try:
        game = GameManager("words.txt")
        print(f"Status inicial: {game.geral_status}")
        
        print("\nIniciando jogo: 2 Jogadores, 2 Rodadas, Jogador 'Ana', Jogador 'Beto'")
        game.start_new_game(mode=2, total_rounds=2, p1_name="Ana", p2_name="Beto")
        
        print(f"Status do jogo: {game.geral_status}")
        print(f"Rodada {game.played_rounds} de {game.total_rounds}")
        print(f"Jogador da vez: {game.get_current_player_name()}")
        
        palavra_secreta_r1 = "".join(game.round_manager.secret_word)
        print(f"Palavra secreta da Rodada 1: {palavra_secreta_r1}")

        print("\nAna tenta 'PALCO'...")
        info = game.process_attempt("PALCO")
        
        if info.get("error"):
            print(f"Erro na tentativa: {info['error']}")
        else:
            print(f"Resultado da Rodada 1 (tentativa 'PALCO'): {info['round_status']}")

        print(f"Ana tenta '{palavra_secreta_r1}'...")
        info_vitoria = game.process_attempt(palavra_secreta_r1)
        
        if info_vitoria.get("error"):
             print(f"Erro na tentativa: {info_vitoria['error']}")
        else:
            print(f"Resultado da Rodada 1 (tentativa de vitória): {info_vitoria['round_status']}")
            print(f"Placar: {info_vitoria['current_scores']}")
            print(f"Status Geral: {info_vitoria['geral_status']}")
        
        print(f"\nRodada {game.played_rounds} de {game.total_rounds}")
        print(f"Jogador da vez: {game.get_current_player_name()}")
        
        print("Beto joga 6x 'PALCO' (simulando derrota)...")
        info_final_rodada = {}
        for _ in range(6):
            info_final_rodada = game.process_attempt("PALCO")
            if info_final_rodada.get("error"):
                break
            if info_final_rodada["round_status"] != ROUND_STATUS["PLAYING"]:
                break

        print(f"Resultado da Rodada 2: {info_final_rodada.get('round_status', 'ERRO')}")
        print(f"Placar: {info_final_rodada.get('current_scores', 'ERRO')}")
        print(f"Status Geral: {info_final_rodada.get('geral_status', 'ERRO')}")
        
        resultado_final = game.get_final_result()
        print(f"Resultado Final: {resultado_final}")
        
        print("\n--- Testes do GameManager concluídos ---")
        
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)