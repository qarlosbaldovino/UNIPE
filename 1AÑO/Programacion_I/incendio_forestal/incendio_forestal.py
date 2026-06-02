import random
import matplotlib.pyplot as plt

"""
Genera una lista de n bosques vacíos.
Todos sus valores son 0.
"""
def bosque_vacio(n):
    bosque = []
    bosque.extend([0] * n)
    return bosque


"""
Genera una lista de n bosques.
Todos sus valores son 0 y 1 aleatoriamente.
"""
def bosque_limpio(n):
    bosque = []
    bosque = [random.randint(0, 1) for _ in range(n)]
    return bosque


"""
Genera una lista de n bosques.
Todos sus valores son 0,1 y -1 aleatoriamente.
"""
def bosque_quemado(n):
    bosque = []
    bosque = [random.randint(-1, 1) for _ in range(n)]
    return bosque


"""
Retorna un valor booleano por una comparación.
- random.random() genera un numero flotante entre el 0 y el 1.
- prob es la probabilidad que pasamos como parámetro.
- retorna True si el numero generado es menor a la probabilidad. 
- retorna Falso si el numero generado es mayor a la probabilidad.
"""
def suceso_aleatorio(prob):
    return random.random() < prob


"""
Modifica un bosque modificando los valores 0 al 1  de sus elementos
siempre y cuando de True la funcion suceso_aleatorio.
En caso de que exista un arbol, queda como está. 
"""
def brotes(bosque, p):
    for i in range(len(bosque)):
        if bosque[i] == 1 or suceso_aleatorio(p):
            bosque[i] = 1
        else:
            bosque[i] = 0
    return bosque


"""
Cuenta cuantos de un tipo determinado de arbol dependiendo el valor que le pasemos como parámetro.
- (1) Cuenta todos los arboles sanos del bosque.
- (0) Cuenta los espacios vacios en el bosque
- (-1) Cuenta los arboles quemados en el bosque.
"""
def cuantos(bosque, tipo_celda):
    return bosque.count(tipo_celda)

"""
Quema un arbol mientras se cumpla la probabilidad de suceso_aleatorio 
y además exista un arbol (no quedamo) en esa posición.
"""
def rayos(bosque, f):
    for i in range(len(bosque)):
        if bosque[i] == 1 and suceso_aleatorio(f):
            bosque[i] = -1
    return bosque


"""
Propaga un incendio por medio de un arbol quemado.
En caso de exista un arbol no-quemado a su lado, se quemará.
En caso de que no haya un arbol (0) a su lado, no se expande el fuego por esa zona.
"""
def propagacion(bosque):
    hubo_cambios = True

    while hubo_cambios:
        hubo_cambios = False

        for i in range(len(bosque)):
            if bosque[i] == 1:
                if (i > 0 and bosque[i - 1] == -1) or \
                   (i < len(bosque) - 1 and bosque[i + 1] == -1):
                    bosque[i] = -1
                    hubo_cambios = True

    return bosque


"""
Se limpian todos los arboles quemados.
Modifica el bosque cambiando los valores -1 a 0.
"""
def limpieza(bosque):
    for i in range(len(bosque)):
        if bosque[i] == -1:
            bosque[i] = 0
    return bosque


"""
Simula el ciclo anual del bosque:
- Brota los arboles.
- Los quema
- Se propaga el fuego
- Se limpian
Devuelve la cantidad de arboles que hayan sobrevivido al ciclo.
"""
def ciclo(bosque,p,f):
    bosque_brotes = brotes(bosque,p)
    bosque_rayos = rayos(bosque_brotes, f)
    bosque_propagado = propagacion(bosque_rayos)
    bosque_limpio = limpieza(bosque_propagado)
    print("Arboles sobrevivientes: ", bosque_limpio.count(1))
    return bosque_limpio.count(1)


"""
Repite el ciclo n veces.
Devuelve el promedio de arboles sobrevivientes por ciclo.
"""
def ciclo_repeticiones(bosque,p,f,repeticiones):
    total_arboles_sobrevivientes = 0

    for _ in range(repeticiones):
        total_arboles_sobrevivientes += ciclo(bosque,p,f)
    
    return total_arboles_sobrevivientes/repeticiones


"""
Grafica los arboles sobrevivientes respecto a
los valores probabilisticos (eje y)
la cantidad de arboles sobrevivientes (eje x)

Se grafica usando la libreria matplotlib
"""
def graficar(valores_p, arboles_vivos):
    plt.plot(valores_p, arboles_vivos, marker="o")
    plt.xticks(valores_p)
    plt.yticks(range(11))
    plt.xlabel("Probabilidad de brote (p)")
    plt.ylabel("Cantidad de árboles vivos")
    plt.show()

"""
Calcula los arboles sobrevivientes
por probabilidad de brote y rayos
la probilidad y la cantidad de arboles sobrevivientes 
se guardan en su correspondiente lista para poder usarlas en el gráfico
"""
def graficar_promedios(bosque,f):

    valores_p = []
    arboles_vivos = []

    for i in range(11):
        p = i / 10
        valores_p.append(p)
        arboles_vivos.append(ciclo(bosque,p,f))
    
    graficar(valores_p, arboles_vivos)

p = 0.6 #probabilidad de brote
f = 0.4 #probabilidad de rayo
repeticiones = 50

print(graficar_promedios(bosque_limpio(10),0.02))

