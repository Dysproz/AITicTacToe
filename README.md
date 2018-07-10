This is a small project of AI for TicTacToe.

It's a playground for pretty simple problem where I can test various types of machine learning algorithms.

# As far I played with:

## 1.Qlearning algorithm

Self-learning algorithm based on formula for Q.
AI has a set of available moves and choose one of them based on random choice or previously calculated Q (It's based on AIPlayer epsilon value how random should these moves be).
After every move Player gets reward that is used to calculate next value of Q.
Algorithms tries to maximalize value of reward (so it tries to win the game).

## 2.CNN with Keras

Keras gives a great opportunity to build neural networks easily and focus on architecture of network.

games.csv file contains a set of games with boards and moves that were performed in these situations by Qlearning algorithm.
Networks use psycopg2 interface so to use thsese scripts you need to import .csv file into Postgres database. (It can be done with SQLinterface class)

Neural network has a 1x9 array on input and 1x9 array on output.
Input array cointains 1s on fields with Xs and -1s on fields with Os.
Neural network is trained to play as X so on output it gets 1 on field where it should put an X.

Networks:
net1.py - first test network with only Dense (Fully Connected) layers.
net2.py - my custom network with Dense, MaxPool and Conv layers
netAlexNet.py - network based on AlexNet network

My trained models are stored in models/ directory.
