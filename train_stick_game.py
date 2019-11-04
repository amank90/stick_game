from collections import defaultdict, Counter
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
#import pickle
import dill as pickle
from tqdm import tqdm
import time
import math
from scipy.stats import expon
import random
import sys
#from tqdm import tqdm_notebook as tqdm


class Player:

    def __init__(self, player_number):
        self.player_number = player_number

    def initial_state(self, n):

        self.stick_count = defaultdict(lambda: defaultdict(int))
        self.stick_prob = defaultdict(lambda: defaultdict(float))

        for i in range(1, n + 1):  # iterating over no. of sticks
            for j in range(1, 4):
                self.stick_count[i][j] = 3
                self.stick_prob[i][j] = 1 / 3

    # updating policy for winning
    def update_policy_winner(self):

        for k in self.stick_no.keys():
            self.stick_count[k][self.stick_no[k]] += 1
            for i in range(1, 4):
                self.stick_prob[k][i] = self.stick_count[k][i] / sum(self.stick_count[k].values())

    # updating policy for losing
    def update_policy_loser(self):

        for k in self.stick_no.keys():
            if sum(self.stick_count[k].values()) > 1 and self.stick_count[k][self.stick_no[k]] > 0:
                self.stick_count[k][self.stick_no[k]] -= 1
            for i in range(1, 4):
                self.stick_prob[k][i] = self.stick_count[k][i] / sum(self.stick_count[k].values())

    def save_policy(self):
        with open('policy_%s.bin' % ('first' if self.player_number == 1 else 'second'), 'wb') as f:
            pickle.dump(self.stick_prob, f)
            pickle.dump(self.stick_count, f)

    def load_policy(self):
        with open('policy_%s.bin' % ('first' if self.player_number == 1 else 'second'), 'rb') as f:
            self.stick_prob = pickle.load(f)
            self.stick_count = pickle.load(f)


class State:

    def __init__(self, n, player1, player2, N, epsilon=0.8):

        self.n = n
        self.sticks = n
        self.player1 = player1
        self.player2 = player2
        self.epsilon = epsilon
        self.N = N

    def reset_state(self):
        self.sticks = self.n
        self.player1.stick_no = {}
        self.player2.stick_no = {}

    def update_state(self, player, sim):

        keys = list(player.stick_prob[self.sticks].keys())
        values = list(player.stick_prob[self.sticks].values())

        if expon.pdf(sim / self.N, loc=0, scale=1) > self.epsilon and np.random.uniform(0, 1) > 0.5:

            rand_index_1 = np.random.choice(len(keys))
            player.stick_no[self.sticks] = keys[rand_index_1]

        else:
            rand_index_1 = np.random.choice(len(keys), 1, p=values)
            player.stick_no[self.sticks] = keys[rand_index_1[0]]
        self.sticks = self.sticks - player.stick_no[self.sticks]

    # checking the winner
    def check_winner(self, winner):

        if winner == 1:
            self.player1.update_policy_winner()
            self.player2.update_policy_loser()
        else:
            self.player2.update_policy_winner()
            self.player1.update_policy_loser()


def train(N, n):
    """
    Train the bot to play a stick game by making two AI players to compete

    Parameters
    ----------
    N : no. of simulations
    n : no. of sticks

    Returns
    -------

    Trained AI players

    player1 : object
    player2 : object


    Examples
    --------
    train(50000,50)

    """

    player1 = Player(1)
    player2 = Player(2)

    state = State(n, player1, player2, N, 0.8)

    player1.initial_state(n)
    player2.initial_state(n)

    for sim in tqdm(range(N)):
        # print (sim)

        state.reset_state()

        while True:

            if state.sticks > 0:
                state.update_state(player1, sim)
                # print (state.sticks)
            else:
                winner = 1
                # print ("Player 1 Wins")
                break

            if state.sticks > 0:
                state.update_state(player2, sim)
            else:
                winner = 2
                # print ("Player 2 Wins")
                break

        state.check_winner(winner)

    player1.save_policy()
    player2.save_policy()

    time.sleep(0.01)



if __name__ == '__main__':
    train(50000,50)

