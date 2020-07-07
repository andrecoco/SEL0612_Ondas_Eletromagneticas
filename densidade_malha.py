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
import matplotlib.ticker as ticker
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
    return (2*PI*C/N)*(1/(cmath.acos(1+1/(S**2)*(math.cos(2*PI*S/N)-1))).real)

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

##### Plot do gráfico #####

#Configura a figura
fig, plotAtenuacao = plt.subplots()
fig.canvas.set_window_title('Nome da Figura')
fig.suptitle('Titulo da Figura', fontsize=16)
plotVelocidade = plotAtenuacao.twinx()

#Plota os dois graficos
plotVelocidade.plot(Ns, velocidades, 'g-')
plotAtenuacao.plot(Ns, atenuacoes, '--')

# Seta os limites para o eixo x
plotAtenuacao.set_xlim(1,10)

# Seta os limites para os eixos y
plotVelocidade.set_ylim(0, 2)
plotAtenuacao.set_ylim(0, 6)

#Seta os ticks
plotAtenuacao.xaxis.set_major_locator(ticker.AutoLocator())
plotAtenuacao.xaxis.set_minor_locator(ticker.AutoMinorLocator())

plotAtenuacao.yaxis.set_major_locator(ticker.AutoLocator())
plotAtenuacao.yaxis.set_minor_locator(ticker.AutoMinorLocator())

plotVelocidade.yaxis.set_major_locator(ticker.AutoLocator())
plotVelocidade.yaxis.set_minor_locator(ticker.AutoMinorLocator())

#Coloca um texto acima de cada gráfico
plotVelocidade.text(4, 1.05, 'Velocidade de Fase da Onda Numérica')
plotAtenuacao.text(3, 1.10, 'Constante de Atenuação')

#Nomeia os eixos
plotAtenuacao.set_xlabel('Densidade da Grade (points per free-space wavelength)')
plotVelocidade.set_ylabel('Velocidade de Fase da Onda Numérica (normalizada em c)')
plotAtenuacao.set_ylabel('Constante de Atenuação (neppers/grid cell)')

plt.show()