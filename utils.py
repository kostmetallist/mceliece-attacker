import math


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


def gcd_step(r, m, rm):
    g, x, y = xgcd(m - 1, r)
    if x == 0 and y == 1:
        return g, rm


def find_permutation(rm, m):
    return


def find_nonsingular(pubkey, rm):
    return
