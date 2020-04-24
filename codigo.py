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
+o   o   o   o   o   o   o   o   o   o   o   o   o   o   o       +
+                                                                +
+  x   x   x   x   x   x   x   x   x   x   x   x   x   x   x \   +
+                                                            |   +
+o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   |dt +
+                                                            |   +
+  x   x   x   x   x   x   x   x   x   x   x   x   x   x   x /   +
+                                                                +
+o   o   o   o   o   o   o   o   o   o   o   o   o   o   o       +
+    \---/                                                       +
+      dz                                                        +
+                                                                +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

import numpy as np

#Impedância característica
Z0 = 50  #Ohm
#Resistência interna da fonte
Rs = 75  #Ohm
#Resistência da carga
Rl = 100 #Ohm

#precisão do tempo
dt = 1e-6 #s
#precisão do comprimento
dz = 1e-3 #m
#obs: dt <= dz/v = dz*sqrt(L*C) para estabilidade

#duração da simulação (Número de passos de tempo)
TIME = int(1e-3/dt) #s
#comprimento do fio (Quantidade de pontos simulados)
LEN = int(1/dz) #m

#tensão na fonte em função do tempo
#2*u(t)
Vs_t = 2*np.ones(TIME) #V

#condições iniciais
v0 = np.zeros(LEN) #V
i0 = np.zeros(LEN) #A

#dados da linha (a especificação não deu diretamente)
R=2500 #Ohm/m
L=2500 #H/m
G=1    #1/Ohm*m
C=1    #F/m

#constantes uteis para a simulação
C1 = (-2*dt)/(dt*dz*R+2*dz*L)
C2 = (2*L-dt*R)/(2*L+dt*R)
C3 = (-2*dt)/(dt*dz*G+2*dz*C)
C4 = (2*C-dt*G)/(2*C+dt*G)

#array para armazenar e processar os dados
v = np.zeros((TIME,LEN))
v[0] = v0
i = np.zeros((TIME,LEN))
i[0] = i0
