'''
Simple class that works as an interface between python scripts and SQL server.
Data is stored as binary (int with specified size) to save space used for keeping data
Author: Szymon Krasuski
June 2018
'''



import psycopg2
import getpass
import numpy as np



class SQLinterface:

    #On create it's possible to pass login and password as arguments or cllass will as for it in terminal
    #setting reset to any vlue will result in creating table for data.
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

    #Method for creating table Games that keeps our data
    def createTables(self):
        self.cur.execute("CREATE TABLE Games (boards numeric(37,0), moves numeric(5,0));")

    #Method for inserting data into SQL - board is  a 3x3 numpy array, move is a 2 letter string and fig is integer (with value 1 or -1)
    def insertRecord(self, board, move, fig):
        self.cur.execute("INSERT INTO Games VALUES (%u, %u);"%(self.hashBoard(board), self.hashMove(move,fig)))

    #Method for declaring size of batch and setting offset to 0 (begin from the first record)
    def declareBatch(self, limit):
        self.limit = limit
        self.offset = 0

    #Method returns batch (with size specified previously) of boards and moves. Boards are represented in 3x3 numpy arrays and moves are represented with 2 letter strings
    def getBatch(self):

        lt2no = {'a':0, 'b':1, 'c':2} #little dictionary to manipulate letters and numbers of rows
        self.cur.execute('SELECT * FROM Games LIMIT %u OFFSET %u;'%(self.limit, self.offset)) #Select data

        self.offset+=self.limit #Update offset

        found = self.cur.fetchall() #get returned result
        boards = np.zeros((self.limit,1, 9)) #Pre-declare boards
        moves = np.zeros((self.limit,1,9)) #Pre-declare moves
        for i in range(0,self.limit):
            boards[i,0,:] = self.decodeBoard(int(found[i][0])).ravel() #Decode every board
            move = self.decodeMove(int(found[i][1]))[0] #Decode move
            moves[i,0,lt2no[move[0]]*3+ int(move[1])-1] = 1 #Put figure in decoded field (we only teach networks for X so it's 1)

        return boards, moves

    #Export CSV file with records
    def exportCSV(self, filename):
        file = open('%s.csv'%filename, 'w')
        self.cur.copy_to(file, 'Games', ',')
        file.close()

    #Improt records from CSV file
    def importCSV(self, filename):
        file = open('filename', 'r')
        next(file)
        self.cur.copy_from(file, 'Games', sep=',')

    #Delete tables and all records
    def deleteTables(self):
        self.cur.execute("DROP TABLE Games;")

    #Finish connection and commit changes
    def finish(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        print("\nSQL saved and closed.")

    #Hash board from 3x3 numpy array  into integer (board coded in binary)
    '''
    Hashing key:
    1.We hash only fields with X or O - empty fields are not hashed
    2.Every field is hashed as RowNumber_ColumnNumber_Figure represented with binary values
    3.RowNumber has 2 bits and every row is coded starting from 1 (it means that a is 1 (01b); b is 2(10b); c is 3(11b))
    4.ColumenNumber is coded in the same way as RowNumber
    5.Figure is coded as 1 for X and 0 for O
    6.Each field segment takes 5 bits
    7.Segments make chain with hashed fields and then resulted binary chain is wirtten as integer
    '''
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

    #Hash move into binary value
    '''
    Hashing Key:
    1.move is hashed in the same way as in board but without figure bit
    2.Hashed binary looks like: RowNumber_ColumnNumber
    3.RowNumber has 2 bits and every row is coded starting from 1 (it means that a is 1 (01b); b is 2(10b); c is 3(11b))
    4.ColumenNumber is coded in the same way as RowNumber
    '''
    def hashMove(self, move, fig):
        if fig == -1:
            fig = 0
        return int("%s%i"%(self.__hashField__(move), fig),2)

    #Decode hashed board into 3x3 nump array
    def decodeBoard(self, hashedBoard):
        binary = list(bin(hashedBoard)[2:])

        #Check whether there are no 0s missing at the beginning and if yes then add 0s
        gap = 5-(len(binary))%5
        if gap != 0:
            binary = ['0'] + binary

        resultBoard = np.zeros((3,3))
        for i in range(0, int(len(binary)/5)):
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

    #Decode hashed move
    def decodeMove(self, hashedMove):

        coded = list(str(format(hashedMove, '#07b')[2:]))
        lfdict = {1:'a', 2:'b', 3:'c'}
        fig = coded[-1]
        if fig == '0':
            fig = '-1'
        return "%s%i"%(lfdict[int("".join(coded[:2]), 2)], (int("".join(coded[2:-1]), 2))), fig

    #Method for hashing one field into biary representation
    def __hashField__(self, field):
        fldict = {'a':'1', 'b':'2', 'c':'3'}
        field = list(field)

        try:
            field[0] = fldict[field[0]]
        except:
            pass

        return "%s%s"%(format((int(field[0])), '#04b')[2:], format(int(field[1]), '#04b')[2:])

    #Method for decoding one field
    def __dehashField__(self, hashedField):
        coded = list(str(format(hashedField, '#06b')[2:]))
        lfdict = {1:'a', 2:'b', 3:'c'}
        return "%s%s"%(lfdict[int("".join(coded[:2]), 2)], str(int("".join(coded[2:]), 2)-1))
