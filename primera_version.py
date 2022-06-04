from typing import Counter
import sympy as S 
import random 
import numpy as np
from pyfinite import ffield 

q = 7
def campo(q):
    campo_elementos = []
    campo = []
    for i in range(q): #i toma valores de 0-(q-1)
        clase_equivalencia = []
        for j in range(10):  # i = j mod q -> j-i=mq
            if (j-i) % q == 0:
                clase_equivalencia.append(j)
                campo_elementos.append(j)
        campo.append(clase_equivalencia)
    return campo_elementos

campo = campo(q)
print(campo)




o = 2 # numero de ecuaciones
v = o 
n = o + v # numero de variables 

indices_V = [i for i in range(1,v+1)]
indices_O = [i for i in range(v+1,n+1)]
print(indices_V)
print(indices_O)



x_vinagre=[]                                    
for i in indices_V:
    x_vinagre.append(S.symbols("x"+str(i)))
print(x_vinagre)

x_oil=[]                                    
for i in indices_O:
    x_oil.append(S.symbols("x"+str(i)))
print(x_oil)

"""generacion de llaves
del modelo Oil and Vinager"""

def sumatoriaPolinomica(V,O,campo): #V = x_vinagre, O= x_oil

    polinomios = []
    vv = []
    for i in V: #Nota: se está generando el oble producto, revisar entre todos 
        for j in V:
            vv.append(random.choice(campo)*i*j)
            polinomios.append(random.choice(campo)*i*j)
    ov = []
    for i in V:
        for j in O:
            ov.append(random.choice(campo)*i*j)
            polinomios.append(random.choice(campo)*i*j)
    

    return polinomios


print(sumatoriaPolinomica(x_vinagre,x_oil,campo))
