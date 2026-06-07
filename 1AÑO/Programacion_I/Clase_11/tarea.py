import random
from datetime import datetime, timedelta

"""
Definir una función ‘lista_de_minimos’ que, dadas dos listas de igual longitud, compuestas por
números, devuelva como resultado una nueva lista que contenga en cada posición el menor entre los
elementos correspondientes de ambas listas.
Ejemplo:
Lista A = [1, 3, 5, 8, 3, 7, 7, 9, 0, 8]
Lista B = [6, 7, 5, 7, 5, 8, 3, 6, 1, 1]
Resultado = [1, 3, 5, 7, 3, 7, 3, 6, 0, 1]
"""

def contador_pares(numeros: list, limite_pares: int) -> int:
    posicion = 0
    cantidad_pares = 0

    while posicion < len(numeros) and cantidad_pares != limite_pares:
        
        if es_par(numeros[posicion]):
            cantidad_pares += 1
        posicion += 1
    
    if cantidad_pares != limite_pares:
        cantidad_pares = 0
    
    return cantidad_pares

def contador_vocales(palabra: str, limite_vocales: int) -> int:
    posicion = 0
    cantidad_vocales = 0
    vocales_encontradas = ""

    while posicion < len(palabra) and cantidad_vocales != limite_vocales:
        
        if es_vocal(palabra[posicion]) and palabra[posicion] not in vocales_encontradas:
            vocales_encontradas += palabra[posicion]
            cantidad_vocales += 1
        posicion += 1
    
    if cantidad_vocales != limite_vocales:
        cantidad_vocales = 0
    
    return cantidad_vocales

def es_par(numero) -> bool:
    return numero % 2 == 0

def es_menor(numero_1: int, numero_2: int) -> bool:
    return numero_1 <= numero_2

def es_vocal(letra: str) -> bool:
    return letra in 'aeiouáéíóú'

def lista_de_minimos(lista_1: list, lista_2: list) -> list:
    lista_nueva = []

    for i in range(len(lista_1)):
        if es_menor(lista_1[i],lista_2[i]):
            lista_nueva.append(lista_1[i])
        else:
            lista_nueva.append(lista_2[i])
    return lista_nueva

"""
En una lista de palabras quiero saber cuántas de ellas empiezan con una vocal.
Ejemplo con palabras que no empiezan con vocal:
palabras_uno = ["arbol", "casa", "elefante", "perro", "ciencia", "gato", "oceano", "util"]
Resultado 4
"""

def cuantas_empiezan_vocal(lista_palabras: list) -> int:
    contador = 0
    for palabra in lista_palabras:
        if es_vocal(palabra[0]):
            contador += 1
    return contador


def cuantas_terminan_vocal(lista_palabras: list) -> int:
    contador = 0
    for palabra in lista_palabras:
        if es_vocal(palabra[-1]):
            contador += 1
    return contador

def cuantas_almenos_tres_vocales(lista_palabras: list) -> int:
    contador = 0

    for palabra in lista_palabras:
        if contador_vocales(palabra, 3):
            contador += 1

    return contador

def cuantos_almenos_tres_pares(lista_numeros: list) -> int:
    contador = 0

    for lista in lista_numeros:
        if contador_pares(lista,3):
            contador += 1

    return contador  


"""
¿Empiezan todas las palabras con vocal?
En una lista de palabras quiero saber si todas ellas empiezan con una vocal.
"""
def todas_empiezan_con_vocal(lista_palabras: list) -> bool:
    vocales = 'aáeéiíoóuú'
    return all(palabra[0].lower() in vocales for palabra in lista_palabras)

def todas_terminan_con_vocal(lista_palabras: list) -> bool:
    vocales = 'aáeéiíoóuú'
    return all(palabra[-1].lower() in vocales for palabra in lista_palabras)

def alguna_palabra_tiene_cantidad_vocales(lista_palabras: list, limite_vocales) -> bool:
    existe_palabra = False
    posicion = 0

    while existe_palabra == False and posicion < len(lista_palabras):
        if contador_vocales(lista_palabras[posicion], limite_vocales):
            existe_palabra = True
        posicion += 1 
    
    return existe_palabra

