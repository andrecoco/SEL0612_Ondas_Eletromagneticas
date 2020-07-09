"""
Esse programa realiza uma simualação segundo a equação de onda pelo
método da FDTD, em particular para uma onda elétromagnética e
considerando um fenômeno de refração/reflexão
"""

import numpy as np
from scipy.constants import c
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
########### Configurações da simulação #########
L = 1               # Comprimento do espaço em metros
T = 1*L/c           # Tempo da simulação em segundos
S = 1.0005               # Fator de estabilidade de Courrant
S_REFRAC = 0.25     # "Fator de courrant" do segundo meio
TRANSICAO = 1       # Ponto a partir do qual começa o segundo meio
DX = 5e-3           # Precisão do comprimento   
LEN = int(L/DX)     # Quantidade de pontos do espaço simulados (automático)

#Configuracoes do grafico1
YMin = None
YMax = None
plotarS1 = False    # Plotar um outro gráfico pontilhado para S = 1

#Comfiguracoes do grafico2 [ variando o n (TIME) ]
plotGrafico2 = True    # Define se o grafico variando o n sera plotado (as configuracoes do grafico 1 sera ignoradas)
# As constantes ligadas ao tempo são determinadas por S
#################################################

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
    pulso = np.linspace(-3.3, 3.3, num=comprimento)
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
fig.canvas.set_window_title('Figura')
fig.suptitle('Propagação do Pulso', fontsize=16)

# Plota os dados
#Verifica se existe uma interface (dois meios distintos)
if(not plotGrafico2):
    if(TRANSICAO == 1): 
        if(plotarS1):
            plotPulsos.plot(calculo(S=1, S_REFRAC=1)[-1],
                            '--', color='black', label='S = 1')
        plotPulsos.plot(calculo()[-1], color='C0', label='S = ' + str(S))
        # Legenda
        plt.legend()
    else:
        plt.axvline(x=TRANSICAO*LEN, linestyle = '--' ,color = 'black')
        plotPulsos.plot(calculo()[-1], color='C0')
    
    # Seta os limites para o eixo x
    plotPulsos.set_xlim(0, LEN)

    # Seta os limites para o eixo y
    if(YMin != None and YMax != None):
        plotPulsos.set_ylim(YMin, YMax)
    
    # Seta os ticks
    plotPulsos.xaxis.set_tick_params(which="major", top=True, direction="in")
    plotPulsos.xaxis.set_tick_params(which="minor", top=True, direction="in")
    plotPulsos.xaxis.set_major_locator(ticker.AutoLocator())
    plotPulsos.xaxis.set_minor_locator(ticker.AutoMinorLocator())

    plotPulsos.yaxis.set_tick_params(which="major", right=True, direction="in")
    plotPulsos.yaxis.set_tick_params(which="minor", right=True, direction="in")
    plotPulsos.yaxis.set_major_locator(ticker.AutoLocator())
    plotPulsos.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    #Nomeia os eixos
    plotPulsos.set_xlabel('Coordenada i na Grade')
    plotPulsos.set_ylabel('Função de Onda u(i)')

else: #Caso a escolha seja plotar o grafico com TIME variando
    fig2, plotPulsos2 = plt.subplots()
    fig2.canvas.set_window_title('Figura')
    fig.suptitle('Propagação do Pulso Variando o TIME (S = ' + str(S) + ')', fontsize=12)
    fig2.suptitle('Propagação do Pulso Variando o TIME com Foco no Início (S = ' + str(S) + ')', fontsize=12)
    T = 1.205*L/c
    plotPulsos.plot(calculo()[-1], color='C2', label='TIME = ' + str(int(T/(S*DX/c))))
    plotPulsos2.plot(calculo()[-1], color='C2', label='TIME = ' + str(int(T/(S*DX/c))))
    T = 1.255*L/c
    plotPulsos.plot(calculo()[-1], color='C1', label='TIME = ' + str(int(T/(S*DX/c))))
    plotPulsos2.plot(calculo()[-1], color='C1', label='TIME = ' + str(int(T/(S*DX/c))))
    T = 1.305*L/c
    plotPulsos.plot(calculo()[-1], color='C0', label='TIME = ' + str(int(T/(S*DX/c))))
    plotPulsos2.plot(calculo()[-1], color='C0', label='TIME = ' + str(int(T/(S*DX/c))))
    plotPulsos2.legend()
    plotPulsos.legend()
    
    # Seta os limites para o eixo x
    plotPulsos.set_xlim(0, LEN)
    plotPulsos2.set_xlim(0, LEN/10)

    # Seta os limites para o eixo y
    plotPulsos2.set_ylim(-0.05, 0.05)

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
