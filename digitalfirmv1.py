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
ver_simbo=[0, 1, np.power(x,1), np.power(x,2)]

α= S.symbols('α')                               # Se genera un vector de simbolos
#np.power(x,2)
ver_simbo=[0, 1, np.power(α,1), np.power(α,2)]
#ver_simbo=[0, 1, α**1, α**2]

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
#print(x_inicial)

# Obtenemos los polinomios pertenecientes a la transformación lineal
polinomiosFTransLineal = transformacion_lineal.dot(x_inicial)
for i in range(n):
    print(polinomiosFTransLineal[i])


#// ***** // Paso 2. Creación de los polinomios de vinagre y aceite // ***** // #
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

#// ***** // Paso 3. Composicion // ***** // #