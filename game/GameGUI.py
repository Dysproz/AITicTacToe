from tkinter import *
from TicTacToe import *
from PIL import ImageTk,Image
from tkinter import messagebox



class GameGUI(Frame):

    def __init__(self, master=None):

        self.tc = TicTacToe()


        self.bg_image = ImageTk.PhotoImage(Image.open('graphics/background.png'))
        self.x_image = ImageTk.PhotoImage(Image.open('graphics/x.png'))
        self.o_image = ImageTk.PhotoImage(Image.open('graphics/o.png'))
        self.empty_image = ImageTk.PhotoImage(Image.open('graphics/empty.png'))

        master.minsize(width=self.bg_image.width(), height=self.bg_image.height())
        super().__init__(master)

        self.pack()
        label1 = Label(root, image=self.bg_image)
        label1.pack()
        self.create_widgets()

    def create_widgets(self):


        self.new = Button(master=None, text="New Game", width=50, height=3, background="#B0E0E6", command= lambda: self.newGame())
        self.new.place(x=100, y=30)

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





    def a1Click(self,event):
        if self.tc.isMoveValid('a1'):
            if self.tc.whoseTurn()==1:
                self.a1.config(image=self.x_image)
            else:
                self.a1.config(image=self.o_image)
            self.__clicked__('a1')

    def a2Click(self,event):
        if self.tc.isMoveValid('a2'):
            if self.tc.whoseTurn()==1:
                self.a2.config(image=self.x_image)
            else:
                self.a2.config(image=self.o_image)
            self.__clicked__('a2')

    def a3Click(self,event):
        if self.tc.isMoveValid('a3'):
            if self.tc.whoseTurn()==1:
                self.a3.config(image=self.x_image)
            else:
                self.a3.config(image=self.o_image)
        self.__clicked__('a3')

    def b1Click(self,event):
        if self.tc.isMoveValid('b1'):
            if self.tc.whoseTurn()==1:
                self.b1.config(image=self.x_image)
            else:
                self.b1.config(image=self.o_image)
            self.__clicked__('b1')

    def b2Click(self,event):
        if self.tc.isMoveValid('b2'):
            if self.tc.whoseTurn()==1:
                self.b2.config(image=self.x_image)
            else:
                self.b2.config(image=self.o_image)
            self.__clicked__('b2')

    def b3Click(self,event):
        if self.tc.isMoveValid('b3'):
            if self.tc.whoseTurn()==1:
                self.b3.config(image=self.x_image)
            else:
                self.b3.config(image=self.o_image)
            self.__clicked__('b3')

    def c1Click(self,event):
        if self.tc.isMoveValid('c1'):
            if self.tc.whoseTurn()==1:
                self.c1.config(image=self.x_image)
            else:
                self.c1.config(image=self.o_image)
            self.__clicked__('c1')

    def c2Click(self,event):
        if self.tc.isMoveValid('c2'):
            if self.tc.whoseTurn()==1:
                self.c2.config(image=self.x_image)
            else:
                self.c2.config(image=self.o_image)
            self.__clicked__('c2')

    def c3Click(self,event):
        if self.tc.isMoveValid('c3'):
            if self.tc.whoseTurn()==1:
                self.c3.config(image=self.x_image)
            else:
                self.c3.config(image=self.o_image)
            self.__clicked__('c3')

    def __clicked__(self, field):
        no2sign = {1:'X', -1:'O'}
        print(field)
        self.tc.makeMove(field, self.tc.whoseTurn())
        print(self.tc.getBoard())
        if self.tc.isGameFinished():
            messagebox.showinfo("Finished!", "The game is over.\n %s won"%(no2sign[self.tc.winner]))



    def newGame(self):
        self.pack()
        self.create_widgets()
        self.tc.newGame()


root = Tk()
root.wm_title("AI TicTacToe")

root.configure()
app = GameGUI( master=root)

app.mainloop()
