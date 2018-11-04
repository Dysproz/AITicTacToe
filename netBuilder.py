import sys
import time
import database.SQLinterface
import getpass
from keras.callbacks import LambdaCallback


class netBuilder:
    def __init__(self,
                 batchSize=16,
                 epochs=100,
                 fname="netName",
                 login=None,
                 psswd=None):
        self.b_size = batchSize
        self.epochs = epochs
        self.fname = "%s.hdf5" % fname
        if login is None or psswd is None:
            self.login = input("SQL login: ")
            self.psswd = getpass.getpass("SQL password: ")
        else:
            self.login = login
            self.psswd = psswd

        self.sql = database.SQLinterface.SQLinterface(name=self.login,
                                                      password=self.psswd)
        self.sql_v = database.SQLinterface.SQLinterface(name=self.login,
                                                        password=self.psswd)
        self.sql.declareBatch(self.b_size)
        self.sql_v.declareBatch(self.b_size)

    def generator(self):
        cnt = 0
        while 1:
            if cnt % self.b_size == 0:
                self.sql.declareBatch(self.b_size)
            cnt = cnt+1

            inmx, outmx = self.sql.getBatch()
            self.sql.getBatch()

            yield inmx, outmx

    def val_generator(self):
        cnt_v = 0
        while 1:
            if cnt_v % self.b_size == 0:
                self.sql_v.declareBatch(self.b_size)
            cnt_v = cnt_v+1
            self.sql_v.getBatch()
            inmx_v, outmx_v = self.sql_v.getBatch()

            yield inmx_v, outmx_v

    def fitGenerator(self, model):

        time_callback = LambdaCallback(on_epoch_begin=lambda epoch,
                                       logs: sys
                                       .stdout
                                       .write("{}\n"
                                              .format(time
                                                      .strftime("%Y-%m-%d"
                                                                "%H:%M:%S"))))
        epoch_loss = LambdaCallback(on_epoch_end=lambda epoch,
                                    logs: sys
                                    .stdout
                                    .write("\nEpoch {} : loss = {:.10f} \n"
                                           .format(epoch + 1, logs['loss'])))
        model.fit_generator(self.generator(),
                            50,
                            self.epochs,
                            callbacks=[epoch_loss, time_callback],
                            validation_data=self.val_generator(),
                            validation_steps=50)
        model.save("models/%s" % self.fname)

    def finish(self):
        self.sql.finish()
        self.sql_v.finish()
