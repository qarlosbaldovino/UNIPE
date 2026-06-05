import random
import matplotlib.pyplot as plt


def bosque_vacio(n):
    """
    Genera un bosque de n celdas vacíos.
    Todos sus valores son 0.
    """

    bosque = [0] * n
    return bosque


def bosque_limpio(n):
    """
    Genera un bosque de n celdas.
    Todos sus valores son 0 y 1 aleatoriamente.
    """
    # bosque = [random.randint(0, 1) for _ in range(n)]
    bosque = []
    for _ in range(n):
        bosque.append(random.randint(0, 1))
    return bosque


def bosque_quemado(n):
    """
    Genera un bosque de n celdas.
    Todos sus valores son 0,1 y -1 aleatoriamente.
    """
    bosque = []
    bosque = [random.randint(-1, 1) for _ in range(n)]
    return bosque


def suceso_aleatorio(prob):
    """
    Retorna un valor booleano por una comparación.
    - random.random() genera un numero flotante entre el 0 y el 1.
    - prob es la probabilidad que pasamos como parámetro.
    - retorna True si el numero generado es menor a la probabilidad. 
    - retorna Falso si el numero generado es mayor a la probabilidad.
    """
    return random.random() < prob


def brotar_si_corresponde(bosque, celda, p):
    """
    ASUME: que el bosque solo tiene elementos 0 (no hay arbol) o 1 (hay arbol).
    Si ya hay un árbol el suceso no lo afecta, si no hay árbol lo brotará.
    Nunca ocurre que saco un árbol existente, solo planto o replanto.
    """
    if suceso_aleatorio(p):
        bosque[celda] = 1


def brotes(bosque, p):
    """
    Modifica un bosque modificando los valores 0 al 1  de sus elementos
    siempre y cuando de True la funcion suceso_aleatorio.
    En caso de que exista un arbol, queda como está. 
    ASUME: que el bosque solo tiene elementos 0 (no hay arbol) o 1 (hay arbol).
    """
    for i in range(len(bosque)):
        brotar_si_corresponde(bosque, i, p)


def cuantos(bosque, tipo_celda):
    """
    Cuenta cuantos de un tipo determinado de arbol dependiendo el valor que le pasemos como parámetro.
    - (1) Cuenta todos los arboles sanos del bosque.
    - (0) Cuenta los espacios vacios en el bosque
    - (-1) Cuenta los arboles quemados en el bosque.
    """
    return bosque.count(tipo_celda)


def hay_arbol_y_ocurre_evento(celda, f):
    return celda == 1 and suceso_aleatorio(f)


def quemar_si_corresponde(bosque, posicion, f):
    if hay_arbol_y_ocurre_evento(bosque[posicion], f):
        bosque[posicion] = -1


def rayos(bosque, f):
    """
    Quema un arbol mientras se cumpla la probabilidad de suceso_aleatorio 
    y además exista un arbol (no quedamo) en esa posición.
    """
    for i in range(len(bosque)):
        quemar_si_corresponde(bosque, i, f)


def propagacion(bosque):
    """
    Propaga un incendio por medio de un arbol quemado.

    Primero manda el viento para un lado y luego para el otro, 
    con esto asegura que en dos pasadas incendia todo.

    En caso de exista un arbol no-quemado a su lado, se quemará.
    En caso de que no haya un arbol (0) a su lado, no se expande el fuego por esa zona.
    """
    # ir a derecha
    for d in range(1, len(bosque)):
        if bosque[d-1] == -1 and bosque[d] == 1:
            bosque[d] == -1

    # ir a izquierda
    for i in range(len(bosque)-1, 0, -1):
        if bosque[i] == -1 and bosque[i-1] == 1:
            bosque[i-1] == -1


def limpieza(bosque):
    """
    Se limpian todos los arboles quemados.
    Modifica el bosque cambiando los valores -1 a 0.
    """
    for i in range(len(bosque)):
        if bosque[i] == -1:
            bosque[i] = 0


def ciclo(bosque, p, f):
    """
    Simula el ciclo anual del bosque:
    - Brota los arboles.
    - Los quema
    - Se propaga el fuego
    - Se limpian
    Devuelve la cantidad de arboles que hayan sobrevivido al ciclo.
    """
    brotes(bosque, p)
    rayos(bosque, f)
    propagacion(bosque)
    limpieza(bosque)
    print("Arboles sobrevivientes: ", cuantos(bosque, 1))
    return cuantos(bosque, 1)


def ciclo_repeticiones(bosque, p, f, repeticiones):
    """
    Repite el ciclo n veces.
    Devuelve el promedio de arboles sobrevivientes por ciclo.
    """
    total_arboles_sobrevivientes = 0

    for _ in range(repeticiones):
        total_arboles_sobrevivientes += ciclo(bosque, p, f)

    return total_arboles_sobrevivientes/repeticiones


def graficar(valores_p, arboles_vivos):
    """
    Grafica los arboles sobrevivientes respecto a
    los valores probabilisticos (eje y)
    la cantidad de arboles sobrevivientes (eje x)

    Se grafica usando la libreria matplotlib
    """
    plt.plot(valores_p, arboles_vivos, marker="o")
    plt.xticks(valores_p)
    plt.yticks(range(11))
    plt.xlabel("Probabilidad de brote (p)")
    plt.ylabel("Cantidad de árboles vivos")
    plt.show()


def graficar_promedios(bosque, f):
    """
    Calcula los arboles sobrevivientes
    por probabilidad de brote y rayos
    la probilidad y la cantidad de arboles sobrevivientes 
    se guardan en su correspondiente lista para poder usarlas en el gráfico
    """

    valores_p = []
    arboles_vivos = []

    for i in range(11):
        p = i / 10
        valores_p.append(p)
        arboles_vivos.append(ciclo(bosque, p, f))

    graficar(valores_p, arboles_vivos)


p_brote = 0.6  # probabilidad de brote
p_rayo = 0.1  # probabilidad de rayo
repeticiones = 50
tamaño = 10
bosque = bosque_limpio(tamaño)

print(graficar_promedios(bosque, p_rayo))
