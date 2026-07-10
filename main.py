import os
import sys
from Controller.GameController import GameController
from Model.GameManager import GameManager
from View.MainView import MainView


def get_resource_path(relative_path: str) -> str:
    """Retorna o caminho absoluto do recurso, suportando execução local e empacotamento PyInstaller."""
    try:
        # O PyInstaller cria uma pasta temporária e salva o caminho em sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    path_words: str = get_resource_path("words.txt")

    model: GameManager = GameManager(path_words)
    view: MainView = MainView("Desenlance")
    controller: GameController = GameController(model, view)

    controller.run()
