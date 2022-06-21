""" 
// ********** // Generación Firma Digital // ********** //

Programa que permite firmar digitalmente un mensaje, generación de las llaves públicas, privadas, y comprobación de las llaves


"""

from hashlib import blake2b
from sympy import * 
import random 
import numpy as np
import copy
from math import gcd
import sympy
from tabulate import tabulate
import pandas as pd

""" Parte 1.1 Creación del campo y sus términos enteros.
Para esto, se toma en cuenta la definicion de campo y enteros modulo m. """

# Mensaje de entrada del usuario, indicando el nombre del archivo de texto
nombreArchivo = input("ingrese nombre del documento: \n")

# Abrimos el archivo de texto para leerlo
archivoUsario = open(nombreArchivo, "r")
data = archivoUsario.read()

# Generación del hash para codificarlo 
message = blake2b(data.encode(), digest_size=1)
hash = int(message.hexdigest(),16)

# Imprimimos el valor del HASH
print("HASH GENERADO: ",hash)
# Convertimos el HASH a un string
hashstr = str(hash)

# Numero de ecuaciones y variables aceite
o = len(str(hashstr)) 

# Valor del módulo
m = 7

# Componentes finitos del campo
campo = [0,1,2,3,4,5,6]


"""
Parte 1.2 - Proceso de creacion de las vaiables Oil y Vinager de modo
que se puedan usar de manera independiente más adelante """

# Se genera un esquema balanceado vinagre/aceite
v = o       # numero de variables vinagre
n = o + v   # numero de variables totales

# Creación de subíndices
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


"""
Parte 2. - Generacion de llaves del modelo Oil and Vinager"""

"""  Parte 2.1 Generación de los polinomios de vinagre y Aceite """

# Primero definimos una funcion que cree los terminos de los polinomios

def sumatoriaPolinomica(V,O,campo): #V = x_vinagre, O= x_oil
    polinomios = []
    vv = []
    # Creación de términos cuadráticos VV
    for i in V: 
        for j in V:
            x = (random.choice(campo))*i*j
            vv.append(x)
            polinomios.append(x)
    ov = []
    # Creación de términos mixtos VO
    for i in V:
        for j in O:
            x = (random.choice(campo))*i*j
            ov.append(x)
            polinomios.append(x)
    # Creación de términos lineales V
    for i in V:
        polinomios.append((random.choice(campo))*i)
    # Creación de términos lineales O
    for i in O:
        polinomios.append((random.choice(campo))*i)
    # Creación de independientes
    polinomios.append(random.choice(campo))

    return polinomios


# Variables que contendrán las preimágenes
ans = 0
ansT = 0

# Contador para controlar los errores
iteracion = 0

# Ciclo que permite iterar hasta que se encuentre una solución que satisfaga al hash como producto de las llaves privadas

