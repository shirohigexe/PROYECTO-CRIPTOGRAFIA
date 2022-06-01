"""
from sympy import *
import itertools
D = (3, 4, 2, 3)
a = symarray("a", D)
x = symarray("x", len(D))
prod_iterator = itertools.product(*map(range, D))
result = Add(*[a[p]*Mul(*[v**d for v, d in zip(x, p)]) for p in prod_iterator])
print(result)
"""

import sympy as sympy

n = 6
vector = []

for i in range(n):
    vector.append(sympy.symbols("x"+str(i)))

print(vector)