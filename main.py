from Model.GameManager import GameManager
from View.MainView import MainView
from Controller.GameController import GameController

if __name__ == "__main__":
    path_words : str = "words.txt"
    
    model : GameManager = GameManager(path_words)
    view : MainView = MainView("Desenlance")
    controller : GameController = GameController(model, view)
    
    controller.run()