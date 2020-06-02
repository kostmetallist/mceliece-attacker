from random import shuffle
import logging
from logging import config as lc

from blincodes import matrix
from blincodes.codes import rm as rm_code

from attacker import Attacker


logger = logging.getLogger(__name__)
lc.fileConfig(fname='logging.conf')


class ChizhovBorodin(Attacker):

    def __init__(self, r, m):

        logger.info('info message')
        logger.debug('debug message')
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

    def attack(self):
        pass
