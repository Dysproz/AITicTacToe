'''
Sample script for teaching neural network with keras
Author: Szymon Krasuski
June 2018

'''
b_size = 16
epochs = 1000
fname = "net1"
from netBuilder import *

net = netBuilder(batchSize=b_size, epochs = epochs, fname=fname)

model = models.Sequential()
model.add(Dense(200, input_shape=(1,9), activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(9, activation='softmax'))

model.compile(loss='mean_squared_error', optimizer='sgd')

net.fitGenerator(model)
net.finish()