while ans == 0 or ansT == 0:

    # F contendrá los polinomios de OV
    F = []

    # Crear una lista con O polinomios usando Xn variables
    for i in range(o):
        f = 0
        for j in sumatoriaPolinomica(x_vinagre,x_oil,campo):
            f += j
        F.append(sympy.polys.polytools.trunc(f,m))              #Se garantiza que los polonomios sean módulo m

    F = np.array(F)     # Se genera un arreglo Numpy para manipular los datos

    """ 2.2 Generación de la transformación lineal """

    # Se inicializa una matriz de 0s de tamaño nxn
    transformacion_lineal_0 = np.zeros((n,n)) 

    # Se transforma la matriz de numpy en una lista de listas para su manipulación
    transformacion_lineal = (transformacion_lineal_0.tolist())

    # Variable para iterar nxn elementos
    contador = len(transformacion_lineal)**2

    # Se empieza la generacion de la matriz aleatoria
    while contador > 1:
        for fila in transformacion_lineal:

            # Se escoge un valor aleatorio del campo
            x = random.choice(campo) 
            # Se reemplaza el valor anterior en las potencial 0, 1, x, x**2 modulo m
            ver_simbo = [0, 1, Mod(x,m), Mod(x**2,m)]  
            # Se escoge un valor aleatorio de la anterior lista
            valor_aleatorio = random.choice(ver_simbo)
            # Se le asigna el valor a un elemento aleatorio de la fila
            indice_cambio = random.randint(0, len(fila)-1)
            fila[indice_cambio] = valor_aleatorio
        contador -= 1

    # Creación del vector de términos independientes de la transformación lineal
    terminosIndependientesT=[]
    for i in range(n):
        terminosIndependientesT.append(random.choice(ver_simbo))
    terminosIndependientesT = np.array(terminosIndependientesT)

    # Convertimos el arreglo en una matriz de numpy
    transformacion_lineal = np.array(transformacion_lineal)

    # Obtenemos las variables x1 a xn

    # Arreglo de varibles iniciales
    x_inicial=[]       

    for i in range(1,n+1):
        x_inicial.append(symbols("x"+str(i)))    # Creamos las xn variables
    
    TVariables = copy.deepcopy(x_inicial)        # Creamos una copia para la generación de la firma
    x_inicial = np.transpose(x_inicial)          # Creamos el vector Xn variables


    # Obtenemos los polinomios pertenecientes a la transformación lineal a través del producto punto, más la adición de los términos independientes
    T = np.dot(x_inicial, transformacion_lineal) + terminosIndependientesT

    for i in range(len(T)):
        T[i] = sympy.polys.polytools.trunc(T[i], 7)

    """ 2.3 - Generación de la llave pública. Se compone la transformación lineal con los polinomios de aceite y vinagre (F o T)"""

    # Se hace una copia de los polinomios de OV
    FPublicKey = copy.deepcopy(F)

    # Se reemplazan en los polinomios de aceite y vinagre, la transformación lineal (F o T) -> Cada vector de la transformación lineal se evalúa en los polinomios, tomará un valor de Xi hasta Xn, y se reemplazará en los polinomios como Xi a Xn respectivamente

    for i in range(o):              # Número de Polinomios de F (OV)
        for j in range(n):          # Número de variables Xn
            auxPolinom = FPublicKey[i]
            # Se sustituyen la variable Xi de cada uno de los polinomios por la el Vector iésimo de la transformada
            FPublicKey[i] = auxPolinom.subs((symbols("y"+str(j+1))), T[j])
            
    # Se asegura para la composición trabajar en módulo m
    for i in range(len(FPublicKey)):
        FPublicKey[i] = sympy.polys.polytools.trunc(FPublicKey[i], m)




    """ 3.0 - Creación de la firma """

    """ 3.1 - Partimos de los polinomios de aceite y vinagre para hallar un sistema homogéneo de ecuaciones, tomando como solución inicial la imagen (hash)"""

    # Se aumenta el contador para verificar errores
    iteracion += 1

    print("Número iteración: ", contador)

    # Si se llega a 1000 iteraciones, no es posible generar la firma para ese mensaje y se rompe el ciclo.
    if(iteracion >= 1000):
        print("ERROR")
        break

    # Se hace una copia de los polinomios OV
    FSignature = copy.deepcopy(F)

    solutionValuesImage = []

    # Se escogen V valores aleatorios
    for i in range(v):
        # Se escogen valores aleatorios de los representantes del campo finito
        solutionValuesImage.append(random.randint(1, 6))

    # Evaluamos los valores aleatorios anterios para las variables vinagre
    for i in range(o):                      # Polinomios de F (OV)
        for j in range(v):                  # Número de variables de vinagre
            auxPolinom = FSignature[i]
            # Reemplazamos la Xi variables por el iésimo valor aletorio
            FSignature[i] = auxPolinom.subs((symbols("y"+str(j+1))), solutionValuesImage[j]) - int(hashstr[i])   # Incluimos la Imagen (HASH), para convertirlo en un sistema homogéneo
        
    # Convertir el sistema a aritmética modular
    for i in range(len(FSignature)):
        FSignature[i] = sympy.polys.polytools.trunc(FSignature[i], m)

    # Generamos una copia para desarrollar la matriz
    FSignatureM = copy.deepcopy(FSignature)

    # Obtenemos la matriz a través de sympy, con la estructua de una matriz para los coeficientes de las variables, y una matriz para los términos independientes en el rango de O
    FSignaturaMatrix = sympy.linear_eq_to_matrix(FSignatureM, x_oil)

    # Solucionamos el sistema lineal con aritmetica modular
    det = int(FSignaturaMatrix[0].det())    # Obtenemos el determinante de la matriz de coeficientes de las variables
    
    # Se resuelve el sistema AX = B -> X = (A**-1)*B con A**-1 = (1/det(A))*A. Todo esto teniendo en cuenta la aritmetica modular
    if gcd(det, m) == 1:                                              
        ans = pow(det, -1, m) * FSignaturaMatrix[0].adjugate() @ FSignaturaMatrix[1] % m

    # Se evalúa si se encontró solución para el sistema. En caso de ser así, se ejecuta el IF
    if ans != 0: 

        # Obtenemos el vector con f^-1 para el mapeo central
        for solution in ans:
            # Se agrega la solución al siguiente vector
            solutionValuesImage.append(solution)

        """ 3.2 - Solución de la transformación lineal inversa, a partir de los valores hallados con la inversa de los polinomios OV, ubicados en el vector solutionValuesImage """

        # Partimos de la transformación lineal T
        TSignature = copy.deepcopy(T)

        # Le agregamos los terminos obtenidos con f^-1 (Polinomios OV)
        for i in range(n):
            auxPolinom = TSignature[i]
            # Incluimos las soluciones inversas de los Polinomios OV, para convertirlo en un sistema homogéneo
            TSignature[i] = auxPolinom - solutionValuesImage[i]

        # Convertir el sistema a aritmética modular
        for i in range(len(TSignature)):
            TSignature[i] = sympy.polys.polytools.trunc(TSignature[i], m)

        # Resolvemos el sistema lineal nxn para T^-1

        # Generamos una copia para desarrollar la matriz
        TSignatureM = copy.deepcopy(TSignature)

        # Obtenemos la matriz a través de sympy, con la estructua de una matriz para los coeficientes de las variables, y una matriz para los términos independientes en el rango de n
        TSignatureMatrix = sympy.linear_eq_to_matrix(TSignatureM, TVariables)

        # Se resuelve el sistema AX = B -> X = (A**-1)*B con A**-1 = (1/det(A))*A. Todo esto teniendo en cuenta la aritmetica modular
        det = int(TSignatureMatrix[0].det())
        if gcd(det, m) == 1:
            ansT = pow(det, -1, m) * TSignatureMatrix[0].adjugate() @ TSignatureMatrix[1] % m

        # Evaluamos si se encontró solución, y de ser el caso se sale del ciclo exitosamente.
        if(ansT != 0):
            break


