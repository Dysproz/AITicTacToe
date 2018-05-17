'''
Simple TicTacToe GUI
Click New Game for new game
Click where you want to put your figure and put it :)

Author: Szymon Krasuski
May 2018
'''


from tkinter import *
from game.TicTacToe import *
from PIL import ImageTk,Image
from tkinter import messagebox
import threading

#Class for handling GUI in other thread
class Game(threading.Thread):
    def __init__(self, x=None, o=None, gameEngine=None):

        self.x = x
        self.o = o
        self.gameEngine = gameEngine
        threading.Thread.__init__(self)
        self.start()
        self.game = None



    def run(self):
        self.root = Tk()
        self.root.wm_title("AI TicTacToe by Szymon Krasuski")

        self.game = GameGUI(self.x,self.o, master=self.root, engine=self.gameEngine)
        self.game.mainloop()


#Actual GUI in tkinter
class GameGUI(Frame):

    def __init__(self, player1=None, player2=None, master=None, engine=None):
        #Assign engine
        if engine is None:
            self.tc=TicTacToe(player1, player2)
        else:
            self.tc = engine

        #Open images for GUI
        self.bg_image = ImageTk.PhotoImage(Image.open('game/graphics/background.png'))
        self.x_image = ImageTk.PhotoImage(Image.open('game/graphics/x.png'))
        self.o_image = ImageTk.PhotoImage(Image.open('game/graphics/o.png'))
        self.empty_image = ImageTk.PhotoImage(Image.open('game/graphics/empty.png'))
        #Configure GUI
        master.minsize(width=self.bg_image.width(), height=self.bg_image.height())
        super().__init__(master)

        self.pack()
        #set background
        label1 = Label(master, image=self.bg_image)
        label1.pack()
        self.create_widgets()




    #Create all elements
    def create_widgets(self):

        #Create button for new game
        self.new = Button(master=None, text="New Game", width=50, height=3, background="#B0E0E6", command= lambda: self.newGame())
        self.new.place(x=100, y=30)

        #Create clickable labels for every field
        self.a1 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.a1.bind("<Button-1>", self.a1Click)
        self.a1.place(x=100, y=106)

        self.a2 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.a2.bind("<Button-1>", self.a2Click)
        self.a2.place(x=100+132, y=106)

        self.a3 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.a3.bind("<Button-1>", self.a3Click)
        self.a3.place(x=100+132+132, y=106)


        self.b1 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.b1.bind("<Button-1>", self.b1Click)
        self.b1.place(x=100, y=106+132)


        self.b2 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.b2.bind("<Button-1>", self.b2Click)
        self.b2.place(x=100+132, y=106+132)


        self.b3 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.b3.bind("<Button-1>", self.b3Click)
        self.b3.place(x=100+132+132, y=106+132)


        self.c1 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.c1.bind("<Button-1>", self.c1Click)
        self.c1.place(x=100, y=106+132+132)


        self.c2 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.c2.bind("<Button-1>", self.c2Click)
        self.c2.place(x=100+132, y=106+132+132)


        self.c3 = Label(master=None, width=128, height=128,bd=0, image=self.empty_image)
        self.c3.bind("<Button-1>", self.c3Click)
        self.c3.place(x=100+132+132, y=106+132+132)





    #Mini methods for handling click on previously declared labels
    def a1Click(self,event):
        if self.tc.isMoveValid('a1'):
            self.__clicked__('a1')

    def a2Click(self,event):
        if self.tc.isMoveValid('a2'):
            self.__clicked__('a2')

    def a3Click(self,event):
        if self.tc.isMoveValid('a3'):
            self.__clicked__('a3')

    def b1Click(self,event):
        if self.tc.isMoveValid('b1'):
            self.__clicked__('b1')

    def b2Click(self,event):
        if self.tc.isMoveValid('b2'):
            self.__clicked__('b2')

    def b3Click(self,event):
        if self.tc.isMoveValid('b3'):
            self.__clicked__('b3')

    def c1Click(self,event):
        if self.tc.isMoveValid('c1'):
            self.__clicked__('c1')

    def c2Click(self,event):
        if self.tc.isMoveValid('c2'):
            self.__clicked__('c2')

    def c3Click(self,event):
        if self.tc.isMoveValid('c3'):
            self.__clicked__('c3')

    #general method that handles click on specific field
    def __clicked__(self, field):

        no2sign = {1:'X', -1:'O', 0.5:'Nobody'} #Little dictionary for messagebox

        self.tc.makeMove(field, self.tc.whoseTurn()) #Make move in engine

        self.updateImages() #Update labels' images
        #In case the game is finished, print messagebox
        if self.tc.isGameFinished():
            messagebox.showinfo("Finished!", "The game is over.\n %s won."%(no2sign[self.tc.winner]))

    #Method to update label  images depending of current board
    def updateImages(self):
        if self.getBoard()[0,0] == 1:
            self.a1.config(image=self.x_image)
        elif self.getBoard()[0,0] == -1:
            self.a1.config(image=self.o_image)
        else:
            self.a1.config(image=self.empty_image)

        if self.getBoard()[0,1] == 1:
            self.a2.config(image=self.x_image)
        elif self.getBoard()[0,1] == -1:
            self.a2.config(image=self.o_image)
        else:
            self.a2.config(image=self.empty_image)

        if self.getBoard()[0,2] == 1:
            self.a3.config(image=self.x_image)
        elif self.getBoard()[0,2] == -1:
            self.a3.config(image=self.o_image)
        else:
            self.a3.config(image=self.empty_image)

        if self.getBoard()[1,0] == 1:
            self.b1.config(image=self.x_image)
        elif self.getBoard()[1,0] == -1:
            self.b1.config(image=self.o_image)
        else:
            self.b1.config(image=self.empty_image)

        if self.getBoard()[1,1] == 1:
            self.b2.config(image=self.x_image)
        elif self.getBoard()[1,1] == -1:
            self.b2.config(image=self.o_image)
        else:
            self.b2.config(image=self.empty_image)

        if self.getBoard()[1,2] == 1:
            self.b3.config(image=self.x_image)
        elif self.getBoard()[1,2] == -1:
            self.b3.config(image=self.o_image)
        else:
            self.b3.config(image=self.empty_image)

        if self.getBoard()[2,0] == 1:
            self.c1.config(image=self.x_image)
        elif self.getBoard()[2,0] == -1:
            self.c1.config(image=self.o_image)
        else:
            self.c1.config(image=self.empty_image)

        if self.getBoard()[2,1] == 1:
            self.c2.config(image=self.x_image)
        elif self.getBoard()[2,1] == -1:
            self.c2.config(image=self.o_image)
        else:
            self.c2.config(image=self.empty_image)

        if self.getBoard()[2,2] == 1:
            self.c3.config(image=self.x_image)
        elif self.getBoard()[2,2] == -1:
            self.c3.config(image=self.o_image)
        else:
            self.c3.config(image=self.empty_image)


    #Method for new game
    def newGame(self):
        self.pack()
        self.create_widgets()
        self.tc.newGame()

    #Returns status of a game
    def isGameFinished(self):
        return self.tc.isGameFinished()

    #returs current board
    def getBoard(self):
        return self.tc.getBoard()

    #Returns current reward
    def getReward(self):
        return self.tc.winner
