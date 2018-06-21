'''
Sample script for teaching neural network with keras
Author: Szymon Krasuski
June 2018

'''


fname = 'net1.hdf5' #Set name of your model
b_size = 16 #Set batch size
epochs = 1000 #set number of epochs


import keras
import sys, os.path
import time, h5py

from keras import models
from keras.layers import Conv2D, Dense, Flatten, MaxPool2D
from keras.callbacks import LambdaCallback
from keras.models import load_model


import numpy as np
#Import and set database
from database.SQLinterface import *
#Get logi and password for SQL
login  = input("SQL login: ")
psswd = getpass.getpass("SQL password: ")
sql = SQLinterface(name=login, password=psswd) #Create connection for data generator
sql_v = SQLinterface(name=login, password=psswd) #Create connection for validation data generator
fname = 'net1.hdf5' #Set name of your model
b_size = 16 #Set batch size
epochs = 1000 #set number of epochs

#declare size of batch in SQL
sql.declareBatch(b_size)
sql_v.declareBatch(b_size)

#Make model of neural network
def build():
    model = models.Sequential()
    model.add(Dense(200, input_shape=(3,3), activation='relu'))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='mean_squared_error', optimizer='sgd')
    return model

#Declare generator for learning dataset
def generator():
    cnt=0
    while 1:
        if cnt%b_size == 0:
            sql.declareBatch(b_size)
        cnt = cnt+1

        inmx, outmx = sql.getBatch()
        sql.getBatch()
        yield inmx, outmx

#Declare another generator for validation data - keras requires it to be separate connection and generator
def val_generator():
    cnt_v=0
    while 1:
        if cnt_v%b_size == 0:
            sql_v.declareBatch(b_size)
        cnt_v = cnt_v+1
        sql_v.getBatch()
        inmx_v, outmx_v = sql_v.getBatch()
        yield inmx_v, outmx_v

#Execute teaching process
model = build() #build model
#Fit given dataset into neural network. At the end of every epoch print value of loss
model.fit_generator(generator(), 50, epochs, callbacks = [LambdaCallback(on_epoch_end=lambda epoch, logs: sys.stdout.write("\nEpoch {} : loss = {:.10f} \n".format(epoch + 1, logs['loss']))), LambdaCallback(on_epoch_begin=lambda epoch, logs: sys.stdout.write("{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"))))], validation_data=val_generator(),validation_steps=50)
model.save("models/%s"%fname) # At the end save model to models directory with selected name

#Close SQL connectons
sql.finish()
sql_v.finish()
