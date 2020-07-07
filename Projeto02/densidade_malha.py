"""
Esse programa motra gráficos para velocidade de propagação e decaimento
espacial para diferentes densidades de grade numa simulação de FDTD para a
equação de onda
"""

import math
import cmath
import scipy.constants
import numpy as np
import matplotlib.pyplot as plt
C = scipy.constants.c
PI = math.pi

NUM_PONTOS = 1000
S = 0.5
MIN_N = 1
MAX_N = 10

def velocidade_fase(S, N):
    """
    determina velocidade de fase para dada uma densidade de grade e um S
    entradas:
    S - Fator de Courrant
    N - Densidade da grade
    """
    return (2*PI*C/N)*(1/(cmath.acos(1+1/(S**2)*(math.cos(2*PI*S/N)-1)))).real

def atenuacao(S, N):
    """
    determina atenuação espacial para dada uma densidade de grade e um S
    entradas:
    S - Fator de Courrant
    N - Densidade da grade
    """
    return -(cmath.acos(1+1/(S**2)*(math.cos(2*PI*S/N)-1))).imag


Ns = np.arange(MIN_N, MAX_N, (MAX_N-MIN_N)/NUM_PONTOS)
velocidades = np.empty(len(Ns))
atenuacoes = np.empty(len(Ns))

for i, n in enumerate(Ns):
    velocidades[i] = velocidade_fase(S, n)/C
    atenuacoes[i] = atenuacao(S, n)

erros = abs(1-velocidades)*100

plt.plot(Ns, velocidades)
plt.ylim(0)
plt.show()
plt.plot(Ns, atenuacoes)
plt.ylim(0)
plt.show()
plt.semilogy(Ns, erros)
plt.show()
