from typing import Counter
import sympy as S 
import random 
import numpy as np

"""creacion del campo y sus terminos enteros
para esto, se toma en cuenta la definicion de campo y enteros modulo m,
con esto tomamos 10 representantes de las clases de 
equivalencia"""
q = [2,3,5,7,11]

valor = random.choice(q)

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

campo = campo(valor)
print(campo)


"""proceso de creacion de las vaiables Oil y Vinager de modo
que se puedan usar de manera independiente más adelante"""

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


#primero definimos una funcion que cree los terminos del polinomio a crear
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
    
    for i in V:
        polinomios.append(random.choice(campo)*i)
    
    for i in O:
        polinomios.append(random.choice(campo)*i)

    polinomios.append(random.choice(campo))

    return polinomios

F = []

#crear una lista con o polinomios usando la definicion anterior
for i in range(o):
    f = 0
    for j in sumatoriaPolinomica(x_vinagre,x_oil,campo):
        f += j
    F.append(f)

F = np.array(F)
print(F)

####################################################################
transformacion_lineal_0 = np.zeros((n,n)) 
#vector de simbolos
x= S.symbols('a')
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

aleatoria1=[]
for i in range(n):
    aleatoria1.append(random.choice(ver_simbo))
print(aleatoria1)
aleatoria1=np.array(aleatoria1)

# Convertimos el arreglo en una matriz de numpy
transformacion_lineal = np.array(transformacion_lineal)
print(transformacion_lineal)
#print(transformacion_lineal)

# Obtenemos las variables x1 a xn
x_inicial=[]                                    # Arreglo de varibles iniciales
for i in range(1,n+1):
    x_inicial.append(S.symbols("x"+str(i)))    # Creamos las xn variables
x_inicial = np.transpose(x_inicial)             # Creamos el vector X
print(x_inicial)
#print(x_inicial)


# Obtenemos los polinomios pertenecientes a la transformación lineal
T = np.dot(x_inicial,transformacion_lineal) + aleatoria1

print(T)


"""private key
NOTA: no sé de donde sacar T:Fn -> Fn"""

