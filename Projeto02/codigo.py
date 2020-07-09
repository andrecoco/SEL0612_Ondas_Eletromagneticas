"""
Esse programa realiza uma simualação segundo a equação de onda pelo
método da FDTD, em particular para uma onda elétromagnética e
considerando um fenômeno de refração/reflexão
"""

import numpy as np
from scipy.constants import c
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# Configurações da simulação
L = 1               # Comprimento do espaço em metros
T = 1*L/c         # Tempo da simulação em segundos
S = 0.5             # Fator de estabilidade de Courrant
S_REFRAC = 0.25     # "Fator de courrant" do segundo meio
TRANSICAO = 1       # Ponto a partir do qual começa o segundo meio
DX = 5e-3           # Precisão do comprimento
LEN = int(L/DX)     # Quantidade de pontos do espaço simulados (automático)
# As constantes ligadas ao tempo são determinadas por S

def calculo(S=S, S_REFRAC=S_REFRAC):
    """
    Função que realiza loop principal da simulação
    """

    # Constantes importantes para a simulação
    DT = S*DX/c         # passo de tempo
    TIME = int(T/DT)    # duração da simulação (Número de passos de tempo)

    # Verificação de memória < 2GB (para nao dar problema no PC)
    memoria = TIME*LEN*8
    assert (memoria < 2*(2**30)), ("parâmetros consomem muita memoria: "
                                   + str(memoria/(2**30)) + "GB")

    # Campo na fonte em função do tempo
    # Pulso retangular
    #E_t = np.zeros(TIME)    # V/m
    #E_t[0:int(0.2*(L/c)/DT)] = 1

    # Pulso gaussiano
    E_t = np.zeros(TIME)    # V/m
    comprimento = int(((L/c)/DT))
    pulso = np.linspace(-3, 3, num=comprimento)
    pulso = np.exp(-(pulso)**2)
    E_t[:comprimento] = pulso

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
        # Condição de contorno na borda final
        E[n, -1] = E[n, -2]

    return E


##### Plot do gráfico #####
# Configura a figura
fig, plotPulsos = plt.subplots()
fig.canvas.set_window_title('Nome da Figura')
fig.suptitle('Titulo da Figura', fontsize=16)

# Plota os dados
plotPulsos.plot(calculo()[-1], color='black', label='S = ' + str(S))
plotPulsos.plot(calculo(S=1, S_REFRAC=1)[-1],
                '--', color='black', label='S = 1')

# Legenda
plt.legend()

# Seta os limites para o eixo x
plotPulsos.set_xlim(0, 200)

# Seta os limites para o eixo y
plotPulsos.set_ylim(-0.2, 1.4)

# Seta os ticks
plotPulsos.xaxis.set_tick_params(which="major", top=True, direction="in")
plotPulsos.xaxis.set_tick_params(which="minor", top=True, direction="in")
plotPulsos.xaxis.set_major_locator(ticker.AutoLocator())
plotPulsos.xaxis.set_minor_locator(ticker.AutoMinorLocator())

plotPulsos.yaxis.set_tick_params(which="major", right=True, direction="in")
plotPulsos.yaxis.set_tick_params(which="minor", right=True, direction="in")
plotPulsos.yaxis.set_major_locator(ticker.AutoLocator())
plotPulsos.yaxis.set_minor_locator(ticker.AutoMinorLocator())

plt.show()
