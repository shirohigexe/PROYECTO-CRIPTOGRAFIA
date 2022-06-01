"""
Programa para generar la llave pública y privada
"""

from typing import Counter
import sympy as S 
import random 
from pyfinite import ffield      # campo finito

valor_primo     = [3, 5, 7]                     # Posibles valores para escoger el campo
valor_campo     = random.choice(valor_primo)    # Se escoge el primo para el campo
F = ffield.FField(valor_campo)                  # Se crea el campo
#help(ffield.FField)
#print(valor_campo)
#print(F.ShowPolynomial(valor_campo))


#tamaño del numero a codificar
n=6 

#matriz aleatoria
import numpy as np

#crear un array numpy con ceros
transformacion_lineal_0 = np.zeros((n,n))
print(transformacion_lineal_0)
a = np.sum(transformacion_lineal_0, axis=0)
print(a)
print(a[1])
#vector de simbolos
α= S.symbols('α')
#np.power(x,2)
ver_simbo=[0, 1, np.power(α,1), np.power(α,2)]
#ver_simbo=[0, 1, α**1, α**2]

#generacion de matriz aleatoria
transformacion_lineal = (transformacion_lineal_0.tolist())
contador = len(transformacion_lineal)**2
while contador > 1:
    for i in transformacion_lineal:
        valor_aleatorio = random.choice(ver_simbo)
        indice_cambio = random.randint(0,len(i)-1)
        i[indice_cambio] = valor_aleatorio
    contador -= 1

# Convertimos el arreglo en una matriz de numpy
transformacion_lineal = np.array(transformacion_lineal)
print(transformacion_lineal)

#variables x1 a xn
x_inicial=[]                                    # Arreglo de varibles iniciales
for i in range(n):
    x_inicial.append(S.symbols("x"+str(i)))     # Creamos las xn variables
x_inicial = np.transpose(x_inicial)             # Creamos el vector X
print(x_inicial)

#transformada
print("*************RESULTADO**************")
print(transformacion_lineal*x_inicial)
print("*************RESULTADO**************")
print(np.transpose(transformacion_lineal*x_inicial))
print("POLIX")
print(np.sum(np.transpose(transformacion_lineal*x_inicial), axis=0))
print("DOT PRODUCT")
print(transformacion_lineal.dot(x_inicial))






