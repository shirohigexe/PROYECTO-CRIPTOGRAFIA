import hashlib

archivo = open('prueba.txt', 'r')
print(archivo.read())

########creacion de hash###########

"""se crea un hash con 256 caracteres (en binario)
que utilizaremos para definir  o=numero de variables"""
Hash = hashlib.sha256()
Hash.update(b'prueba.txt')
print(Hash.hexdigest())

########creacion de variables para las keys########
