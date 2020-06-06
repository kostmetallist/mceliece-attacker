import logging
from logging import config as lc
from random import shuffle

from blincodes import matrix
from blincodes.codes import rm as rm_code

from attacker import Attacker
from utils import dot_product, find_nonsingular, find_permutation, gcd_step


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

        r = self.r
        rm = self.public_key
        is_dual_code = self.m <= 2 * self.r
        
        if is_dual_code:
            r = self.m - 1 - r 
            rm = rm.orthogonal

        d, rm = gcd_step(rm, r, self.m)
        if d != 1:
            logger.info('performing Minder-Shokrollahi attack...')
            rm_minus_1 = MinderShokrollahi(d, self.m).attack(rm)
            rm = dot_product(rm.orthogonal, rm_minus_1).orthogonal

        elif:
            logger.info('skipping Minder-Shokrollahi step...')

        self.logger.debug('solving P and M matrices...')
        P = find_permutation(rm, self.m)
        if is_dual_code:
            r = self.m - 1 - r

        permuted_rm = rm_code.generator(r, self.m) * P
        M = find_nonsingular(self.public_key, permuted_rm)
        
        return M, P
