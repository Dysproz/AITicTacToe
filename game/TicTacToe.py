'''
Engine for TicTacToe game.
TicTacToe object expects on creation 2 Player clases - you should find these classes in QLearningPlayers.py script.
By default player1 is X and player2 is O.

Author: Szymon Krasuski
May 2018
'''


import numpy as np

class TicTacToe(object):
    letters2numbers = {'a' : 0, 'b': 1, 'c':2} #Little dictionary to easily decode standard notation

    #Constructor for our class
    def __init__(self, player1, player2):

        #Assign passed players' classes to global class variables
        self.player1 = player1
        self.player2 = player2
        self.newGame() #Start new game

    #Method for performing one move. While it's AI Player turn, it automatically asks for move and returns reward.
    def play(self):
        #When 2 AIs are playing we wont to restart game imediately every time it's finished
        if self.isGameFinished() and not (self.player1.getType() is "h" or self.player2.getType() is "h"):
            self.newGame()

        mv = None
        #If it's X's turn and it's AI
        if self.token == 1 and (self.player1.getType() != "h"):
            mv = self.player1.move(self.getBoard()) #Get move from AI
            #Check whether AI is right and it's possible to perform that move and if yes then make that move
            if self.isMoveValid(mv):
                self.makeMove(mv, self.player1.figure)
            #Give AI reward
            self.player1.rewarded(self.winner, self.isMoveValid(mv), self.getBoard())

        #When it's AI and it's O turn
        elif self.token == -1 and (self.player2.getType() != "h"):
            mv = self.player2.move(self.getBoard()) #Get move form AI
            #Check whether move is valid and if yes then make that move
            if self.isMoveValid(mv):
                self.makeMove(mv, self.player2.figure)
            #Give AI a reward
            self.player2.rewarded(self.winner, self.isMoveValid(mv), self.getBoard())
        else:
            pass

    #Method for starting new game
    def newGame(self):
        self.board = np.zeros([3,3]) #We begin with 3x3 matrix of zeros
        self.token = 1 #X starts
        self.winner = 0 #Nobody's winner
        #Send players signal that it''s new game
        self.player1.begginNewGame()
        self.player2.begginNewGame()

    #Method returns who won (0-the game is on, 0.5 - it's a tie, 1-X won, -1 - O won)
    def whoseTurn(self):
        return self.token

    #Method for performing move (with additional check)
    def makeMove(self, move, player):
        #Make move only when the gae is on
        if not self.isGameFinished():
            #If it's turn of a player that wants to make that move
            if player == self.token:
                #If there's a place for new figure
                if self.board[int(self.letters2numbers[move[0]]),int(move[1])-1] == 0:
                    self.__move__(move) #put figure on this field

    #Method for checking whether passed move is valid
    def isMoveValid(self, move):
        #Just check if specific field is empty
        if self.board[int(self.letters2numbers[move[0]]),int(move[1])-1] == 0 and not self.isGameFinished():
            return True
        else:
            return False

    #Method for changing players' classes during the game
    def changePlayers(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    #Method returns current board
    def getBoard(self):
        return self.board

    #Mehod search for winning situation and returns True/False
    def isGameFinished(self):
        if self.__searchForWin__() != 0:
            self.winner = self.__searchForWin__()
            return True
        else:
            return False

    #Performing actual move on board (use only via makeMove())
    def __move__(self, field):
        field = list(field) #Transformm field into list
        if self.token == 1:
            self.board[int(self.letters2numbers[field[0]]), int(field[1])-1] = 1 #Put X if it's X's turn
            self.token = -1 #Change turn to O
        else:
            self.board[int(self.letters2numbers[field[0]]), int(field[1])-1] = -1 #Put O if it's O's turn
            self.token = 1 #Change turn to X

    #Search for wining situation (returns 0 when the game is still on, 1 when X won, -1 when O won and 0.5 when it's a tie)
    def __searchForWin__(self):
        for i in range(0,3):
            #Search columns for 3X
            if np.sum(self.board[:,i]) == 3:
                return 1
            #Search rows for 3X
            if np.sum(self.board[i,:]) == 3:
                return 1
            #Search columns for 3O
            if np.sum(self.board[:,i]) == -3:
                return -1
            #Search rows for 3O
            if np.sum(self.board[i,:]) == -3:
                return -1
        #Search trace for 3X
        if np.trace(self.board) == 3:
            return 1
        #Search trace for 3O
        if np.trace(self.board) == -3:
            return -1
        #Search off diagonal for 3X
        if self.board[2,0]+self.board[1,1]+self.board[0,2] == 3:
            return 1
        #Search off diagonal for 3O
        if self.board[2,0]+self.board[1,1]+self.board[0,2] == -3:
            return -1

        #In case of tie return 0.5
        if not 0 in self.board:
            return 0.5

        return 0
