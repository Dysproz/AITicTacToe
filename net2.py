'''
Sample script for teaching neural network with keras
Author: Szymon Krasuski
June 2018

'''
b_size = 16
epochs = 1000
fname = "net2"
from netBuilder import *

net = netBuilder(batchSize=b_size, epochs = epochs, fname=fname)

model = models.Sequential()
model.add(Conv1D(196, kernel_size=(1), input_shape=(1,9), padding='same', activation='relu'))
model.add(MaxPool1D(padding='same'))
model.add(Conv1D(184, kernel_size=(2), padding='same', activation='relu'))
model.add(Dense(156, activation='relu'))
model.add(Conv1D(124,kernel_size=(3),padding='same', activation='relu'))
model.add(Conv1D(64,kernel_size=(2),padding='same', activation='relu'))
model.add(Dense(20))
model.add(Dense(9,activation='softmax'))

model.compile(loss='mean_squared_error', optimizer='adam')

net.fitGenerator(model)
net.finish()
