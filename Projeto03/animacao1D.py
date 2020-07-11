import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pylab import *

def plotAnimations(Ez, Hy, EzLen, HyLen, LEN, l, TIME, velocidade = 5, intervalo = 20):
    plt.style.use('seaborn-pastel')

    # Cria as figuras
    anim = plt.figure(num = 0, figsize = (8, 6))

    # Nomeia as figuras
    anim.canvas.set_window_title('Animações')

    #Cria os subplots de cada figura
    EAnim = plt.subplot2grid((2, 1), (0, 0), fig=anim)
    HAnim = plt.subplot2grid((2, 1), (1, 0), fig=anim)

    # Configura os titulos dos subplots
    EAnim.set_title('Componente z do Campo E')
    HAnim.set_title('Componente y do Campo H')

    # Seta os limites para o eixo y
    HyYmax = np.amax(Hy)
    HyYmin = np.amin(Hy)
    EzYmax = np.amax(Ez)
    EzYmin = np.amin(Ez)
    EAnim.set_ylim(EzYmin - 0.2*(EzYmax - EzYmin),EzYmax + 0.2*(EzYmax - EzYmin))
    HAnim.set_ylim(HyYmin - 0.2*(HyYmax - HyYmin),HyYmax + 0.2*(HyYmax - HyYmin))

    # Seta os limites para o eixo x
    EAnim.set_xlim(0, EzLen)
    HAnim.set_xlim(0, HyLen)

    # Seta os ticklabels para o eixo x
    EAnim.set_xticklabels(EAnim.get_xticks()/LEN)
    HAnim.set_xticklabels(HAnim.get_xticks()/LEN)

    # Aciona o modo 'grid'
    EAnim.grid(True)
    HAnim.grid(True)

    # Nomeia os eixos
    EAnim.set_xlabel("Comprimento (m)")
    EAnim.set_ylabel("Campo Elétrico (V/m)")
    HAnim.set_xlabel("Comprimento (m)")
    HAnim.set_ylabel("Campo Magnético (Tesla)")

    # Vetores utilizados como eixo x
    EzEixoX= np.arange(EzLen)
    HyEixoX= np.arange(HyLen)

    # Ajeita o Layout
    anim.tight_layout()

    # Inicializa os gráficos
    p011, = EAnim.plot(Ez[0], 'r-')
    p021, = HAnim.plot(Hy[0], 'b-')
    
    # Função que atualiza a animação
    def updateData(n):
        p011.set_data(EzEixoX, Ez[n*velocidade])
        p021.set_data(HyEixoX, Hy[n*velocidade])

        return p011, p021

    animation.FuncAnimation(anim, updateData, blit=True, frames=TIME//velocidade, interval=intervalo, repeat=False)

    plt.show()