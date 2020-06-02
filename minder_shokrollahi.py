import logging
from logging import config as lc

from blincodes import matrix

from attacker import Attacker


logger = logging.getLogger('MS')
lc.fileConfig(fname='logging.conf')


class MinderShokrollahi(Attacker):

    def __init__(self, r, m):
        self.r = r
        self.m = m
        self.d = 2**(self.m - self.r)

    def attack(self, pub_key):
        
        B = matrix.Matrix()
        B_size = 0

        codeword_support_list = []

        return B
