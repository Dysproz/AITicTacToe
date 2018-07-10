import keras
import sys, os.path
import time, h5py

from keras import models
from keras.layers import Conv2D, Dense, Flatten, MaxPool2D, Conv1D, MaxPool1D
from keras.callbacks import LambdaCallback
from keras.models import load_model


import numpy as np
from database.SQLinterface import *



class netBuilder:

    def __init__(self,batchSize = 16, epochs = 100, fname = "netName", login=None, psswd=None):
        self.b_size = batchSize
        self.epochs = epochs
        self.fname = "%s.hdf5"%fname
        if login is None or psswd is None:
            self.login  = input("SQL login: ")
            self.psswd = getpass.getpass("SQL password: ")
        else:
            self.login = login
            self.psswd = psswd

        self.sql = SQLinterface(name=self.login, password=self.psswd) #Create connection for data generator
        self.sql_v = SQLinterface(name=self.login, password=self.psswd) #Create connection for validation data generator
        self.sql.declareBatch(self.b_size)
        self.sql_v.declareBatch(self.b_size)
    #Declare generator for learning dataset
    def generator(self):
        cnt=0
        while 1:
            if cnt%self.b_size == 0:
                self.sql.declareBatch(self.b_size)
            cnt = cnt+1

            inmx, outmx = self.sql.getBatch()
            self.sql.getBatch()

            yield inmx, outmx

    #Declare another generator for validation data - keras requires it to be separate connection and generator
    def val_generator(self):
        cnt_v=0
        while 1:
            if cnt_v%self.b_size == 0:
                self.sql_v.declareBatch(self.b_size)
            cnt_v = cnt_v+1
            self.sql_v.getBatch()
            inmx_v, outmx_v = self.sql_v.getBatch()

            yield inmx_v, outmx_v

    def fitGenerator(self, model):
        #Fit given dataset into neural network. At the end of every epoch print value of loss
        model.fit_generator(self.generator(), 50, self.epochs, callbacks = [LambdaCallback(on_epoch_end=lambda epoch, logs: sys.stdout.write("\nEpoch {} : loss = {:.10f} \n".format(epoch + 1, logs['loss']))), LambdaCallback(on_epoch_begin=lambda epoch, logs: sys.stdout.write("{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"))))], validation_data=self.val_generator(),validation_steps=50)
        model.save("models/%s"%self.fname) # At the end save model to models directory with selected name

    def finish(self):
        #Close SQL connectons
        self.sql.finish()
        self.sql_v.finish()
