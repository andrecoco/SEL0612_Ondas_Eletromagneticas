#ADAPTAR A DESCRIÇÃO ABAIXO

"""
Esse programa visa simular uma linha de transmissão segundo as equações do
telegrafista através do método das diferenças finitas.

O procedimento consiste em guardar gerar duas grades de pontos z,t, uma para
tensão e uma para corrente. As grades estão desalinhadas para melhorar a
qualidade das aproximações numéricas. Em princípio só são conhecidas as
condições iniciais para t=0 e daí são calculados os estados da linha para
os outros instantes de tempo.

Também integrado ao programa está uma animação do resultado.

Ilustração da grade (o=corrente x=tensão)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+o|  o   o   o   o   o   o   o   o   o   o   o   o   o  |o       +
+ |                                                     |        +
+ |x   x   x   x   x   x   x   x   x   x   x   x   x   x|    \   +
+ |                                                     |    |   +
+o|  o   o   o   o   o   o   o   o   o   o   o   o   o  |o   |dt +
+ |                                                     |    |   +
+ |x   x   x   x   x   x   x   x   x   x   x   x   x   x|    /   +
+ |                                                     |        +
+o|  o   o   o   o   o   o   o   o   o   o   o   o   o  |o       +
+ fonte      \---/                                      carga    +
+              dz                                                +
+                                                                +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

import numpy as np
from scipy.constants import c, mu_0, epsilon_0
import matplotlib.pyplot as plt
import animacao2D

import matplotlib.cm as cm

l = 1e0                 # Comprimento do espaço em metros
SIGMA = 0               # Condutividade do meio
SIGMA_STAR = 0          # Perda magnética equivalente
EPSILON = epsilon_0     # Permissividade elétrica do meio
MU = mu_0               # Permeabilidade magnética do meio

#precisão do comprimento
dx = 1e-2  # m
dt = dx/(np.sqrt(2)*c)  # s

#lado do quadrado do espaço (Quantidade de pontos simulados)
LEN = int(l/dx) #pontos

#duração da simulação (Número de passos de tempo)
TIME = int(np.sqrt(2)*0.5*(l/c)/dt) #pontos

#verificação de memória < 2GB (para nao dar problema no PC)
memoria = TIME*LEN*LEN*8*3
assert (memoria < 2*(2**30)), "parâmetros consomem muita memoria: " + str(memoria/(2**30)) + "GB"

# Ez no centro da grade
# Pulso retangular
Ez_t = np.zeros(TIME)
Ez_t[0:int(0.1*(l/c)/dt)] = 1
# Onda senoidal
#Ez_t = np.linspace(0, 2*np.pi, num=TIME)
#Ez_t = np.sin(2*Ez_t*(TIME/(0.5*(l/c)/dt)))

# Condições iniciais
Ez0 = np.zeros((LEN+1, LEN+1))
Hx0 = np.zeros((LEN+1, LEN))
Hy0 = np.zeros((LEN, LEN+1))

# Constantes uteis para a simulação
CA = (1-((SIGMA*dt)/(2*EPSILON)))/(1+((SIGMA*dt)/(2*EPSILON)))
CB = (dt/(EPSILON*dx))/(1+((SIGMA*dt)/(2*EPSILON)))
DA = (1-((SIGMA_STAR*dt)/(2*MU)))/(1+((SIGMA_STAR*dt)/(2*MU)))
DB = (dt/(MU*dx))/(1+((SIGMA_STAR*dt)/(2*MU)))

# Arrays para armazenar e processar os dados
Ez = np.empty((TIME, LEN+1, LEN+1))
Ez[0] = Ez0     # Condição inicial
# Condição de contorno
Ez[:, :, +1] = 0
Ez[:, :, -1] = 0
Ez[:, +1, :] = 0
Ez[:, -1, :] = 0

Hx = np.empty((TIME, LEN+1, LEN))
Hx[0] = Hx0     # Condição inicial

Hy = np.empty((TIME, LEN, LEN+1))
Hy[0] = Hy0     # Condição inicial

# Loop principal da simulação
for n in range(1, TIME): # Começa em 1 porque condições iniciais são conhecidas
    Ez[n, 1:-1, 1:-1] = CA*Ez[n-1, 1:-1, 1:-1] + CB*(
        - (Hx[n-1, 1:-1, 1:] - Hx[n-1, 1:-1, :-1])
        + (Hy[n-1, 1:, 1:-1] - Hy[n-1, :-1, 1:-1])
        )

    Ez[n, int(LEN/2), int(LEN/2)] = Ez_t[n]
    Hx[n] = DA*Hx[n-1] - DB*(Ez[n, :, 1:] - Ez[n, :, :-1])
    Hy[n] = DA*Hy[n-1] + DB*(Ez[n, 1:, :] - Ez[n, :-1, :])


###### PLOT dos Gráficos ######
COR = 'seismic'

#Cria as Figuras
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()
fig1.canvas.set_window_title('Ez')
fig1.suptitle('Subtitulo Fig1', fontsize=12)
fig2.canvas.set_window_title('Hx')
fig2.suptitle('Subtitulo Fig2', fontsize=12)
fig3.canvas.set_window_title('Hz')
fig3.suptitle('Subtitulo Fig3', fontsize=12)
fig4.canvas.set_window_title('Ez 3D')
fig4.suptitle('Subtitulo Fig4', fontsize=12)

#Plota FIG1
maxval = np.max(abs(Ez[-1]))
colormap = ax1.imshow(Ez[-1], cmap=COR, vmin=-maxval, vmax=maxval)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
fig1.colorbar(colormap)

#Plota FIG2
maxval = np.max(abs(Hx[-1]))
colormap = ax2.imshow(Hx[-1], cmap=COR, vmin=-maxval, vmax=maxval)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
fig2.colorbar(colormap)

#Plota FIG3
maxval = np.max(abs(Hy[-1]))
colormap = ax3.imshow(Hy[-1], cmap=COR, vmin=-maxval, vmax=maxval)
ax3.set_xlabel('x')
ax3.set_ylabel('y')
fig3.colorbar(colormap)

#Plota FIG4
x = np.linspace(-100, 100, 101)
y = np.linspace(-100, 100, 101)
X, Y = np.meshgrid(x, y)
Z = Ez[-1]
ax4 = plt.axes(projection='3d')
#ax4.contour3D(X, Y, Z, 50, cmap=COR)
ax4.plot_surface(X, Y, Z, rcount = 200 , ccount = 200,  cmap=COR)
ax4.set_xlabel('x')
ax4.set_ylabel('y')
ax4.set_zlabel('z')

plt.show()

