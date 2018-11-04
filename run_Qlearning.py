'''
This is a demo script of QLearning algorithm  playing TicTacToe.

In  the first part we put  AI Players agaist each other to teach them play.
In the second part we swap one AI Player to Human
that can play with trained AI Player via GUI.

Author: Szymon Krasuski
May 2018

'''

from game.QLearningPlayers import *
from game.GameGUI import *
from game.TicTacToe import *
from tkinter import *
import threading

def refreshGUI(threader):
        try:
            threader.game.updateImages()
        except:
            pass

x = AIPlayer()
o = AIPlayer(figure=-1)
human = Player(figure=-1)
game = TicTacToe(x, o)

learning_cycles = 20000

for i in range(0, learning_cycles*2):
    game.play()
    print("Learning... Move %i out of %i" % (int(i/2)+1, learning_cycles))

game.changePlayers(x, human)
game.newGame()
app = Game(gameEngine=game)

while 1:
    game.play()
    refreshGUI(app)
    if not app.isAlive():
        break

print("I'm still alive!")
