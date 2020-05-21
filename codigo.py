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
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from graficos import plotAnimations

######################### CONFIGURACOES DA SIMULACAO ##########################
#Escolha da carga
# 1 - 100 ohm
# 2 - 0 ohm (Curto)
# 3 - inf ohm (Circuito Aberto)
carga = 2

#Escolha da Fonte
# 1 - 2*u(t) 
# 2 - u(t) - u(t - l/10uf)
fonte = 1

######################### CONFIGURACOES DA ANIMACAO ###########################
#Tomar media de pontos proximos para reduzir ruido (filtro de média)
#   pode causar distorções nos pontos extremos
tomarMedia = False

#A velocidade determina o numero de pontos considerados na hora de atualizar
#   a animação, velocidade = n quer dizer que somente um ponto a cada n no
#   tempo serão considerados na animação. velocidade = 1 quer dizer que todos
#   os pontos no tempo serão considerados
#   OBS: Deve ser um valor inteiro!
velocidade = 8

#O intervalo determina quantos ms ocorrem entre cada atualização da animação
#   um intervalor muito pequeno pode causar problemas de desempenho ao mostrar
#   a animação. Já um valor muito alto pode causar uma animação "travada"
#   OBS: Deve ser um valor inteiro!
intervalo = 100 #ms

###############################################################################

assert (carga >= 1 and carga <= 3), "Configuracao de Carga Invalida!"
assert (fonte >= 1 and carga <= 2), "Configuracao de Fonte Invalida!"

#Impedância característica
Z0 = 50  #Ohm
#Resistência interna da fonte
Rs = 75  #Ohm
#Resistência da carga
Rl = 100 #Ohm

#Dados da linha (pegamos de um par trançado comercial)
R= 0            #Ohm/m
L= 185e-9       #H/m
G= R/(Z0**2)     #1/Ohm*m
C= L/(Z0**2)     #F/m
uf= 1/np.sqrt(L*C) #m/s
l= 1e0              #m

#precisão do tempo
dt = 5e-12 #s
#precisão do comprimento
dz = 5e-3  #m
assert (dt <= dz*(L*C)**(1/2)), "dt deve ser menor que " + str(dz*(L*C)**(1/2)) + " (v = "+str(1/(L*C)**(1/2))+")!"

#comprimento do fio (Quantidade de pontos simulados)
LEN = int(l/dz) #pontos

#duração da simulação (Número de passos de tempo)
#tempo suficiente para ir ou voltar 10 vezes na linha
TIME = 10*int((l/uf)/dt) #pontos

#verificação de memória < 2GB (para nao dar problema no PC) 
memoria = TIME*LEN*8*2
assert (memoria < 2*(2**30)), "parâmetros consomem muita memoria: " + str(memoria/2*(2**30)) + "GB"

#tensão na fonte em função do tempo
if(fonte == 1):
    Vs_t = 2*np.ones(TIME) #V
else:
    Vs_t = np.zeros(TIME)
    Vs_t[0:int(l/(10*uf*dt))] = 1

#condições iniciais
v0 = np.zeros(LEN) #V
i0 = np.zeros(LEN+1) #A

#constantes uteis para a simulação
C1 = (-2*dt)/(dt*dz*R+2*dz*L)
C2 = (2*L-dt*R)/(2*L+dt*R)
C3 = (-2*dt)/(dt*dz*G+2*dz*C)
C4 = (2*C-dt*G)/(2*C+dt*G)

#array para armazenar e processar os dados
v = np.zeros((TIME,LEN))
v[0] = v0
i = np.zeros((TIME,LEN+1))
i[0] = i0

#loop principal da simulação
for n in range(1,TIME): #começa em 1 porque condições iniciais são conhecidas
    #Para tomar a tensão no ponto anterior ao analisado (fora do vetor para z=0)
    #desloca-se o vetor para a direita e adiciona a tensão da fonte
    i[n][1:-1] = C1*( v[n-1][1:] - v[n-1][:-1] ) + C2*i[n-1][1:-1]
    i[n][0]  = (Vs_t[n-1]-v[n-1][0])/Rs
    
    if(carga == 1):
        i[n][-1] = v[n-1][-1]/Rl
    elif(carga == 2):
        i[n][-1] = i[n][-2] #CASO EM CURTO (Rl == 0)
    else:
        i[n][-1] = 0        #CASO ABERTO (Rl = inf)

    #Para tomar a corrente no ponto posterior ao analisado (fora do vetor para a=l)
    #delosca-se o vetor para a esquerda e adiciona a corrente na carga
    v[n] = C3*( i[n][1:] - i[n][:-1] ) + C4*v[n-1]

plotAnimations(i, v, LEN, TIME, dz, tomarMedia, velocidade, intervalo)