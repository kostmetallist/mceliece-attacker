import logging
from logging import config as lc
import math


logger = logging.getLogger('UT')
lc.fileConfig(fname='logging.conf')


def dot_product(matrix1, matrix2):

    rows = [row1 & row2 for row1 in matrix1 for row2 in matrix2]
    new_pub = matrix.from_vectors([row for row in matrix.from_vectors(rows)
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


def dottify_key(gpub, x, y):

    q = math.ceil((-y)/x)
    s = q*x + y

    if s == q == 0:
        return None

    if s:
        rm_s = gpub
        for i in range(s - 1):
            rm_s = dot_product(rm_s, gpub)

    rm_qr = gpub
    for i in range(q - 1):
        rm_qr = dot_product(rm_qr, gpub)

    rm_qr = rm_qr.orthogonal
    rm_dm = rm_qr
    for i in range(x - 1):
        rm_dm = dot_product(rm_dm, rm_qr)

    return dot_product(rm_dm, rm_s) if s else rm_dm


def gcd_step(r, m, rm):

    g, x, y = xgcd(m - 1, r)
    if x == 0 and y == 1:
        return g, rm

    elif x > 0 and y < 0:
        return g, dottify_key(rm, x, y)

    elif x < 0 and y > 0:
        return g, dottify_key(rm, 1 - x, -y).orthogonal

    else:
        logger.info(f'received invalid x-y pair: ({x}, {y})')
        return None


def find_permutation(rm, m):
    return


def find_nonsingular(pubkey, rm):
    return
