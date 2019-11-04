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

    def load_policy(self):
        with open('policy_%s.bin' % ('first' if self.player_number == 1 else 'second'), 'rb') as f:
            self.stick_prob = pickle.load(f)
            self.stick_count = pickle.load(f)

def play_game():

    """Play the game of sticks


    Examples
    --------
    >>> play_game()

    """

    player = Player(2)
    player.load_policy()
    val = input("Enter number of sticks between 10 and 50: ")
    val = int(val)

    print("Start the game")

    # print (player.stick_prob)

    while True:

        if val == 1:
            print("Computer Won")
            break

        p = input("Pick any number of sticks from 1,2,3 : ")

        if int(p) < 4:

            val -= int(p)

            if val == 1:
                print("Player Won")
                break

            keys = list(player.stick_prob[val].keys())
            values = list(player.stick_prob[val].values())
            # rand_index_2 = np.random.choice(len(keys), 1, p=values)
            # s = keys[rand_index_2[0]]
            s = keys[np.argmax(values)]
            val -= s
            print(val)
        else:
            print("Invalid Entry")
            print(val)


if __name__ == '__main__':
    play_game()
