import numpy as np
import random
from random import randint

startingBenchSize = 5
intialPlayer = 0
randintMin = 0
randintMax = 4

class Player():
    benchPosition = -1
    endPosition = 14
    contestedPositionStart = 4
    contestedPositionEnd = 11
    doubleRollSpaces = [13, 7, 3]
    '''
    Each player has it's piece postions as relative to its own bench/ exit

    [ 4][ 5][ 6][ 7][ 8][ 9][10][11]
    [ 3][ 2][ 1][ 0][-1][14][13][12]
    '''
    playerConversion = {
            8:contestedPositionStart,
            9:5,
            10:6,
            11:7,
            12:8,
            13:9,
            14:10,
            15:contestedPositionEnd,
            16:3,
            17:2,
            18:1,
            19:0,
            20:benchPosition, # off map
            21:endPosition, # end
            22:13,
            23:12,
        }
    
    convertOpponent = {
        0 :3,
        1 :2,
        2 :1,
        3 :0,
        4 :8,
        5 :9,
        6 :10,
        7 :11,
        8 :12,
        9 :13,
        10:14,
        11:15,
        12:7,
        13:6,
        endPosition:5,
        benchPosition:4
    }
    convertPlayer = {
        0 :19,
        1 :18,
        2 :17,
        3 :16,
        4 :8,
        5 :9,
        6 :10,
        7 :11,
        8 :12,
        9 :13,
        10:14,
        11:15,
        12:23,
        13:22,
        endPosition:21,
        benchPosition:20
    }
    validClickLocations = playerConversion.keys()
    def __init__(self, id, piecePositions, benchSize, roll, role, selectedPiece):
        self.id = id
        self.piecePositions = piecePositions # Intialize board data
        self.benchSize = benchSize # Initalize the off board bench sizes
        self.roll = roll
        self.role = role # Player 1's view is mirrored
        self.selectedPiece = selectedPiece

    def updateRoll(self):
        self.roll = randint(0, 1) + randint(0, 1) + randint(0, 1) + randint(0, 1)
    
    def moveExists(self):
        '''
        Returns true if move exists returns false if no move exists
        '''
        # Check if any piece can move off the board
        if max(self.piecePositions) + self.roll >= 14:
            return True 
        # Check if you can move a piece forward without hitting another piece 
        for pos in self.piecePositions:
            if pos + self.roll not in self.piecePositions:
                return True
        # check if you can move a piece off your bench
        if self.benchSize > 0 and self.roll + Player.benchPosition not in self.piecePositions:
            return True
        return False

