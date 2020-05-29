from random import shuffle

from blincodes import matrix
from blincodes.codes import rm as rm_code

from attacker import Attacker


class ChizhovBorodin(Attacker):

    def __init__(self, r, m):

        self.r = r
        self.m = m
        self.generate_keys()

    def generate_keys(self):

        G = rm_code.generator(self.r, self.m)
        M = matrix.nonsingular(G.nrows)
        permutation = list(range(G.ncolumns))
        shuffle(permutation)
        P = matrix.permutation(permutation)
        
        self.private_key = (M, G, P)
        self.public_key = (M * G * P)

    def attack():
        pass
