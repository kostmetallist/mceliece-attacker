import logging
from logging import config as lc
import math

from blincodes import matrix as mx, vector


logger = logging.getLogger('UT')
lc.fileConfig(fname='logging.conf')


def dot_product(matrix1, matrix2):

    rows = [row1 & row2 for row1 in matrix1 for row2 in matrix2]
    new_pub = mx.from_vectors([row for row in mx.from_vectors(rows)
                                      .gaussian_elimination()
                                   if len(row.support)])
    return new_pub


# stands for eXtended Greatest Common Divisor
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


def dottify(matrix, x, y):

    q = math.ceil((-y)/x)
    s = q*x + y

    if s == q == 0:
        return None

    if s:
        rm_s = matrix
        for i in range(s - 1):
            rm_s = dot_product(rm_s, matrix)

    rm_qr = matrix
    for i in range(q - 1):
        rm_qr = dot_product(rm_qr, matrix)

    rm_qr = rm_qr.orthogonal
    rm_dm = rm_qr
    for i in range(x - 1):
        rm_dm = dot_product(rm_dm, rm_qr)

    return dot_product(rm_dm, rm_s) if s else rm_dm


def gcd_step(matrix, r, m):

    g, x, y = xgcd(m - 1, r)
    if x == 0 and y == 1:
        return g, matrix

    elif x > 0 and y < 0:
        return g, dottify(matrix, x, y)

    elif x < 0 and y > 0:
        return g, dottify(matrix, 1 - x, -y).orthogonal

    else:
        logger.info(f'received invalid x-y pair: ({x}, {y})')
        return None


def find_nonsingular(public, permuted_rm):
    rows = [permuted_rm.T.solve(row)[1] for row in iter(public)]
    return mx.from_vectors(rows)


def find_permutation(matrix, m):

    a = matrix.T.solve(vector.from_support_supplement(2**m))[1]
    removing_num = a.support[0] if len(a.support) else 0
    logger.debug(f'removing {removing_num}...')
    a_rows = [a]

    for i in range(m + 1):
        if i != removing_num:
            a_rows.append(a ^ vector.from_support(m + 1, [i]))

    a_rows = (mx.from_vectors(a_rows)*matrix)[1:]
    return mx.permutation([row.value for row in a_rows.T])
