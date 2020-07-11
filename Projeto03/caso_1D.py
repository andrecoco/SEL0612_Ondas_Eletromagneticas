"""
Esse programa realiza a simulação de uma onda eletromagnética 1D por meio
do algoritmo de Yee adaptado para uma dimensão
"""

import numpy as np
from scipy.constants import c, mu_0, epsilon_0
import matplotlib.pyplot as plt
import animacao1D

l = 1e0                 # Comprimento do espaço em metros
T = 1.5*(l/c)           # Tempo da simulação em segundos
SIGMA = 0               # Condutividade do meio
SIGMA_STAR = 0          # Perda magnética equivalente
EPSILON = epsilon_0     # Permissividade elétrica do meio
MU = mu_0               # Permeabilidade magnética do meio

#precisão do comprimento
dx = 1e-3  # m
dt = dx/c  # s

#comprimento do fio (Quantidade de pontos simulados)
LEN = int(l/dx) #pontos

#duração da simulação (Número de passos de tempo)
TIME = int(T/dt) #pontos

#verificação de memória < 2GB (para nao dar problema no PC)
memoria = TIME*LEN*8*2
assert (memoria < 2*(2**30)), "parâmetros consomem muita memoria: " + str(memoria/(2**30)) + "GB"

# Campo na borda esquerda
# Pulso retangular
Ez_t = np.zeros(TIME)
Ez_t[0:int(0.4*(l/c)/dt)] = 1

# Condições iniciais
Ez0 = np.zeros(LEN+1)
Hy0 = np.zeros(LEN)

# Constantes uteis para a simulação
CA = (1-((SIGMA*dt)/(2*EPSILON)))/(1+(SIGMA*dt)/(2*EPSILON))
CB = (dt/(EPSILON*dx))/(1+(SIGMA*dt)/(2*EPSILON))
DA = (1-((SIGMA_STAR*dt)/(2*MU)))/(1+(SIGMA_STAR*dt)/(2*MU))
DB = (dt/(MU*dx))/(1+(SIGMA_STAR*dt)/(2*MU))

# Arrays para armazenar e processar os dados
Ez = np.empty((TIME, LEN+1))
Ez[0] = Ez0     # Condição inicial
Ez[:, 0] = Ez_t # Fonte na borda esquerca
Ez[:, -1] = 0   # Condição de contorno na borda direita

Hy = np.empty((TIME, LEN))
Hy[0] = Hy0     # Condição inicial

print(CA, CB, DA, DB)

# Loop principal da simulação
for n in range(1, TIME): # Começa em 1 porque condições iniciais são conhecidas
    Ez[n][1:-1] = CA*Ez[n-1][1:-1] + CB*(Hy[n-1][1:]-Hy[n-1][:-1])
    Hy[n] = DA*Hy[n-1] + DB*(Ez[n][1:] - Ez[n][:-1])

###### Plot dos Graficos ######
fig1, ax1 = plt.subplots()
fig1_2, ax1_2 = plt.subplots()
fig2, ax2 = plt.subplots()
fig2_2, ax2_2 = plt.subplots()
fig1.canvas.set_window_title('Ez_Antes')
fig1.suptitle('Componente z do Campo E (antes de chegar ao final da grid)', fontsize=12)
fig1_2.canvas.set_window_title('Ez_Depois')
fig1_2.suptitle('Componente z do Campo E (depois de chegar ao final da grid)', fontsize=12)
fig2.canvas.set_window_title('Hy_Antes')
fig2.suptitle('Componente y do Campo H (antes de chegar ao final da grid)', fontsize=12)
fig2_2.canvas.set_window_title('Hy_Depois')
fig2_2.suptitle('Componente y do Campo H (depois de chegar ao final da grid)', fontsize=12)

#Plota Ez
ax1.plot(np.linspace(0, l, num=LEN+1), Ez[int(TIME*0.6)], 'r-')
ax1.set_xlabel('Comprimento (m)')
ax1.set_ylabel('Campo Elétrico (V/m)')
ax1_2.plot(np.linspace(0, l, num=LEN+1), Ez[-1], 'r-')
ax1_2.set_xlabel('Comprimento (m)')
ax1_2.set_ylabel('Campo Elétrico (V/m)')
ymax = 1.2*np.maximum(np.amax(Ez[int(TIME*0.6)]), np.amax(Ez[-1]))
ymin = 1.2*np.minimum(np.amin(Ez[int(TIME*0.6)]), np.amin(Ez[-1]))
ax1.set_ylim(ymin - 0.4*(ymax - ymin), ymax + 0.4*(ymax - ymin))
ax1_2.set_ylim(ymin - 0.4*(ymax - ymin), ymax + 0.4*(ymax - ymin))

#Plota Hy
ax2.plot(np.linspace(0, l, num=LEN), Hy[int(TIME*0.6)], 'b-')
ax2.set_xlabel('Comprimento (m)')
ax2.set_ylabel('Campo Magnético (Tesla)')
ax2_2.plot(np.linspace(0, l, num=LEN), Hy[-1], 'b-')
ax2_2.set_xlabel('Comprimento (m)')
ax2_2.set_ylabel('Campo Magnético (Tesla)')
ymax = np.maximum(np.amax(Hy[int(TIME*0.6)]), np.amax(Hy[-1]))
ymin = np.minimum(np.amin(Hy[int(TIME*0.6)]), np.amin(Hy[-1]))
ax2.set_ylim(ymin - 0.4*(ymax - ymin), ymax + 0.4*(ymax - ymin))
ax2_2.set_ylim(ymin - 0.4*(ymax - ymin), ymax + 0.4*(ymax - ymin))

ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax2_2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.show()

#Animacao
animacao1D.plotAnimations(Ez, Hy, len(Ez[0]), len(Hy[0]), LEN, l, TIME)
