import sympy as S 
import random 

#campo finito
from pyfinite import ffield

valor_primo=[3, 5, 7]
valor_campo=random.choice(valor_primo)
F = ffield.FField(valor_campo) 
#help(ffield.FField)
print(valor_campo)
print(F.ShowPolynomial(valor_campo))



#matriz aleatoria
import numpy as np
#crear un array numpy con ceros
A = np.zeros((valor_campo-1,valor_campo-1))
print(A)
#vector de simbolos
x= S.symbols('x')
#np.power(x,2)
ver_simbo=[0, 1, np.power(x,1), np.power(x,2)]


b = (A.tolist())
contador = len(b)**2
while contador > 1:
    for i in b:
        valor_aleatorio = random.choice(ver_simbo)
        indice_cambio = random.randint(0,len(i)-1)
        i[indice_cambio] = valor_aleatorio
    contador -= 1

print(np.array(b))







