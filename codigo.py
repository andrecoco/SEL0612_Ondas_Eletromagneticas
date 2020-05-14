"""
Esse programa visa simular uma linha de transmissão segundo as equações do
radialista através do método das diferenças finitas.

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

#Impedância característica
Z0 = 50  #Ohm
#Resistência interna da fonte
Rs = 75  #Ohm
#Resistência da carga
Rl = 100 #Ohm

#dados da linha (pegamos de um par trançado comercial)
R= 32e-3            #Ohm/m
L= 509e-9           #H/m
G=R/(Z0**2)         #1/Ohm*m
C=L/(Z0**2)         #F/m

#precisão do tempo
dt = 1e-10 #s
#precisão do comprimento
dz = 1e-2  #m
assert (dt <= dz*(L*C)**(1/2)), "dt deve ser menor que " + str(dz*(L*C)**(1/2)) + " (v = "+str(1/(L*C)**(1/2))+")!"
#dt <= dz/v = dz*sqrt(L*C) para estabilidade

#duração da simulação (Número de passos de tempo)
TIME = int(1e-6/dt) #s
#comprimento do fio (Quantidade de pontos simulados)
LEN = int(1e0/dz) #m

#verificação de memória < 512MB porque travou meu pc algumas vezes
memoria = TIME*LEN
assert (memoria < 2**29), "parâmetros consomem muita memoria: " + str(memoria/2**30) + "GB"

#tensão na fonte em função do tempo
#2*u(t)
Vs_t = 2*np.ones(TIME) #V

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
    i[n][-1] = v[n-1][-1]/Rl
    #Para tomar a corrente no ponto posterior ao analisado (fora do vetor para a=l)
    #delosca-se o vetor para a esquerda e adiciona a corrente na carga
    v[n] = C3*( i[n][1:] - i[n][:-1] ) + C4*v[n-1]

#running mean ao longo do fio para suavizar a medida
plt.plot(np.convolve(v[-1], np.ones(5)*(1/5), mode="valid"))
plt.ylim(0,2.1)
plt.show()
