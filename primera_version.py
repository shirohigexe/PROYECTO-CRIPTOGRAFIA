from typing import Counter
import sympy as S 
import random 
import numpy as np
from pyfinite import ffield 

q = 7
def campo(q):
    campo_elementos = []
    campo = []
    for i in range(q): #i toma valores de 0-q
        clase_equivalencia = []
        for j in range(100):  # i = j mod q -> j-i=mq
            if (j-i) % q == 0:
                clase_equivalencia.append(j)
                campo_elementos.append(j)
        campo.append(clase_equivalencia)
    return campo_elementos 

campo = campo(q)
print(campo)




o = 6 # numero de ecuaciones
v = o 

"""F = ffield.FField(q)
valor_campo=random.choice(F)
print(valor_campo)
print(F.ShowCoefficients(500))"""

n = o + v # numero de variables 

indices_V = [i for i in range(1,v+1)]
indices_O = [i for i in range(v+1,n+1)]

x_vinagre=[]                                    
for i in indices_V:
    x_vinagre.append(S.symbols("x"+str(i)))
print(x_vinagre)

x_oil=[]                                    
for i in indices_O:
    x_oil.append(S.symbols("x"+str(i)))
print(x_oil)

#def polinomios(terminosOil,terminosVinager):
