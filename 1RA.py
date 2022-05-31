import sympy as S 
import random 

#campo finito
from pyfinite import ffield
valor_primo=[3, 5, 7]
valor_campo=random.choice(valor_primo)
F = ffield.FField(valor_campo) 
#help(ffield.FField)
print(len(F))

#matriz aleatoria
import numpy as np
 #crear un array numpy con ceros
a = np.zeros(valor_campo-1)
print(a)
#vector de simbolos
ver_simbo=[0, 1, x, x**2]
#arreglo en la matrix






