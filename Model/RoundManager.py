from Model.Constants import *


class RoundManager:
    secret_word: list
    max_attempts: int
    remaining_attempts: int
    round_status: str
    results_history: list

    def __init__(self, secret_word: str, attempts_amount: int):
        self.secret_word = list(secret_word.upper())
        self.max_attempts = attempts_amount
        self.remaining_attempts = attempts_amount
        self.results_history = []
        self.round_status = ROUND_STATUS["PLAYING"]

    def send_attempt(self, attempt_word: str) -> list:
        if self.round_status != ROUND_STATUS["PLAYING"]:
            return []

        self.remaining_attempts -= 1

        attempts_list: list = list(attempt_word.upper())
        result: list = self._calculate_result(attempts_list)
        self.results_history.append(result)

        if attempts_list == self.secret_word:
            self.round_status = ROUND_STATUS["WIN"]
        elif self.remaining_attempts == 0:
            self.round_status = ROUND_STATUS["LOSE"]

        return result

    def get_status(self) -> str:
        return self.round_status

    def get_points(self) -> int:
        if self.round_status == ROUND_STATUS["WIN"]:
            attempts_used: int = self.max_attempts - self.remaining_attempts

            point_mapping: dict[int, int] = {1: 120, 2: 100, 3: 80, 4: 60, 5: 40, 6: 20}

            return point_mapping.get(attempts_used, 0)

        return 0

    def _calculate_result(self, attempt_list: list) -> list:
        secret_temp: list = list(self.secret_word)

        parcial_result: list = [(letter, None) for letter in attempt_list]

        for i in range(len(self.secret_word)):
            if attempt_list[i] == secret_temp[i]:
                parcial_result[i] = (attempt_list[i], LETTER_STATUS["CORRECT"])
                secret_temp[i] = None

        for j in range(len(self.secret_word)):
            if parcial_result[j][1] is None:
                attempt_letter: str = attempt_list[j]

                if attempt_letter in secret_temp:
                    parcial_result[j] = (attempt_letter, LETTER_STATUS["WRONG_PLACE"])
                    secret_temp[secret_temp.index(attempt_letter)] = None
                else:
                    parcial_result[j] = (attempt_letter, LETTER_STATUS["WRONG"])

        return parcial_result


if __name__ == "__main__":
    print("\n--- Testando RoundManager ---")

    palavra_secreta_teste = "TESTE"
    rodada = RoundManager(palavra_secreta_teste, 6)

    print(f"Palavra secreta: {palavra_secreta_teste}")

    tentativa_1 = "PALCO"
    resultado_1 = rodada.send_attempt(tentativa_1)
    print(f"Tentativa 1 ('{tentativa_1}'): {resultado_1}")
    print(f"Status: {rodada.get_status()}, Restantes: {rodada.remaining_attempts}")

    tentativa_2 = "TENTE"
    resultado_2 = rodada.send_attempt(tentativa_2)
    print(f"Tentativa 2 ('{tentativa_2}'): {resultado_2}")
    print(f"Status: {rodada.get_status()}, Restantes: {rodada.remaining_attempts}")

    rodada_letras_repetidas = RoundManager("CASAS", 6)
    tentativa_3 = "AMAIS"
    resultado_3 = rodada_letras_repetidas.send_attempt(tentativa_3)
    print(f"\nTeste Repetidas (Secreta 'CASAS', Tentativa '{tentativa_3}'): {resultado_3}")

    tentativa_4 = "TESTE"
    resultado_4 = rodada.send_attempt(tentativa_4)
    print(f"\nTentativa 3 ('{tentativa_4}'): {resultado_4}")
    print(f"Status: {rodada.get_status()}, Restantes: {rodada.remaining_attempts}")
    print(f"Pontuação: {rodada.get_points()}")

    tentativa_5 = "FINAL"
    resultado_5 = rodada.send_attempt(tentativa_5)
    print(f"\nTentativa 4 ('{tentativa_5}' após fim): {resultado_5}")
    print(f"Status: {rodada.get_status()}, Restantes: {rodada.remaining_attempts}")

    rodada_derrota = RoundManager("FORCA", 6)
    rodada_derrota.send_attempt("AAAAA")
    rodada_derrota.send_attempt("BBBBB")
    rodada_derrota.send_attempt("CCCCC")
    rodada_derrota.send_attempt("DDDDD")
    rodada_derrota.send_attempt("EEEEE")
    print("\nTeste de Derrota (Secreta 'FORCA')")
    print(f"Restantes antes da última: {rodada_derrota.remaining_attempts}")
    resultado_6 = rodada_derrota.send_attempt("GGGGG")
    print(f"Tentativa 6 ('GGGGG'): {resultado_6}")
    print(f"Status: {rodada_derrota.get_status()}, Restantes: {rodada_derrota.remaining_attempts}")
    print(f"Pontuação: {rodada_derrota.get_points()}")
