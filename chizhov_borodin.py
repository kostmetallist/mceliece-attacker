from random import shuffle
import logging
from logging import config as lc

from blincodes import matrix
from blincodes.codes import rm as rm_code

from attacker import Attacker


# 'CB' stands for Chizhov-Borodin
logger = logging.getLogger('CB')
lc.fileConfig(fname='logging.conf')


class ChizhovBorodin(Attacker):

    def __init__(self, r, m):

        self.r = r
        self.m = m
        self.generate_keys()

    def generate_keys(self):

        logger.info('generating pair of keys...')
        G = rm_code.generator(self.r, self.m)
        M = matrix.nonsingular(G.nrows)
        permutation = list(range(G.ncolumns))
        shuffle(permutation)
        P = matrix.permutation(permutation)
        
        self.private_key = (M, G, P)
        self.public_key = (M * G * P)
        logger.debug(self.stringify_matrix('Public Key', self.public_key))

    def attack(self):
        pass
