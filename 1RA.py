"""
Programa para generar la llave pública y privada

Se necesitan instalar las librerías sympy, random, pyfinite y numpy.
"""

from typing import Counter
import sympy as S 
import random 
import numpy as np
from pyfinite import ffield      # campo finito

#campo finito
from pyfinite import ffield

#n = int(input("ingrese el numero primo que desea: "))

valor_primo=[2,3,5,7]
valor_campo=random.choice(valor_primo)
F = ffield.FField(valor_campo) 
#help(ffield.FField)
#print(valor_campo)
#print(F.ShowPolynomial(valor_campo))

#// ***** // Paso 1. Creación de la matriz para la transformación lineal // ***** // #

n=6                                             #tamaño del numero a codificar
transformacion_lineal_0 = np.zeros((n,n))       #crear un array numpy con ceros de tamaño nxn
#print(transformacion_lineal_0)

#matriz aleatoria
import numpy as np
#lectura de hash
n=5
#crear un array numpy con ceros
A = np.zeros((n,n))
#vector de simbolos
x= S.symbols('x')
#np.power(x,2)
ver_simbo=[0, 1, x, x**2]

# Se empieza la generacion de la matriz aleatoria
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
#print(transformacion_lineal)

# Obtenemos las variables x1 a xn
x_inicial=[]                                    # Arreglo de varibles iniciales
for i in range(n+1):
    x_inicial.append(S.symbols("x"+str(i)))    # Creamos las xn variables
x_inicial = np.transpose(x_inicial)             # Creamos el vector X
print(x_inicial)
#print(x_inicial)

T = []
# Obtenemos los polinomios pertenecientes a la transformación lineal
polinomiosFTransLineal = transformacion_lineal.dot(x_inicial)
for i in range(n):
    T.append(polinomiosFTransLineal[i])
    print(polinomiosFTransLineal[i])


#// ***** // Paso 2. Creación de los polinomios de vinagre y aceite // ***** // #

    




