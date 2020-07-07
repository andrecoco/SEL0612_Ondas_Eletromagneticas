"""
Esse programa realiza uma simualação segundo a equação de onda pelo
método da FDTD, em particular para uma onda elétromagnética e
considerando um fenômeno de refração/reflexão
"""

import numpy as np
from scipy.constants import c
import matplotlib.pyplot as plt
# Configurações da simulação
L = 1  # m
T = 1*L/c  # s
S = 0.15  # Fator de estabilidade de Courrant
S_REFRAC = 1  # "Fator de courrant" do segundo meio
TRANSICAO = 0.7  # ponto a partir do qual começa o segundo meio

# Precisão do comprimento
DX = 5e-3  # m
# Precisão do tempo
DT = S*DX/c  # s

# Comprimento do espaço (Quantidade de pontos simulados)
LEN = int(L/DX)  # pontos

# Duração da simulação (Número de passos de tempo)
TIME = int(T/DT)  # pontos

# Verificação de memória < 2GB (para nao dar problema no PC)
memoria = TIME*LEN*8
assert (memoria < 2*(2**30)), ("parâmetros consomem muita memoria: "
                               + str(memoria/(2**30)) + "GB")

# Campo na fonte em função do tempo

# Pulso retangular
# E_t = np.zeros(TIME) #V/m
# E_t[0:40] = 1

# Pulso gaussiano
E_t = np.linspace(-0.5*TIME, 0.5*TIME, num=TIME)
E_t = np.exp(-(E_t/20)**2)

# Condições iniciais
E0 = np.zeros(LEN+2)  # V/m

# Array para armazenar e processar os dados
E = np.empty((TIME, LEN+2))  # +2 para comportar condições de contorno
E[0] = E0
E[:, 0] = E_t

QUEBRA = int((TRANSICAO*LEN-2)+1)
# Loop principal da simulação
for n in range(1, TIME):  # começa em 1 porque condições iniciais são conhecidas
    # Cálculo do campo elétrico antes da mudança de meio
    E[n][1:QUEBRA] = ((S**2)*(E[n-1, 2:QUEBRA+1] + E[n-1, :QUEBRA-1] - 2*E[n-1, 1:QUEBRA])
                      + 2*E[n-1][1:QUEBRA] - E[n-2][1:QUEBRA])
    # Cálculo do campo elétrico depois da mudança de meio
    E[n][QUEBRA:-1] = ((S_REFRAC**2)*(E[n-1, QUEBRA+1:] + E[n-1, QUEBRA-1:-2] - 2*E[n-1, QUEBRA:-1])
                       + 2*E[n-1][QUEBRA:-1] - E[n-2][QUEBRA:-1])
    # condição de contorno na borda final
    E[n, -1] = E[n, -2]

plt.plot(E[-1])
# plt.ylim(0)
plt.show()
