class Game():
    def __init__(self, player1):
        self.boardState = []
        self.initalizeBoard()
        self.player_one_IP = str(player1)
    
    def addSecondPlayer(self, player2):
        self.player_two_IP = str(player2)

    def initalizeBoard(self):
        pass
