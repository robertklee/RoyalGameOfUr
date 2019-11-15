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
        # rolling 4 dice, each with either 0 or 1 value, results in
        # mean of 4*0.5 and variance of 4*0.25
        normal = np.round(np.random.normal(2,1,1))[0]
        if normal < 0:
            normal = 0
        
        if normal > 4:
            normal = 4
        
        self.roll = normal
    
    def moveExists(self):
        '''
        Returns true if move exists returns false if no move exists
        '''
        # Check if any piece can move off the board
        if len(self.piecePositions) > 0 and max(self.piecePositions) + self.roll >= 14:
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
                    if selectedLocationTranslated in player.piecePositions or \
                        (selectedLocationTranslated == Player.benchPosition and player.benchSize > 0):
                        player.selectedPiece = selectedLocationTranslated
                elif (selectedLocationTranslated == player.selectedPiece):
                    player.selectedPiece = None
                else:
                    # If they have already selected something. check if the move they are requesting is valid
                    pieceMoveSuccessful = False

                    if (player.selectedPiece == selectedLocationTranslated - player.roll or \
                        (selectedLocationTranslated >= Player.endPosition and player.selectedPiece + player.roll >= Player.endPosition)):
                        # location is valid distance from selected piece or moves off board
                        if (Player.contestedPositionStart <= selectedLocationTranslated <= Player.contestedPositionEnd and \
                            selectedLocationTranslated in opponent.piecePositions):
                            # if selected location is on opponent piece, move that piece to their bench
                            opponent.piecePositions.remove(selectedLocationTranslated)
                            opponent.benchSize += 1
                            
                            pieceMoveSuccessful = True
                        elif (selectedLocationTranslated not in player.piecePositions):
                            # piece will not overlap with existing piece except when piece moves off board
                            pieceMoveSuccessful = True
                    
                    if pieceMoveSuccessful:
                        # if the piece was successfully moved
                        if player.selectedPiece == Player.benchPosition:
                            # moved from bench
                            player.benchSize -= 1
                        else: 
                            # moved from previous location
                            player.piecePositions.remove(player.selectedPiece)
                        
                        if (selectedLocationTranslated < Player.endPosition):
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
                self.nextPlayerToPlay = opponent.role
                opponent.updateRoll()
                
        # self.printPlayerStates("HANDLE CLICK END")
        return self.render(player.role)

    def render(self, playerRole):
        '''
        player view = {
            'gameState' = [array of 24 strings to show in board state],
            'status'    = string showing their game connection/turn/win status,
            'rollValue'  = int [0-4] their roll value,
            'youWon'     = bool if they have won,
            'gameOver'   = bool if game over,   
        }
        '''
        # print("render: " + str(playerRole))
        boardState = []
        for _ in range(24):
            boardState.append("")

        message = ''

        yourTurn = self.nextPlayerToPlay == playerRole
        gameOver = self.gameCompleted

        gameConnected = self.player1.id != None

        youWon = False
        if (gameOver):
            youWon = playerRole == self.winningPlayer
            message = "Congratulations! You won!" if youWon else "Game over!"
        elif gameConnected:
            message = "It's Your Turn!" if yourTurn else "Opponent's Turn!"
        else:
            message = "Waiting for opponent..."
        
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
            'message'  : message,
            'rollValue' : rollValue,
            'youWon'    : youWon,
            'gameOver'  : gameOver,
        }

        return returnValue