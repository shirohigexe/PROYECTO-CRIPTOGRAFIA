from math import gcd
from hashlib import blake2b
from sympy import * 
import random 
import numpy as np
import copy
from math import gcd
import sympy


"""creacion del campo y sus terminos enteros
para esto, se toma en cuenta la definicion de campo y enteros modulo m,
con esto tomamos 10 representantes de las clases de 
equivalencia"""

# Generación del hash para evaluar generar la llave 

message = blake2b(b'Buenos dias sennnnnnnnnnnnnnnasdasdasdasdadasdfjghjghjghqwejqwiueyquweyuqwyeuqyowuieqyor profesorrrrr', digest_size = 1)
hash = int(message.hexdigest(),16)
#print(hash)
hashstr = str(hash)

#if (len(str(hash))%2 != 0):
#    hashstr = hashstr + str(9)

o = len(str(hashstr)) # numero de ecuaciones

# Módulo 7
m = 7

# Variables iteración
ans = 0
ansT = 0
iteracion = 0

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

while ans == 0 or ansT == 0:

    F = []

    #crear una lista con o polinomios usando la definicion anterior
    for i in range(o):
        f = 0
        for j in sumatoriaPolinomica(x_vinagre,x_oil,campo):
            f += j
        F.append(sympy.polys.polytools.trunc(f,7))

    F = np.array(F)

    """for i in F:
        print(i)
    print("*******************")"""

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

    for i in range(len(T)):
        T[i] = sympy.polys.polytools.trunc(T[i], 7)

    # Imprimimos cada uno de los polinomios
    """for i in T:
        print(i)"""

    # Public Key -> Se compone la transformación lineal con los polinomios de aceite y vinagre (F o T)

    FPublicKey = copy.deepcopy(F)


    for i in range(o):              # Polinomios de F (OV)
        for j in range(n):          # Número de variables
            auxPolinom = FPublicKey[i]
            FPublicKey[i] = auxPolinom.subs((symbols("y"+str(j+1))), T[j])
            
        
    for i in range(len(FPublicKey)):
        FPublicKey[i] = sympy.polys.polytools.trunc(FPublicKey[i], 7)

    print("******// Clave Pública // ******")
    """for i in FPublicKey:
        print(i)
        print("// ***** // ----- // ***** //")"""


    """ Creación de la firma """

    # La llave publica se iguala a su preimagen en el siguiente vector
    #linsolve(F,x_vinagre+x_oil)

    # Partimos de los polinomios de aceite y vinagre


#************************************************************

    iteracion += 1
    print(iteracion,ans,ansT)

    if(iteracion >= 1000):
        print("ERROR")
        break

    FSignature = copy.deepcopy(F)

    solutionValuesImage = []

    # Evaluamos valores aleatorios para las variables vinagre
    for i in range(v):
        solutionValuesImage.append(random.randint(1, 6))# se corrigio el 10 pues la solucion debe realizarse en los numeros de los modulos

    for i in range(o):                      # Polinomios de F (OV)
        for j in range(v):                  # Número de variables de vinagre
            auxPolinom = FSignature[i]
            FSignature[i] = auxPolinom.subs((symbols("y"+str(j+1))), solutionValuesImage[j]) - int(hashstr[i])   # Incluimos la Imagen (HASH)
        
    # Convertir el sistema a aritmética modular
    for i in range(len(FSignature)):
        FSignature[i] = sympy.polys.polytools.trunc(FSignature[i], 7)

    # Generamos una copia para desarrollar la matriz
    FSignatureM = copy.deepcopy(FSignature)

    # Obtenemos la matriz
    FSignaturaMatrix = sympy.linear_eq_to_matrix(FSignatureM, x_oil)

    # Solucionamos el sistema lineal con aritmetica modular
    det = int(FSignaturaMatrix[0].det())
    if gcd(det, m) == 1:                                               ########***************
        ans = pow(det, -1, m) * FSignaturaMatrix[0].adjugate() @ FSignaturaMatrix[1] % m

    if ans != 0: 
        # Obtenemos el vector con f^-1 para el mapeo central
        #print("SOLUCIONF", ans)
        for solution in ans:
            solutionValuesImage.append(solution)

        #print("// ***** SIGNATURE ***** //")
        """for i in range(v):
            print(FSignature[i])"""

        #print("solutionValuesImage",solutionValuesImage)

        # Partimos de la transformación lineal T
        TSignature = copy.deepcopy(T)

        # Le agregamos los terminos obtenidos con f^-1
        for i in range(n):
            auxPolinom = TSignature[i]
            TSignature[i] = auxPolinom - solutionValuesImage[i]

        # Convertir el sistema a aritmética modular
        for i in range(len(TSignature)):
            TSignature[i] = sympy.polys.polytools.trunc(TSignature[i], m)

        """print("TSIGNATURE")
        for i in TSignature:
            print(i)"""

        # Resolvemos el sistema lineal nxn para T^-1

        # Generamos una copia para desarrollar la matriz
        TSignatureM = copy.deepcopy(TSignature)

        # Obtenemos la matriz
        TSignatureMatrix = sympy.linear_eq_to_matrix(TSignatureM, TVariables)

        # Solucionamos el sistema lineal con aritmetica modular
        det = int(TSignatureMatrix[0].det())
        if gcd(det, m) == 1:  # ***************
            ansT = pow(det, -1, m) * TSignatureMatrix[0].adjugate() @ TSignatureMatrix[1] % m

        if(ansT != 0):
            break

ValuesPreImage = []

print("SOLUCION T", ansT)
# Obtenemos el vector con T^-1 para la transformación
for values in ansT:
    ValuesPreImage.append(values)

#print(" PRE-IMAGEN ")
print(ValuesPreImage)


""" Comprobación de la firma """

TestPublicKey = copy.deepcopy(FPublicKey)

for i in range(len(TestPublicKey)):              # Polinomios de F (OV)
    for j in range(n):                           # Número de variables
        auxPolinom = TestPublicKey[i]
        TestPublicKey[i] = auxPolinom.subs((symbols("x"+str(j+1))), ValuesPreImage[j])
        TestPublicKey[i] = Mod((TestPublicKey[i]), m)

for i in range(o):
    q = (int(hashstr[i])*len(hashstr[i]))/7 - TestPublicKey[i]
    n = (q + TestPublicKey[i])*m/len(hashstr[i])
    print(TestPublicKey[i], hashstr[i], int(np.round(float(n))))


"""(n*len(hashstr[i]))%7 = k
n = k
(8*2)%7 = 2

a/b = q + m

(n*len(hashstr[i]))/7 = q + TestPublicKey[i]"""


