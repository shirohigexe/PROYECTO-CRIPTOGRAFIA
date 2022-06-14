from hashlib import blake2b
from sympy import * 
import random 
import numpy as np


"""creacion del campo y sus terminos enteros
para esto, se toma en cuenta la definicion de campo y enteros modulo m,
con esto tomamos 10 representantes de las clases de 
equivalencia"""

# Generación del hash para evaluar generar la llave 

message = blake2b(b'Esto es una prueba', digest_size = 1)
hash = int(message.hexdigest(),16)
#print(hash)
hashstr = str(hash)

#if (len(str(hash))%2 != 0):
#    hashstr = hashstr + str(9)

o = len(str(hashstr)) # numero de ecuaciones


campo = [0,1,2,3,4,5,6]


"""proceso de creacion de las vaiables Oil y Vinager de modo
que se puedan usar de manera independiente más adelante"""

v = o 
n = o + v # numero de variables 

indices_V = [i for i in range(1,v+1)]
indices_O = [i for i in range(v+1,n+1)]



x_vinagre=[]                                    
for i in indices_V:
    x_vinagre.append(symbols("x"+str(i)))

x_oil=[]                                    
for i in indices_O:
    x_oil.append(symbols("x"+str(i)))


"""generacion de llaves
del modelo Oil and Vinager"""


#primero definimos una funcion que cree los terminos del polinomio a crear
def sumatoriaPolinomica(V,O,campo): #V = x_vinagre, O= x_oil

    polinomios = []
    vv = []
    for i in V: #Nota: se está generando el oble producto, revisar entre todos 
        for j in V:
            x = (random.choice(campo))*i*j
            vv.append(x)
            polinomios.append(x)
    ov = []
    for i in V:
        for j in O:
            x = (random.choice(campo))*i*j
            ov.append(x)
            polinomios.append(x)
    
    for i in V:
        polinomios.append((random.choice(campo))*i*j)
    
    for i in O:
        polinomios.append((random.choice(campo))*i*j)

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

print("*******************")
#print(F)

####################################################################
transformacion_lineal_0 = np.zeros((n,n)) 

# Se empieza la generacion de la matriz aleatoria
transformacion_lineal = (transformacion_lineal_0.tolist())

contador = len(transformacion_lineal)**2

while contador > 1:
    for i in transformacion_lineal:
        #vector de simbolos
        x= random.choice(campo) 
        ver_simbo=[0, 1, Mod(x,7), Mod(x**2,7)]
        
        valor_aleatorio = random.choice(ver_simbo)
        indice_cambio = random.randint(0,len(i)-1)
        i[indice_cambio] = valor_aleatorio
    contador -= 1

aleatoria1=[]
for i in range(n):
    aleatoria1.append(random.choice(ver_simbo))
aleatoria1=np.array(aleatoria1)


# Convertimos el arreglo en una matriz de numpy
transformacion_lineal = np.array(transformacion_lineal)

# Obtenemos las variables x1 a xn
x_inicial=[]                                    # Arreglo de varibles iniciales
for i in range(1,n+1):
    x_inicial.append(symbols("x"+str(i)))    # Creamos las xn variables
x_inicial = np.transpose(x_inicial)             # Creamos el vector X


# Obtenemos los polinomios pertenecientes a la transformación lineal
T = np.dot(x_inicial,transformacion_lineal) + aleatoria1

for i in T:
    print(i)

print("*************")

# Public Key -> Se compone la transformación lineal con los polinomios de aceite y vinagre (F o T)

for i in range(o):              # Polinomios de F (OV)
    for j in range(n):          # Número de variables
        auxPolinom = F[i]
        F[i] = auxPolinom.subs((symbols("y"+str(j+1))), T[j])
        
    
print("******// Clave Pública // ******")
for i in F:
    print("// ***** Polinomios ***** //")
    print(i)


# la llave pueblica se iguala a su preihmagen en el sigueinte vector
#linsolve(F,x_vinagre+x_oil)