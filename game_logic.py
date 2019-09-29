import numpy as np
from random import randint

class Game():
    def __init__(self, player0Ip):
        self.nextPlayerToPlay = 0

        # Initalize the off board bench sizes
        self.player0BenchSize = 5 
        self.player1BenchSize = 5 

        # Intialize board data
        self.player0PiecesPostions = []
        self.player1PiecePositions = []
        '''
        Each player has it's piece postions as relative to its own bench/ exit

        [ 4][ 5][ 6][ 7][ 8][ 9][10][11]
        [ 3][ 2][ 1][ 0][15][14][13][12]
        '''
        self.playerConversion = {
            19:0,
            18:1,
            17:2,
            16:3,
            8:4,
            9:5,
            10:6,
            11:7,
            12:8,
            13:9,
            14:10,
            15:11,
            23:12,
            22:13,
            21:14,
            20:15,
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
            return self.player1View()
        # Handel wrong person attempting to join game
        if self.player1Ip != None and self.player1Ip != ip and self.player0Ip != ip:
            return self.render(0)
        # Handel player 1 making a click
        if ip == self.player0Ip:
            # Check if it is their turn
                if self.nextPlayerToPlay == 0:
                # Check if they already have something selected or if they are trying to select something
                    if self.playerSelection == None:
                        # If they are trying to select something check if they have clicked on something valid
                        if position in self.playerConversion.keys() and self.playerConversion[position] in self.player0PiecesPostions:
                            self.playerSelection = self.playerConversion[position]
                            return self.render(0)
                    else:
                        # If they have already selected something check if the move they are requesting is valid
                        if self.playerConversion[position] == 14 and self.playerConversion[position] - self.player0Roll <= self.playerSelection: # They are moving a piece off the board 
                            self.player0PiecesPostions.remove(self.playerSelection) # Remove that piece from the board
                            if len(self.player0PiecesPostions) == 0  and self.player0BenchSize == 0:
                                self.player0won = True
                            self.player0Roll = randint(0,4)
                            return self.render(0)
                        if self.playerConversion[position] - self.player0Roll == self.playerSelection and not self.playerConversion[position] in self.player0PiecesPostions:
                            if self.playerSelection == 15: # They are moving someone from their bench
                                self.player0BenchSize -= 1
                                self.player0PiecesPostions.append(self.playerConversion[position])
                                if self.playerConversion[position] not in self.doubleRollSpaces:
                                    self.nextPlayerToPlay = 1
                                self.player0Roll = randint(0,4)
                                return self.render(0)

                            # If the move they are making is valid make the move and whitch the player to play

                            # If the move they are making is invalid clear their selection return old board state 

        # Handel player 2 making a click


    def render(self, player):
        return None