def toda_lista_tiene_cantidad_pares(lista_numeros: list, limite_pares) -> bool:
    lista_con_pares = True
    posicion = 0

    while lista_con_pares == True and posicion < len(lista_numeros):
        if not contador_pares(lista_numeros[posicion], limite_pares):
            lista_con_pares = False
        posicion += 1 
    
    return lista_con_pares

"""
¿Hay alguna de columna en la que sean todos pares?
"""
def alguna_columna_son_pares(lista_numeros: list) -> bool:
    lista_con_pares = False
    posicion = 0

    while lista_con_pares == False and posicion < len(lista_numeros):
        if contador_pares(lista_numeros[posicion], len(lista_numeros[posicion])):
            lista_con_pares = True
        posicion += 1 
    
    return lista_con_pares

"""
¿Empiezan todas las palabras con vocal?
En una lista de palabras quiero eliminar todas las que no empiezan con una vocal.
"""

def filtrar_palabras_que_no_empiezan_con_vocal(lista_palabras: list) -> list:
    empiezan_con_vocal = []

    for palabra in lista_palabras:
        if es_vocal(palabra[0]):
            empiezan_con_vocal.append(palabra)
        
    lista_palabras = empiezan_con_vocal
    return lista_palabras

def filtrar_palabras_que_tengan_cantidad_vocales(lista_palabras: list, limite_vocales) -> list:
    tienen_cantidad_vocales = []
    posicion = 0

    for palabra in lista_palabras:
        if not contador_vocales(palabra,limite_vocales):
            tienen_cantidad_vocales.append(palabra)
    
    lista_palabras = tienen_cantidad_vocales
    return lista_palabras

def eliminar_columna_todos_pares_de_lista(lista_numeros: list) -> list:
    lista_con_pares = False
    posicion = 0

    while lista_con_pares == False and posicion < len(lista_numeros):
        if contador_pares(lista_numeros[posicion], len(lista_numeros[posicion])):
            lista_numeros.pop(posicion)
            lista_con_pares = True
        posicion += 1 
    
    return lista_numeros

# Integración: Crear, Contar y Buscar

"""
Cumpleaños en el mismo día
Voy a hacer mi fiesta de cumple. En mi grupo somos en total 23 personas. La tradición indica que se
canta el cumpleaños feliz a todas las personas que cumplan el mismo día. ¿Cuántas veces tendré que
cantar el feliz cumple el día de mi cumpleaños? Contar la cantidad de cumples mi mismo día.
Este valor puede estimarse generando muestras aleatorias para los 22 cumpleaños restantes. Si en esa
lista de fechas de cumpleaños, alguien cumple el mismo día que yo, cantamos una vez más el cumple
para esa otra persona.
Pista: consulte la función randint del módulo random.
Otra pista: los números del año considerarlos 365 (no contaremos los que cumplen el 29 de febrero).
Versión 2: Buscar si en la lista de 23 cumpleaños hay 2 cumples el mismo día. Devolver Verdadero o
Falso. O bien devolver el día que coinciden.
"""
def generar_lista_cumpleaños(personas, tu_cumpleaños):
    lista_cumpleaños = []
    lista_cumpleaños.append(tu_cumpleaños)
    for _ in range(personas):
        lista_cumpleaños.append(random.randint(1,10))
    return lista_cumpleaños

def cuantos_cumplen_mismo_dia_que_yo(lista_cumpleaños):
    contador_mismo_dia = 0
    posicion = 1
    while posicion < len(lista_cumpleaños):
        if lista_cumpleaños[0] == lista_cumpleaños[posicion]:
            contador_mismo_dia += 1
        posicion += 1
    return contador_mismo_dia

