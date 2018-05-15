import numpy as np

class TicTacToe:
    letters2numbers = {'a' : 0, 'b': 1, 'c':2}

    def __init__(self):
        self.newGame()


    def newGame(self):
        self.board = np.zeros([3,3])
        self.token = 1
        self.winner = 0

    def whoseTurn(self):
        return self.token

    def makeMove(self, move, player):
        if not self.isGameFinished():
            if player == self.token:
                if self.board[int(self.letters2numbers[move[0]]),int(move[1])-1] == 0:
                    self.__move__(move)

    def isMoveValid(self, move):
        if self.board[int(self.letters2numbers[move[0]]),int(move[1])-1] == 0 and not self.isGameFinished():
            return True
        else:
            return False

    def getBoard(self):
        return self.board

    def isGameFinished(self):
        if self.__searchForWin__() != 0:
            self.winner = self.__searchForWin__()
            return True
        else:
            return False


    def __move__(self, field):
        field = list(field)
        if self.token == 1:
            self.board[int(self.letters2numbers[field[0]]), int(field[1])-1] = 1
            self.token = -1
        else:
            self.board[int(self.letters2numbers[field[0]]), int(field[1])-1] = -1
            self.token = 1

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

        return 0
