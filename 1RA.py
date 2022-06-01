from typing import Counter
import sympy as S 
import random 

#campo finito
from pyfinite import ffield

valor_primo=[3, 5, 7]
valor_campo=random.choice(valor_primo)
F = ffield.FField(valor_campo) 
#help(ffield.FField)
print(valor_campo)
print(F.ShowPolynomial(valor_campo))


#tamaño del numero a codificar
n=6 

#matriz aleatoria
import numpy as np
#crear un array numpy con ceros
A = np.zeros((n,n))
print(A)
#vector de simbolos
α= S.symbols('α')
#np.power(x,2)
ver_simbo=[0, 1, np.power(α,1), np.power(α,2)]
#ver_simbo=[0, 1, α**1, α**2]

#generacion de matriz aleatoria
b = (A.tolist())
contador = len(b)**2
while contador > 1:
    for i in b:
        valor_aleatorio = random.choice(ver_simbo)
        indice_cambio = random.randint(0,len(i)-1)
        i[indice_cambio] = valor_aleatorio
    contador -= 1

matriz1=np.array(b)
#print(np.array(b))

#variables x1 a xn
x_inicial=[]
for i in range(n):
    x_inicial.append(S.symbols("x"+str(i)))
print(x_inicial)

#transformada







