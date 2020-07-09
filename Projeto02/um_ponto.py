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
#T = 0.8*L/c           # Tempo da simulação em segundos (n sei se serve aqui, pq dps eu seto dois Ts pra dar bom)
                       #posso qualquer coisa podemos deixar esse como a "base" e o outro soma um deslocamento 
S = 1             # Fator de estabilidade de Courrant
S_DIFF = 1.075       # "Fator de courrant" do ponto diferente
DIFF_POS = 0.45      # Posição do ponto diferente
DX = 5e-3           # Precisão do comprimento
LEN = int(L/DX)     # Quantidade de pontos do espaço simulados (automático)
# As constantes ligadas ao tempo são determinadas por S

def calculo(S=S, S_DIFF=S_DIFF):
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
    comprimento = int(((L/c)/DT))
    assert TIME > comprimento, "A implementação da gaussiana exige simulação mais longa"
    E_t = np.zeros(TIME)    # V/m
    pulso = np.linspace(-6, 6, num=comprimento)
    pulso = np.exp(-(pulso)**2)
    E_t[:comprimento] = pulso

    # Condições iniciais
    E0 = np.zeros(LEN+2)  # V/m

    # Array para armazenar e processar os dados
    E = np.empty((TIME, LEN+2))  # +2 para comportar condições de contorno
    E[0] = E0
    E[:, 0] = E_t

    DIFF_IDX = int((DIFF_POS*LEN-2)+1)

    # Loop principal da simulação
    for n in range(1, TIME):  # começa em 1 porque condições iniciais são conhecidas
        # Cálculo do campo elétrico antes da mudança de meio
        E[n][1:-1] = ((S**2)*(E[n-1, 2:] + E[n-1, :-2] - 2*E[n-1, 1:-1])
                      + 2*E[n-1][1:-1] - E[n-2][1:-1])
        # Ponto com S diferente
        E[n][DIFF_IDX] = ((S_DIFF**2)*(E[n-1, DIFF_IDX+1] + E[n-1, DIFF_IDX-1] - 2*E[n-1, DIFF_IDX])
                          + 2*E[n-1][DIFF_IDX] - E[n-2][DIFF_IDX])

        # Condição de contorno na borda final
        E[n, -1] = E[n, -2]

    return E


##### Plot do gráfico #####
fig, plotPulsos = plt.subplots()
fig.canvas.set_window_title('Figura')
fig.suptitle('Propagação do Pulso', fontsize=16)

fig2, plotPulsos2 = plt.subplots()
fig2.canvas.set_window_title('Figura')
fig.suptitle('Propagação do Pulso com S diferente em 1 ponto', fontsize=12)
fig2.suptitle('Propagação do Pulso com S diferente em 1 ponto com Foco no Início', fontsize=12)

T = 1.105*L/c
plotPulsos.plot(calculo()[-1], color='C2', label='TIME = ' + str(int(T/(S*DX/c))))
plotPulsos2.plot(calculo()[-1], color='C2', label='TIME = ' + str(int(T/(S*DX/c))))
T = 1.155*L/c
plotPulsos.plot(calculo()[-1], color='C1', label='TIME = ' + str(int(T/(S*DX/c))))
plotPulsos2.plot(calculo()[-1], color='C1', label='TIME = ' + str(int(T/(S*DX/c))))
plotPulsos2.legend()
plotPulsos.legend()

# Seta os limites para o eixo x
plotPulsos.set_xlim(0, LEN)
plotPulsos2.set_xlim(3*LEN/10, 6*LEN/10)

# Seta os limites para o eixo y
plotPulsos2.set_ylim(-1, 1)

# Seta os ticks
plotPulsos.xaxis.set_tick_params(which="major", top=True, direction="in")
plotPulsos.xaxis.set_tick_params(which="minor", top=True, direction="in")
plotPulsos.xaxis.set_major_locator(ticker.AutoLocator())
plotPulsos.xaxis.set_minor_locator(ticker.AutoMinorLocator())
plotPulsos2.xaxis.set_tick_params(which="major", top=True, direction="in")
plotPulsos2.xaxis.set_tick_params(which="minor", top=True, direction="in")
plotPulsos2.xaxis.set_major_locator(ticker.AutoLocator())
plotPulsos2.xaxis.set_minor_locator(ticker.AutoMinorLocator())

plotPulsos.yaxis.set_tick_params(which="major", right=True, direction="in")
plotPulsos.yaxis.set_tick_params(which="minor", right=True, direction="in")
plotPulsos.yaxis.set_major_locator(ticker.AutoLocator())
plotPulsos.yaxis.set_minor_locator(ticker.AutoMinorLocator())
plotPulsos2.yaxis.set_tick_params(which="major", right=True, direction="in")
plotPulsos2.yaxis.set_tick_params(which="minor", right=True, direction="in")
plotPulsos2.yaxis.set_major_locator(ticker.AutoLocator())
plotPulsos2.yaxis.set_minor_locator(ticker.AutoMinorLocator())

#Nomeia os eixos
plotPulsos.set_xlabel('Coordenada i na Grade')
plotPulsos.set_ylabel('Função de Onda u(i)')
plotPulsos2.set_xlabel('Coordenada i na Grade')
plotPulsos2.set_ylabel('Função de Onda u(i)')

plt.show()