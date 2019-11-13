import numpy as np
from random import randint

class Game():
    def __init__(self, player0Ip):
        self.nextPlayerToPlay = 0

        # Initalize the off board bench sizes
        self.player0BenchSize = 5 
        self.player1BenchSize = 5 

        # Intialize board data
        self.player0PiecesPositions = []
        self.player1PiecesPositions = []
        '''
        Each player has it's piece postions as relative to its own bench/ exit

        [ 4][ 5][ 6][ 7][ 8][ 9][10][11]
        [ 3][ 2][ 1][ 0][15][14][13][12]
        '''
        self.playerConversion = {
            8:4,
            9:5,
            10:6,
            11:7,
            12:8,
            13:9,
            14:10,
            15:11,
            16:3,
            17:2,
            18:1,
            19:0,
            20:15,
            21:14,
            22:13,
            23:12,
        }
        self.doubleRollSpaces = [13, 7, 3]

        self.player0Ip = player0Ip
        self.player1Ip = None
        self.player0Roll = randint(0,4)
        self.player1Roll = randint(0,4)
        self.playerSelection = None

        self.player0Won = False
        self.player1Won = False

    def handelClick(self, ip, position):
        '''
        TODO handel double turns
        '''
        # Handel second player joining
        if self.player1Ip == None and self.player0Ip != ip:
            self.player1Ip = ip
            return self.render(1)
        # Handel wrong person attempting to join game
        if self.player1Ip != None and self.player1Ip != ip and self.player0Ip != ip:
            return self.render(0) # Just return a render of the game from player 0's perspective
        #
        # Handel player 0 making a click
        if ip == self.player0Ip:
            # Check if it is their turn and check if it is a valid move
            if self.nextPlayerToPlay == 0 and position in self.playerConversion.keys(): 
            # Check if they already have something selected or if they are trying to select something
                if self.playerSelection == None:
                    # If they are trying to select something check if they have clicked on something valid
                    if self.playerConversion[position] in self.player0PiecesPositions or self.playerConversion[position] == 15:
                        self.playerSelection = self.playerConversion[position]
                    return self.render(0)
                else:
                    # If they have already selected something check if the move they are requesting is valid
                    if self.playerConversion[position] == 14 and self.playerConversion[position] - self.player0Roll <= self.playerSelection: # They are moving a piece off the board 
                        self.player0PiecesPositions.remove(self.playerSelection) # Remove that piece from the board
                        # Check for win condition
                        if len(self.player0PiecesPositions) == 0  and self.player0BenchSize == 0: 
                            self.player0won = True
                        self.player0Roll = randint(0,4)
                        return self.render(0)
                    elif self.playerConversion[position] - self.player0Roll == self.playerSelection and not self.playerConversion[position] in self.player0PiecesPositions:
                        if self.playerSelection == 15: # They are moving someone from their bench
                            self.player0BenchSize -= 1
                        else:
                            self.player0PiecesPositions.remove(self.playerSelection) # They are moving an already existing piece on the board remove the old piece position
                        if self.playerConversion[position] in self.player1PiecesPositions: # If the new piece position in the other players positions remove the board and add it to the other players bench
                            self.player1PiecesPositions.remove(self.playerConversion[position])
                            self.player1BenchSize+=1
                        self.player0PiecesPositions.append(self.playerConversion[position]) # Add the new position of the piece
                        if self.playerConversion[position] not in self.doubleRollSpaces: # They have moved a piece onto a second turn postion
                            self.nextPlayerToPlay = 1
                        self.player0Roll = randint(0,4)
                        return self.render(0)
                    else:
                        self.playerSelection = None
                        return self.render(0)
            else:
                return self.render(0) # If it is not their turn return their board state nothing else

        return self.render(0)

        # Handel player 1 making a click
        if ip == self.player1Ip:
            # Check if it is their turn and check if it is a valid move
            if self.nextPlayerToPlay == 1 and position in self.playerConversion.keys(): 
            # Check if they already have something selected or if they are trying to select something
                if self.playerSelection == None:
                    # If they are trying to select something check if they have clicked on something valid
                    if self.playerConversion[position] in self.player1PiecesPositions or self.playerConversion[position] == 15:
                        self.playerSelection = self.playerConversion[position]
                    return self.render(1)
                else:
                    # If they have already selected something check if the move they are requesting is valid
                    if self.playerConversion[position] == 14 and self.playerConversion[position] - self.player1Roll <= self.playerSelection: # They are moving a piece off the board 
                        self.player1PiecesPositions.remove(self.playerSelection) # Remove that piece from the board
                        # Check for win condition
                        if len(self.player1PiecesPositions) == 0  and self.player1BenchSize == 0: 
                            self.player1won = True
                        self.player1Roll = randint(0,4)
                        return self.render(1)
                    elif self.playerConversion[position] - self.player1Roll == self.playerSelection and not self.playerConversion[position] in self.player1PiecesPositions:
                        if self.playerSelection == 15: # They are moving someone from their bench
                            self.player1BenchSize -= 1
                        else:
                            self.player1PiecesPositions.remove(self.playerSelection) # They are moving an already existing piece on the board remove the old piece position
                        if self.playerConversion[position] in self.player1PiecesPositions: # If the new piece position in the other players positions remove the board and add it to the other players bench
                            self.player1PiecesPositions.remove(self.playerConversion[position])
                            self.player1BenchSize+=1
                        self.player1PiecesPositions.append(self.playerConversion[position]) # Add the new position of the piece
                        if self.playerConversion[position] not in self.doubleRollSpaces: # They have moved a piece onto a second turn postion
                            self.nextPlayerToPlay = 1
                        self.player1Roll = randint(0,4)
                        return self.render(1)
                    else:
                        self.playerSelection = None
                        return self.render(1)
            else:
                return self.render(-1) # If it is not their turn return their board state nothing else


    def render(self, player):
        '''
        player view = {
            'gameState' = [array of 24 strings to show in board state],
            'yourTurn'   = bool if it is their turn,
            'rollValue'  = int [0-4] their roll value,
            'youWon'     = bool if they have won,
            'gameOver'   = bool if game over,   
        }
        '''
        boardState = []
        for _ in range(24):
            boardState.append("")

        yourTurn = self.nextPlayerToPlay == player
        youWon = False
        if player == 0:
            youWon = self.player0Won == True
        else:
            youWon = self.player0Won == True


        gameOver = self.player0Won == True or self.player1Won == True
        rollValue = None

        if player == 0:
            rollValue = self.player0Roll
            pass
        elif player == 1:
            rollValue = self.player1Roll
            pass

        convertPlayerOff = {
            0 :3,
            1 :2,
            2 :1,
            3 :0,
            4 :8,
            5 :9,
            6 :10,
            7 :11,
            9 :12,
            10:13,
            11:14,
            12:15,
            13:7,
            14:6
        }
        convertPlayerMain = {
            0 :19,
            1 :18,
            2 :17,
            3 :16,
            4 :8,
            5 :9,
            6 :10,
            7 :11,
            9 :12,
            10:13,
            11:14,
            12:15,
            13:23,
            14:22
        }

        for value in self.player1PiecesPositions:
            if player == 1:
                boardState[convertPlayerMain[value]] = "O"
            else:
                boardState[convertPlayerOff[value]] = "O"

        for value in self.player0PiecesPositions:
            if player == 0:
                boardState[convertPlayerMain[value]] = "X"
            else:
                boardState[convertPlayerOff[value]] = "X"

        if player == 0:
            boardState[20] = str(self.player0BenchSize)
            boardState[4]  = str(self.player1BenchSize)
        else:
            boardState[4] = str(self.player0BenchSize)
            boardState[20]  = str(self.player1BenchSize) 

        print(self.playerSelection)
        if yourTurn and print(self.playerSelection) != None:    
            print(convertPlayerMain[self.playerSelection])
            boardState[convertPlayerMain[self.playerSelection]] = "[" + boardState[convertPlayerMain[self.playerSelection]] + "]"



        returnValue = {
            'gameState' : boardState,
            'yourTurn'  : yourTurn,
            'rollValue' : rollValue,
            'youWon'    : youWon,
            'gameOver'  : gameOver,
        }

        return returnValue