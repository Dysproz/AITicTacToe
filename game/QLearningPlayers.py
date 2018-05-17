'''
Two classes for TicTacToe players.
Player - it's a dummy class for human player that'll use GUI.
AIPlayer - it's a QLearning algorithm that learns to play by itself.

Author: Szymon Krasuski
May 2018
'''

import numpy as np
import random

class Player:
    def __init__(self, figure='X'):
        self.type = 'h' #Define its type to human
        #Set it's figure
        if figure == 'X' or figure == 1:
            self.figure = 1
        else:
            self.figure = -1

    def move(self, board):
        pass

    def rewarded(self, reward, valid, board):
        pass

    def begginNewGame(self):
        pass

    def getType(self):
        return self.type



class AIPlayer:

    def __init__(self, eps=0.2, alpha=0.2, gamma=0.9, figure='X'):
        self.type = 'ai' #Set its type to AI
        self.Q = {} #Declare Q
        #Declare input values
        self.epsilon = eps
        self.alpha = alpha
        self.gamma = gamma
        #Set initial reward value to 0
        self.reward = 0
        #Set proper figure
        if figure == 'X' or figure == 1:
            self.figure = 1
        else:
            self.figure = -1

    #Reset inner board and last move
    def begginNewGame(self):
        self.lastBoard = np.zeros([3,3])
        self.lastMove = None

    #Get  move for specific board
    def move(self, board):
        no2mv = {1:'a1', 2:'a2', 3:'a3', 4:'b1', 5:'b2', 6:'b3', 7:'c1', 8:'c2', 9:'c3'} #Little dictionary to decode class notations into 'official' notation
        board = self.transformBoard(board) #Transform numpy aray into tuple that's easier to use
        self.lastBoard = board  #Set last board
        actions = self.__availableMoves__(board) #get all available actions

        #It's good to explore new possibilities from time to time
        if random.random() < self.epsilon:
            self.lastMove = random.choice(actions) #make random move
            return no2mv[self.lastMove]

        Qs = [self.getQ(self.lastBoard, action) for action in actions] #Count all Q for every possiblr action
        maxQ = max(Qs) #Find maximum

        #Define index of the best action
        if Qs.count(maxQ)>1:
            best = [i for i in range(len(actions)) if Qs[i] == maxQ]
            i = random.choice(best)
        else:
            i = Qs.index(maxQ)

        #choose the best action
        self.lastMove = actions[i]
        return no2mv[actions[i]]

    #Method for rewarding player judged on his move
    def rewarded(self, reward, valid, newBoard):
        newBoard = self.transformBoard(newBoard) #Transform board
        #If performed move was not valid then give player a punishment (-100 reward)
        if valid == False:
            self.reward = -100
        else:
            #If it's a tie, just give 0.5
            if reward == 0.5:
                self.reward = reward
            else:
                #Depending on playing figure give appropiate reward
                if self.figure == 1:
                    self.reward = reward
                else:
                    #For O it's reversed
                    self.reward = -reward
        #If there was a move (there's no move at the beggining of game) use it to learn
        if self.lastMove:
            self.learn(self.lastBoard, self.lastMove, self.reward, newBoard)


    #Method for learning based on performed moves
    def learn(self, board, action, reward, resultBoard):
        previous = self.getQ(board, action) #get previous Q
        maxQnew = max([self.getQ(resultBoard, a) for a in self.__availableMoves__(board)]) #count maximum new Q
        self.Q[(board, action)] = previous + self.alpha*((reward + self.gamma*maxQnew)-previous)

    #Returns current Q (if there's no, set it to 1)
    def getQ(self, board, action):
        if self.Q.get((board, action)) is None:
            self.Q[(board, action)] = 1.0
        return self.Q.get((board, action))

    #Tranorm numpy array into more convinient form
    def transformBoard(self,board):
        return (board[0,0],board[0,1],board[0,2],board[1,0],board[1,1],board[1,2],board[2,0],board[2,1],board[2,2])

    #Returns type of player ('ai')
    def getType(self):
        return self.type

    #Returns estimate of max reward
    def __countEstimate__(self,board):
        #When it's not possible to finish game
        if np.count_nonzero(board == 0)<5:
            return 0
        else:
            #Whe it's possible to finish game
            return 1

    #Find all possible moves
    def __availableMoves__(self, board):
        result = ()
        for i in range(0,len(board)):
            if board[i] == 0:
                result = result + (i+1,)

        return result