def cuantos_cumplen_mismo_dia(lista_cumpleaños):
    coinciden_cumpleaños = []
    posicion = 0
    posicion_siguiente = 1
    print(lista_cumpleaños)

    while posicion < len(lista_cumpleaños) -1: #recorre lista hasta la posicion final -1 porque tiene que compararse con el que sigue. 
        while posicion_siguiente < len(lista_cumpleaños) and lista_cumpleaños[posicion] not in coinciden_cumpleaños: #recorre hasta el final porque los vamos a comparar con el "principal" y tambien sólo recorre si ya el numero principal no está en la lista que coincide cumpleaños así no lo usamos para comparar.
            if lista_cumpleaños[posicion] == lista_cumpleaños[posicion_siguiente]:
                coinciden_cumpleaños.append(lista_cumpleaños[posicion])
            posicion_siguiente += 1
        posicion += 1
        posicion_siguiente = posicion + 1
    return coinciden_cumpleaños  

def cumpleaños_en_el_mismo_dia(personas, tu_cumpleaños):
    lista_cumpleaños = generar_lista_cumpleaños(personas, tu_cumpleaños)
    return cuantos_cumplen_mismo_dia(lista_cumpleaños)


#Mastermind

def generar_codigo_secreto():
    codigo_secreto = ""
    for _ in range(4):
        codigo_secreto += random.choice("RVAN")
    return codigo_secreto

def menu(codigo_secreto, intentos, pistas_negras, pistas_blancas):
    print("------------------------")
    print("Bienvenido a Mastermind!")
    print("Codigo: ????")
    print(f"Te quedan {intentos} intentos")
    print("Pistas: ")
    print("Negras: ", pistas_negras)
    print("Blancas: ", pistas_blancas)
    codigo_usuario = input("Ingrese color (R-V-A-N): ").upper()
    
    while len(codigo_usuario) != len(codigo_secreto) or not all(color in "RVAN" for color in codigo_usuario):
        print("Codigo incorrecto. Ingrese un codigo válido (R-V-A-N): ")
        codigo_usuario = input("Ingrese color (R-V-A-N): ").upper()
    return codigo_usuario

def verificar_color(codigo_secreto, codigo_usuario, pistas_negras, pistas_blancas):
    pistas_negras = 0
    pistas_blancas = 0
    print(codigo_usuario)
    print(codigo_secreto)
    for posicion in range(len(codigo_secreto)):
        if codigo_usuario[posicion] == codigo_secreto[posicion]:
                pistas_negras += 1
        elif codigo_secreto.count(codigo_usuario[posicion]):
            pistas_blancas += 1
    
    return pistas_negras, pistas_blancas


def mastermind(intentos):
    pistas_negras = 0
    pistas_blancas = 0
    codigo_usuario = ''
    codigo_secreto = generar_codigo_secreto()
    while intentos != 0 and pistas_negras != 4:
        codigo_usuario = menu(codigo_secreto,intentos, pistas_negras, pistas_blancas)
        pistas_negras, pistas_blancas = verificar_color(codigo_secreto,codigo_usuario,pistas_negras,pistas_blancas)
        print(pistas_negras,pistas_blancas)
        intentos -= 1
    if intentos == 0 and pistas_negras != 4:
        print("--------------------------------------")
        print("Perdiste! Se te acabaron los intentos.")
        print("--------------------------------------")
    else:
        print("--------------------------------------")
        print(f"Ganaste! El codigo es: {codigo_usuario}.")
        print("--------------------------------------")





lista_1 = [1, 3, 5, 8, 3, 7, 7, 9, 0, 8]
lista_2 = [6, 7, 5, 7, 5, 8, 3, 6, 1, 1]
lista_numeros = [[1,2,3], [1,2,2,1,2], [4,4,1,5,5,5], [2,3,8,6]]
lista_numeros_2 = [[2,4,4,1], [2,2,4,4,1,6], [4,4,2], [2,8,2]]
palabras = ["arbol", "casa", "elefante", "perro", "ciencia", "gato", "oceano", "util"]
palabras_2 = ['arboleda', "amapola", "ígnea"]

#print(lista_de_minimos(lista_1,lista_2))
#print(cuantas_terminan_vocal(palabras))
#print(cuantas_almenos_tres_vocales(palabras))
#print(cuantos_almenos_tres_pares(list_numeros))
#print(cumpleaños_en_el_mismo_dia(22,5))
print(mastermind(4))
#print()