import logging
from logging import config as lc
from random import shuffle

from blincodes import matrix
from blincodes.codes import rm as rm_code

from attacker import Attacker


# 'CB' stands for Chizhov-Borodin
logger = logging.getLogger('CB')
lc.fileConfig(fname='logging.conf')


class ChizhovBorodin(Attacker):

    # stands for eXtended Greatest Common Divisor
    @staticmethod
    def xgcd(a, b):
    """
    Return (gcd, x, y) where gcd is the greatest common divisor of `a` and `b`
    with the sign of `b` if `b` is nonzero, and with the sign of `a` otherwise.
    The numbers `x`, `y` are such that gcd = ax+by.
    
    Credit to: http://anh.cs.luc.edu/331/code/xgcd.py
    """
    prev_x, x = 1, 0
    prev_y, y = 0, 1
    while b:
        q, r = divmod(a,b)
        x, prev_x = prev_x - q*x, x  
        y, prev_y = prev_y - q*y, y
        a, b = b, r

    return a, prev_x, prev_y

    @staticmethod
    def gcd_step(r, m, rm):
        g, x, y = ChizhovBorodin.xgcd(m - 1, r)
        if x == 0 and y == 1:
            return g, rm

    @staticmethod
    def find_permutation(rm, m):
        return

    @staticmethod
    def find_nonsingular(pubkey, rm):
        return

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

        r = self.r
        rm = self.public_key
        is_dual_code = self.m <= 2 * self.r
        
        if is_dual_code:
            r = self.m - 1 - r 
            rm = rm.orthogonal

        d, rm = self.gcd_step(r, self.m, rm)
        if d != 1:
            logger.info('performing Minder-Shokrollahi attack...')
            rm_minus_1 = MinderShokrollahi(d, self.m).attack(rm)

        elif:
            logger.info("skipping Minder-Shokrollahi step...")

        self.logger.debug("solving P and M matrices...")
        P = self.find_permutation(rm, self.m)

        permuted_rm = rm_code.generator(r, self.m) * P
        M = self.find_nonsingular(self.public_key, permuted_rm)
        
        return M, P
