import psycopg2
import getpass
import numpy as np

class SQLinterface:


    def __init__(self, reset=None, name = None, password=None):
        if name is None or password is None:
            login  = input("SQL login: ")
            psswd = getpass.getpass("SQL password: ")
        else:
            login = name
            psswd = password
        connectionString = "dbname='tictactoe' user='%s' host='localhost' password='%s'"%(login,psswd)
        self.conn = psycopg2.connect(connectionString)
        self.cur = self.conn.cursor()
        if reset != None:
            self.createTables()

    def createTables(self):
        self.cur.execute("CREATE TABLE Games (boards numeric(37,0), moves numeric(5,0));")

    def insertRecord(self, board, move, fig):
        self.cur.execute("INSERT INTO Games VALUES (%u, %u);"%(self.hashBoard(board), self.hashMove(move,fig)))

    def declareBatch(self, limit):
        self.limit = limit
        self.offset = 0

    def getBatch(self):
        self.cur.execute('SELECT * FROM Games LIMIT %u OFFSET %u;'%(self.limit, self.offset))

    def exportCSV(self, filename):
        file = open('%s.csv'%filename, 'w')
        self.cur.copy_to(file, 'Games', ',')
        file.close()

    def importCSV(self, filename):
        file = open('filename', 'r')
        next(file)
        self.cur.copy_from(file, 'Games', sep=',')

    def deleteTables(self):
        self.cur.execute("DROP TABLE Games;")

    def finish(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        print("\nSQL saved and closed.")

    def hashBoard(self, board):
        hashedBoard= []
        for i in range(0,3):
            for j in range(0,3):

                if board[i,j] != 0:
                    fig = str(int(board[i,j]))

                    if fig == '-1':
                        fig = '0'


                    hashedBoard.append(self.__hashField__("%i%i"%(i+1,j+1)))

                    hashedBoard.append(fig)


        return int("".join(hashedBoard), 2)

    def hashMove(self, move, fig):
        if fig == -1:
            fig = 0
        return int("%s%i"%(self.__hashField__(move), fig),2)

    def decodeBoard(self, hashedBoard):
        binary = list(bin(hashedBoard)[2:])

        gap = 5-(len(binary))%5
        if gap != 0:
            binary = ['0'] + binary

        resultBoard = np.zeros((3,3))
        for i in range(0, 9):
            if not binary:
                break
            fig = binary[-1]
            if fig == '0':
                fig = '-1'
            del binary[-1]
            posX = int("".join(binary[-2:]),2)
            del binary[-2:]
            posY = int("".join(binary[-2:]),2)
            del binary[-2:]
            resultBoard[posX-1, posY-1]=fig

        return resultBoard

    def decodeMove(self, hashedMove):

        coded = list(str(format(hashedMove, '#07b')[2:]))
        lfdict = {1:'a', 2:'b', 3:'c'}
        fig = coded[-1]
        if fig == '0':
            fig = '-1'
        return "%s%i"%(lfdict[int("".join(coded[:2]), 2)], (int("".join(coded[2:-1]), 2))), fig

    def __hashField__(self, field):
        fldict = {'a':'1', 'b':'2', 'c':'3'}
        field = list(field)

        try:
            field[0] = fldict[field[0]]
        except:
            pass

        return "%s%s"%(format((int(field[0])), '#04b')[2:], format(int(field[1]), '#04b')[2:])

    def __dehashField__(self, hashedField):
        coded = list(str(format(hashedField, '#06b')[2:]))
        lfdict = {1:'a', 2:'b', 3:'c'}
        return "%s%s"%(lfdict[int("".join(coded[:2]), 2)], str(int("".join(coded[2:]), 2)-1))