# Se reorganiza la solución de las Xn variables obtenidas de la inversa de la transformada.
ValuesPreImage = []
for values in ansT:
    # Los valores están en una matriz, y se reorganizan en una lista
    ValuesPreImage.append(values)

#print(" PRE-IMAGEN ")
print(ValuesPreImage)



""" 4.0 - Comprobación de la firma """

# Se genera una copia de las llaves públicas (F o T)
TestPublicKey = copy.deepcopy(FPublicKey)

# Se evalúan los valores hallados con las llaves privadas (T^-1(F^-1(x))), en la llave pública (F o T)(x)
for i in range(len(TestPublicKey)):              # Polinomios llave pública FoT
    for j in range(n):                           # Número de variables
        # En cada polinomio FoT reemplazo la varriable Xi por los valores encontrados en (T^-1(F^-1(x)))
        TestPublicKey[i] = TestPublicKey[i].subs((symbols("x"+str(j+1))), ValuesPreImage[j])
        # Nos aseguramos de trabajarlo en aritmética modular
        TestPublicKey[i] = Mod((TestPublicKey[i]), m)

# Los elementos del hash se convierten en aritmética modular
for i in range(o):
    q = (int(hashstr[i])*len(hashstr[i]))/7 - TestPublicKey[i]
    n = (q + TestPublicKey[i])*m/len(hashstr[i])
    TestPublicKey[i] = int(np.round(float(n)))
    print(hashstr[i],TestPublicKey[i])

datos = {"Hash":list(hashstr), "PublicKey":TestPublicKey}
print(pd.DataFrame(datos))

"""resultados = [hashstr,TestPublicKey]
resultados = np.transpose(np.array(resultados))

print(resultados)
#resultados = np.transpose(resultados)
titulos = ["Hash", "PublicKey"]
print(tabulate(resultados,
               headers=titulos,  # Escogemos los titulos
               showindex=True,  # Agregamos indices para las iteraciones
               tablefmt="fancy_grid",  # Le damos estetica a la tabla
               stralign="center"))  # Centramos los resultados en la tabla"""