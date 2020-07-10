import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pylab import *

def plotAnimations(Ez, Hy, LEN, l, TIME, velocidade = 5, intervalo = 20):
    plt.style.use('seaborn-pastel')

    # Cria as figuras
    anim = plt.figure(num = 0, figsize = (8, 6))

    # Nomeia as figuras
    anim.canvas.set_window_title('Animações')

    #Cria os subplots de cada figura
    EAnim = plt.subplot2grid((2, 1), (0, 0), fig=anim)
    HAnim = plt.subplot2grid((2, 1), (1, 0), fig=anim)

    # Configura os titulos dos subplots
    EAnim.set_title('Ez')
    HAnim.set_title('Hy')

    # Seta os limites para o eixo y
    EAnim.set_ylim(-1.5,1.5)
    HAnim.set_ylim(-0.01,0.01)

    # Seta os limites para o eixo x
    EAnim.set_xlim(0,LEN)
    HAnim.set_xlim(0,LEN+1)

    # Seta os ticklabels para o eixo x
    EAnim.set_xticklabels(EAnim.get_xticks()/LEN)
    HAnim.set_xticklabels(HAnim.get_xticks()/LEN)

    # Aciona o modo 'grid'
    EAnim.grid(True)
    HAnim.grid(True)

    # Nomeia os eixos
    EAnim.set_xlabel("Ez EixoX")
    EAnim.set_ylabel("Ez EixoY")
    HAnim.set_xlabel("Hy EixoX")
    HAnim.set_ylabel("Hy EixoY")

    # Vetores utilizados como eixo x
    EzEixoX= np.arange(LEN+1)
    HyEixoX= np.arange(LEN)

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