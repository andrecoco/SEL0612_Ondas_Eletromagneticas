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
MAX_N = 80

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


##### Plot dos gráficos #####
#Configura as figuras
fig, plotAtenuacao = plt.subplots()
fig.canvas.set_window_title('Figura 1')
fig.suptitle('Variação da Velocidade de Fase da Onda e a Atenuação', fontsize=14)
plotVelocidade = plotAtenuacao.twinx()

fig2, plotErro = plt.subplots()
fig2.canvas.set_window_title('Figura 2')
fig2.suptitle('Erro da Velocidade de Fase', fontsize=14)

#Plota os dados
plotVelocidade.plot(Ns, velocidades, 'g-', color = 'red')
plotAtenuacao.plot(Ns, atenuacoes, '--', color = 'blue')
#Para o plot do Erro vamos utilzar um subarray para N entre 3-80
plotErro.plot(Ns[int((3-MIN_N)*NUM_PONTOS/(MAX_N-MIN_N)) :], erros[int((3-MIN_N)*NUM_PONTOS/(MAX_N-MIN_N)) :], color = 'green')

# Seta os limites para o eixo x
plotAtenuacao.set_xlim(1,10)
plotErro.set_xlim(0,80)

# Seta os limites para os eixos y
plotVelocidade.set_ylim(0, 2)
plotAtenuacao.set_ylim(0, 6)
plotErro.set_ylim(0.01, 100)
#Seta a escala do eixo y para log no grafico do erro
plotErro.set_yscale('log')

#Seta os ticks
plotAtenuacao.xaxis.set_tick_params(which="major", top = True, direction = "in")
plotAtenuacao.xaxis.set_tick_params(which="minor", top = True, direction = "in")
plotAtenuacao.xaxis.set_major_locator(ticker.AutoLocator())
plotAtenuacao.xaxis.set_minor_locator(ticker.AutoMinorLocator())

plotAtenuacao.yaxis.set_tick_params(which="major", left = True, direction = "in")
plotAtenuacao.yaxis.set_tick_params(which="minor", left = True, direction = "in")
plotAtenuacao.yaxis.set_major_locator(ticker.AutoLocator())
plotAtenuacao.yaxis.set_minor_locator(ticker.AutoMinorLocator())

plotVelocidade.yaxis.set_tick_params(which="major", right = True, direction = "in")
plotVelocidade.yaxis.set_tick_params(which="minor", right = True, direction = "in")
plotVelocidade.yaxis.set_major_locator(ticker.AutoLocator())
plotVelocidade.yaxis.set_minor_locator(ticker.AutoMinorLocator())

plotErro.xaxis.set_tick_params(which="major", top = True, direction = "in")
plotErro.xaxis.set_tick_params(which="minor", top = True, direction = "in")
plotErro.xaxis.set_major_locator(ticker.AutoLocator())
plotErro.xaxis.set_minor_locator(ticker.AutoMinorLocator())

plotErro.yaxis.set_tick_params(which="major", right = True, direction = "in")
plotErro.yaxis.set_tick_params(which="minor", right = True, direction = "in")

#Coloca um texto acima dos plots
plotVelocidade.text(4, 1.05, 'Velocidade de Fase da Onda Numérica')
plotAtenuacao.text(3, 1.10, 'Constante de Atenuação')

#Nomeia os eixos
plotAtenuacao.set_xlabel('Densidade da Grade (pontos por comprimento de onda)')
plotAtenuacao.set_ylabel('Constante de Atenuação (neppers/celula da grade)')
plotVelocidade.set_ylabel('Velocidade de Fase da Onda Numérica (normalizada em c)')
plotErro.set_xlabel('Densidade da Grade (pontos por comprimento de onda)')
plotErro.set_ylabel('Erro da Velocidade de Fase (%)')

plt.show()