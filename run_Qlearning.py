'''
This is a demo script of QLearning algorithm  playing TicTacToe.

In  the first part we put  AI Players agaist each other to teach them play.
In the second part we swap one AI Player to Human that can play with trained AI Player via GUI.

Author: Szymon Krasuski
May 2018

'''

from game.QLearningPlayers import *
from game.GameGUI import *
from game.TicTacToe import *
from tkinter import *
import threading

#Define function for refreshing GUI after every move
def refreshGUI(threader):
        try:
            threader.game.updateImages()
        except:
            pass

#Create 3 exmple players
x = AIPlayer() #AI Player as X
o = AIPlayer(figure=-1) #AI Player as O
human = Player(figure=-1) #Human player as O (for further tests)
#Create game
game = TicTacToe(x,o)

#Define number of cycles that AI Players should play with each other
learning_cycles = 20000

#Run learning_cycles cycles of AI playing wiith AI
for i in range(0,learning_cycles*2):
    game.play()
    print("Learning... Move %i out of %i"%(int(i/2)+1, learning_cycles))

#Change players - now AI will play with human
game.changePlayers(x,human)
game.newGame()
#Create GUI connected with existing TicTacToe engine
app = Game(gameEngine=game)

#Infinite play with AI
while 1:
    game.play()
    refreshGUI(app)
    #In case our GUI will crash
    if not app.isAlive():
        break

print("I'm still alive!")
