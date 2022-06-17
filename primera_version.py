from hashlib import blake2b
from sympy import * 
import random 
import numpy as np
import copy


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

# Creación de índices
indices_V = [i for i in range(1,v+1)]
indices_O = [i for i in range(v+1,n+1)]


# Creación de variables vinagre
x_vinagre=[]                                    
for i in indices_V:
    x_vinagre.append(symbols("y"+str(i)))

# Creación de variables aceite
x_oil=[]                                    
for i in indices_O:
    x_oil.append(symbols("y"+str(i)))


"""generacion de llaves
del modelo Oil and Vinager"""

""" // Generación de los polinomios de vinagre y Aceite """

#primero definimos una funcion que cree los terminos del polinomio a crear
def sumatoriaPolinomica(V,O,campo): #V = x_vinagre, O= x_oil

    polinomios = []
    vv = []
    for i in V: #Nota: se está generando el doble producto, revisar entre todos 
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
        polinomios.append((random.choice(campo))*i)
    
    for i in O:
        polinomios.append((random.choice(campo))*i)

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

for i in F:
    print(i)
print("*******************")

####################################################################

""" Generación de la transformación lineal """

transformacion_lineal_0 = np.zeros((n,n)) 

# Se empieza la generacion de la matriz aleatoria
transformacion_lineal = (transformacion_lineal_0.tolist())

contador = len(transformacion_lineal)**2

while contador > 1:
    for i in transformacion_lineal:
        #vector de simbolos
        x= random.choice(campo) 
        ver_simbo=[0, 1, Mod(x,7), Mod(x**2,7)]     #DUDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        
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
TVariables = copy.deepcopy(x_inicial)
x_inicial = np.transpose(x_inicial)             # Creamos el vector X


# Obtenemos los polinomios pertenecientes a la transformación lineal
T = np.dot(x_inicial,transformacion_lineal) + aleatoria1

# Imprimimos cada uno de los polinomios
for i in T:
    print(i)

# Public Key -> Se compone la transformación lineal con los polinomios de aceite y vinagre (F o T)

FPublicKey = copy.deepcopy(F)

for i in range(o):              # Polinomios de F (OV)
    for j in range(n):          # Número de variables
        auxPolinom = FPublicKey[i]
        FPublicKey[i] = auxPolinom.subs((symbols("y"+str(j+1))), T[j])
        
    
print("******// Clave Pública // ******")
for i in FPublicKey:
    print(i)
    print("// ***** // ----- // ***** //")


""" Creación de la firma """

# La llave publica se iguala a su preimagen en el siguiente vector
#linsolve(F,x_vinagre+x_oil)

# Partimos de los polinomios de aceite y vinagre
FSignature = copy.deepcopy(F)

solutionValuesImage = []

# Evaluamos valores aleatorios para las variables vinagre
for i in range(v):
    solutionValuesImage.append(random.randint(1, 10))

for i in range(o):              # Polinomios de F (OV)
    for j in range(v):          # Número de variables de vinagre
        auxPolinom = FSignature[i]
        FSignature[i] = auxPolinom.subs((symbols("y"+str(j+1))), solutionValuesImage[j]) - int(hashstr[i])   # Incluimos la Imagen (HASH)
    

# Resolvemos el sistema lineal
solutionImage = solve((FSignature), x_oil)

# Obtenemos el vector con f^-1 para el mapeo central
for i in solutionImage:
    solutionValuesImage.append(float(solutionImage[i]))

#print("// ***** SIGNATURE ***** //")
for i in range(v):
    print(FSignature[i])
print("solutionValuesImage",solutionValuesImage)

# Partimos de la transformación lineal T
TSignature = copy.deepcopy(T)

# Le agregamos los terminos obtenidos con f^-1
for i in range(n):
    auxPolinom = TSignature[i]
    TSignature[i] = auxPolinom - solutionValuesImage[i]

print("TSIGNATURE")
for i in TSignature:
    print(i)

# Resolvemos el sistema lineal nxn para T^-1
solutionPreImage = solve((TSignature), TVariables)

ValuesPreImage = []

# Obtenemos el vector con T^-1 para la transformación
for i in solutionPreImage:
    ValuesPreImage.append(float(solutionPreImage[i]))

#print(" PRE-IMAGEN ")
print(ValuesPreImage)


""" Comprobación de la firma """

TestPublicKey = copy.deepcopy(FPublicKey)

for i in range(len(TestPublicKey)):              # Polinomios de F (OV)
    for j in range(n):                           # Número de variables
        auxPolinom = TestPublicKey[i]
        TestPublicKey[i] = auxPolinom.subs((symbols("x"+str(j+1))), ValuesPreImage[j])


for i in range(o):
    print(TestPublicKey[i] ,hashstr[i])