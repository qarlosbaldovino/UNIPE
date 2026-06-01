import random

p = 0.6

def suceso_aleatorio(prob):
    return random.random() < prob

def bosque_vacio(n):
    bosque = []
    bosque.extend([0] * n)
    return bosque

def bosque_limpio(n):
    bosque = []
    bosque = [random.randint(0, 1) for _ in range(n)]
    return bosque

def bosque_quemado(n):
    bosque = []
    bosque = [random.randint(-1, 1) for _ in range(n)]
    return bosque

def brotes(bosque, prob):
    print(bosque)
    posicion = 0
    while posicion != len(bosque):
        if suceso_aleatorio(prob) or bosque[posicion] == 1:
            bosque[posicion] = 1
        else:
            bosque[posicion] = 0
        posicion += 1

    return bosque



print(brotes(bosque_limpio(10),p))