class Game():
    def __init__(self, player0Id):
        self.nextPlayerToPlay = intialPlayer

        random.seed()

        self.player0 = Player(player0Id, [], startingBenchSize, -1, 0, None)
        self.player1 = Player(None, [], startingBenchSize, -1, 1, None)
        self.player0.updateRoll()
        self.player1.updateRoll()

        self.gameCompleted = False
        self.winningPlayer = -1

    def printPlayerStates(self, msg=''):
        print(msg)
        print("-----------------------\nPlayer 0: ")
        print("piecePositions: " + str(self.player0.piecePositions))
        print("benchSize: " + str(self.player0.benchSize))
        print("roll: " + str(self.player0.roll))
        print("selectedPiece: " + str(self.player0.selectedPiece) + "\n\n")
        
        print("Player 1: ")
        print("piecePositions: " + str(self.player1.piecePositions))
        print("benchSize: " + str(self.player1.benchSize))
        print("roll: " + str(self.player1.roll))
        print("selectedPiece: " + str(self.player1.selectedPiece) + "\n--------------------")
    
    def handleClick(self, id, position):
        # self.printPlayerStates("HANDLE CLICK START")

        # Handle second player joining
        if (self.player1.id == None):
            if id != self.player0.id:
                self.player1.id = id
                print("player 1 id set")
                return self.render(1)
            else:
                return self.render(0)
        # Handle wrong person attempting to join game
        elif (self.player1.id != id and self.player0.id != id):
            return self.render(0) # Just return a render of the game from player 0's perspective

        player = None
        opponent = None
        # determine which player clicked
        if (id == self.player0.id):
            player = self.player0
            opponent = self.player1
        elif (id == self.player1.id):
            player = self.player1
            opponent = self.player0
        else:
            # default to player 0 view if spectator
            return self.render(0)

        # check if it is their turn and check if it's a valid move
        if (self.nextPlayerToPlay == player.role and position in Player.validClickLocations):
            # Handle zero rolls
            if (player.roll != 0 and player.moveExists()):
                # Check if they already have something selected or if they are trying to select something
                selectedLocationTranslated = Player.playerConversion.get(position)

                # print("\n\nposition: " + str(position) + " selectedLocationTranslated: " + str(selectedLocationTranslated))

                assert selectedLocationTranslated != None

                if (player.selectedPiece == None):
                    # If they are trying to select something check if they have clicked on something valid
                    if selectedLocationTranslated in player.piecePositions or selectedLocationTranslated == Player.benchPosition:
                        player.selectedPiece = selectedLocationTranslated
                else:
                    # If they have already selected something. check if the move they are requesting is valid
                    pieceMoveSuccessful = False

                    if (player.selectedPiece == selectedLocationTranslated - player.roll):
                        # location is valid distance from selected piece
                        if (Player.contestedPositionStart <= selectedLocationTranslated <= Player.contestedPositionEnd and selectedLocationTranslated in opponent.piecePositions):
                            # if selected location is on opponent piece, move that piece to their bench
                            opponent.piecePositions.remove(selectedLocationTranslated)
                            opponent.benchSize += 1
                            
                            pieceMoveSuccessful = True
                        elif (selectedLocationTranslated not in player.piecePositions):
                            # piece will not overlap with existing piece
                            pieceMoveSuccessful = True
                    
                    if pieceMoveSuccessful:
                        # if the piece was successfully moved
                        if player.selectedPiece == Player.benchPosition:
                            # moved from bench
                            player.benchSize -= 1
                        else: 
                            # moved from previous location
                            player.piecePositions.remove(player.selectedPiece)
                        
                        player.piecePositions.append(selectedLocationTranslated)

                        if selectedLocationTranslated in Player.doubleRollSpaces:
                            # handle double roll locations
                            self.nextPlayerToPlay = player.role
                            player.updateRoll()
                        else:
                            # change player
                            self.nextPlayerToPlay = opponent.role
                            opponent.updateRoll()
                        
                        player.selectedPiece = None

                        if player.benchSize == 0 and len(player.piecePositions) == 0:
                            # handle win case
                            self.gameCompleted = True
                            self.winningPlayer = player.role
            else: 
                player.updateRoll()
                self.nextPlayerToPlay = opponent.role
                opponent.updateRoll()
                
        # self.printPlayerStates("HANDLE CLICK END")
        return self.render(player.role)
    '''
        # Handle player making a click
        if id == self.player0Id:
            # Check if it is their turn and check if it is a valid move
            if self.nextPlayerToPlay == 0 and position in self.playerConversion.keys(): 
                # Handle zero rolls
                if self.player0Roll != 0:
                    # Check if they already have something selected or if they are trying to select something
                    if self.playerSelection == None:
                        # If they are trying to select something check if they have clicked on something valid
                        if self.playerConversion[position] in self.player0PiecesPositions or self.playerConversion[position] == 15:
                            self.playerSelection = self.playerConversion[position]
                        return self.render(0)
                    else:
                        # If they have already selected something check if the move they are requesting is valid
                        if (self.playerSelection==15 and self.playerConversion[position] == self.player0Roll - 1) and not self.playerConversion[position] in self.player0PiecesPositions: # They are moving a piece off the board 
                            # Check for win condition
                            print("move Ok")
                            self.player0PiecesPositions.append(self.playerConversion[position])
                            self.player0BenchSize -= 1
                            if self.playerConversion[position] not in self.doubleRollSpaces:
                                self.nextPlayerToPlay = 1
                            if len(self.player0PiecesPositions) == 0  and self.player0BenchSize == 0: 
                                self.player0won = True
                            self.player0Roll = randint(0,4)
                            self.playerSelection = None
                            return self.render(0)
                        elif self.playerConversion[position] - self.player0Roll == self.playerSelection and not self.playerConversion[position] in self.player0PiecesPositions and self.playerConversion[position] < 14:
                            self.player0PiecesPositions.remove(self.playerSelection) # They are moving an already existing piece on the board remove the old piece position
                            if self.playerConversion[position] in self.player1PiecesPositions and self.playerConversion[position] in range(4,12): # If the new piece position in the other players positions remove the board and add it to the other players bench
                                self.player1PiecesPositions.remove(self.playerConversion[position])
                                self.player1BenchSize+=1
                            self.player0PiecesPositions.append(self.playerConversion[position]) # Add the new position of the piece
                            if self.playerConversion[position] not in self.doubleRollSpaces: # They have moved a piece onto a second turn postion
                                self.nextPlayerToPlay = 1
                            self.player0Roll = randint(0,4)
                            self.playerSelection = None
                            return self.render(0)
                        elif self.playerConversion[position] == 14 and self.playerSelection + self.player0Roll >= 14:
                            self.player0PiecesPositions.remove(self.playerSelection)
                            self.nextPlayerToPlay = 1
                            self.player0Roll = randint(0,4)
                            self.playerSelection = None
                            return self.render(0)
                        else:
                            self.playerSelection = None
                            return self.render(0)
                else:
                    self.nextPlayerToPlay = 1
                    self.player0Roll = randint(1,4)
                    return self.render(0)
            else:
                return self.render(0) # If it is not their turn return their board state nothing else

            return self.render(0)

        # Handle player 0 making a click
        if id == self.player1Id:
            # Check if it is their turn and check if it is a valid move
            if self.nextPlayerToPlay == 1 and position in self.playerConversion.keys(): 
                # Handle zero rolls
                if self.player1Roll != 0:
                    # Check if they already have something selected or if they are trying to select something
                    if self.playerSelection == None:
                        # If they are trying to select something check if they have clicked on something valid
                        if self.playerConversion[position] in self.player1PiecesPositions or self.playerConversion[position] == 15:
                            self.playerSelection = self.playerConversion[position]
                        return self.render(1)
                    else:
                        # If they have already selected something check if the move they are requesting is valid
                        if (self.playerSelection==15 and self.playerConversion[position] == self.player1Roll - 1) and not self.playerConversion[position] in self.player1PiecesPositions: # They are moving a piece off the board 
                            # Check for win condition
                            print("move Ok")
                            self.player1PiecesPositions.append(self.playerConversion[position])
                            self.player1BenchSize -= 1
                            if self.playerConversion[position] not in self.doubleRollSpaces:
                                self.nextPlayerToPlay = 0
                            if len(self.player1PiecesPositions) == 0  and self.player1BenchSize == 0: 
                                self.player1won = True
                            self.player1Roll = randint(0,4)
                            self.playerSelection = None
                            return self.render(1)
                        elif self.playerConversion[position] - self.player1Roll == self.playerSelection and not self.playerConversion[position] in self.player1PiecesPositions and self.playerConversion[position] < 14:
                            self.player1PiecesPositions.remove(self.playerSelection) # They are moving an already existing piece on the board remove the old piece position
                            if self.playerConversion[position] in self.player0PiecesPositions and self.playerConversion[position] in range(4,12): # If the new piece position in the other players positions remove the board and add it to the other players bench
                                self.player0PiecesPositions.remove(self.playerConversion[position])
                                self.player0BenchSize+=1
                            self.player1PiecesPositions.append(self.playerConversion[position]) # Add the new position of the piece
                            if self.playerConversion[position] not in self.doubleRollSpaces: # They have moved a piece onto a second turn postion
                                self.nextPlayerToPlay = 0
                            self.player1Roll = randint(0,4)
                            self.playerSelection = None
                            return self.render(1)
                        elif self.playerConversion[position] == 14 and self.playerSelection + self.player1Roll >= 14:
                            self.player1PiecesPositions.remove(self.playerSelection)
                            self.nextPlayerToPlay = 0
                            self.player1Roll = randint(0,4)
                            self.playerSelection = None
                            return self.render(1)
                        else:
                            self.playerSelection = None
                            return self.render(1)
                else:
                    self.nextPlayerToPlay = 0
                    self.player1Roll = randint(0,4)
                    return self.render(1)
            else:
                return self.render(1) # If it is not their turn return their board state nothing else

            return self.render(1)
        '''

    def render(self, playerRole):
        '''
        player view = {
            'gameState' = [array of 24 strings to show in board state],
            'yourTurn'   = bool if it is their turn,
            'rollValue'  = int [0-4] their roll value,
            'youWon'     = bool if they have won,
            'gameOver'   = bool if game over,   
        }
        '''
        # print("render: " + str(playerRole))
        boardState = []
        for _ in range(24):
            boardState.append("")

        yourTurn = self.nextPlayerToPlay == playerRole

        gameOver = self.gameCompleted

        youWon = False
        if (gameOver):
            youWon = playerRole == self.winningPlayer
        
        player = None
        opponent = None
        # determine which player clicked
        if (playerRole == self.player0.role):
            player = self.player0
            opponent = self.player1
        elif (playerRole == self.player1.role):
            player = self.player1
            opponent = self.player0
        
        rollValue = player.roll

        for value in player.piecePositions:
            boardState[Player.convertPlayer.get(value)] = "X"
        
        for value in opponent.piecePositions:
            boardState[Player.convertOpponent.get(value)] = "O"
        
        boardState[Player.convertPlayer.get(Player.benchPosition)] = str(player.benchSize)
        boardState[Player.convertOpponent.get(Player.benchPosition)] = str(opponent.benchSize)

        if (yourTurn and player.selectedPiece != None):
            boardState[Player.convertPlayer.get(player.selectedPiece)] = "[" + boardState[Player.convertPlayer.get(player.selectedPiece)] + "]"

        returnValue = {
            'gameState' : boardState,
            'yourTurn'  : "It's Your Turn!" if yourTurn else "Opponent's Turn!",
            'rollValue' : rollValue,
            'youWon'    : youWon,
            'gameOver'  : gameOver,
        }

        return returnValue