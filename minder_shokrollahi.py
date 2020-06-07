import logging
from logging import config as lc
import math

from blincodes import matrix, vector
from blincodes.codes import tools
import networkx as nx
from networkx.algorithms.approximation import clique
from scipy.special import binom

from attacker import Attacker


logger = logging.getLogger('MS')
lc.fileConfig(fname='logging.conf')


class MinderShokrollahi(Attacker):

    def __init__(self, r, m):
        self.r = r
        self.m = m
        self.d = 2**(self.m - self.r)

    def _gauss_codeword_support(self, rm, codeword_support_list):

        for vec in tools.iter_codewords(rm):
            if vec.hamming_weight == self.d and \
               vec.support not in codeword_support_list:

                codeword_support_list.append(vec.support)
                return vec.support

    def _get_cliques(self, G):

        r = self.r
        m = self.m

        target_clique_size = 2**(m - r)
        target_number_of_cliques = 2**r - 1
        result_cliques = []

        while True:

            max_cliques = nx.find_cliques(G)
            exit_with_empty = True

            for clique in max_cliques:
                if len(clique) >= target_clique_size:
                    if not len(clique) % target_clique_size:

                        for i in range(int(len(clique) / target_clique_size)):
                            from_  = i*target_clique_size
                            result_cliques \
                                .append(clique[from_:from_+target_clique_size])

                        G.remove_nodes_from(clique)
                        exit_with_empty = False
                        break

            if exit_with_empty:
                logger.debug('return on flag')
                return []

            if len(result_cliques) == target_number_of_cliques:
                logger.debug('return on length equality')
                return result_cliques

    def _decompose_inner_sets(self, pub_key):
        
        m = self.m
        r = self.r
        eps = float(math.sqrt(1 - 1/(2**(m - 2*r + 1))))

        desired_weight_min = 2**(m - r)
        desired_weight_max = math.floor(float(2**(m - 2*r + 1)*(2**r - 1))*eps)
        codewords_supports = []

        for vec in tools.iter_codewords(pub_key):
            if vec.hamming_weight >= desired_weight_min and \
               vec.hamming_weight <= desired_weight_max:

                codewords_supports.append(vec.support)

        word_len = 2**m
        logger.debug(f'word length is {word_len}')
        G = nx.Graph()
        G.add_nodes_from(range(word_len))

        cij = [[0 for x in range(word_len)] for y in range(word_len)]
        for i in range(word_len):
            for j in range(i + 1, word_len):
                word_num = 0
                for word_support in codewords_supports:
                    if (i in word_support) and (j in word_support):
                        cij[i][j] += 1

                    word_num += 1

        c = max({cij[i][j] for i in range(word_len)
                           for j in range(i + 1, word_len)})
        logger.debug(f'threshold c is set to {c}')

        for i in range(word_len):
            for j in range(i + 1, word_len):
                if cij[i][j] >= c:
                    G.add_edge(i,j)

        cliques = self._get_cliques(G)
        assert(len(cliques) != 0)
        return cliques

    def attack(self, pub_key):
        
        B = matrix.Matrix()
        B_size = 0
        for i in range(self.r):
            B_size += binom(self.m, i)

        codeword_support_list = []
        while B.nrows < B_size: 

            codeword_support = self \
                ._gauss_codeword_support(pub_key, codeword_support_list)
            codeword_support_list.append(codeword_support)
   
            pub_key_truncated = tools.truncate(pub_key, codeword_support)
            inner_sets = self._decompose_inner_sets(pub_key_truncated)

            f_vecs = [vector.from_support(2**self.m, codeword_support + s)
                      for s in inner_sets]
            B = tools.union(B, matrix.from_vectors(f_vecs))

        return B
