import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.pylab import *

def plotAnimations(i, v, LEN, TIME):
    plt.style.use('seaborn-pastel')

    # Seta algumas configurações
    #font = {'size' : 9}
    #matplotlib.rc('font', **font)

    # Configura a janela (figure) e os gráficos (subplots)
    f0 = figure(num = 0, figsize = (8, 6))
    #f0.suptitle("Tensao e Corrente", fontsize=10)
    volt = subplot2grid((2, 1), (0, 0))
    curr = subplot2grid((2, 1), (1, 0))
    #tight_layout()

    # Configura os titulos
    volt.set_title('Tensao')
    curr.set_title('Corrente')

    # Seta os limites para o eixo y
    volt.set_ylim(0,3)
    curr.set_ylim(0,0.05)

    # Seta os limites para o eixo x
    volt.set_xlim(0,LEN)
    curr.set_xlim(0,LEN)

    # Aciona o modo 'grid'
    volt.grid(True)
    curr.grid(True)

    # Nomeia os eixos
    volt.set_xlabel("m")
    volt.set_ylabel("tensao")
    curr.set_xlabel("m")
    curr.set_ylabel("corrente")

    # Vetores utilizados como eixo x
    tensaoEixoX= np.arange(LEN)
    correnteEixoX= np.arange(LEN+1)

    # Inicializa os gráficos
    p011, = volt.plot(tensaoEixoX, v[0], 'r-', label="tensao")
    p021, = curr.plot(correnteEixoX, i[0], 'b-', label="corrente")

    # Configura as legendas
    volt.legend([p011], [p011.get_label()])
    curr.legend([p021], [p021.get_label()])

    # Função que atualiza a animação
    def updateData(n):

        p011.set_data(tensaoEixoX, v[n])
        p021.set_data(correnteEixoX, i[n])

        return p011, p021

    # interval: desenhe um novo frame a cada 'interval' ms
    # frames: numero de frames a serem desenhados
    simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=TIME, interval=1, repeat=False)

    plt.show()
    # Uncomment the next line if you want to save the animation
    #simulation.save(filename='sim.mp4',fps=30,dpi=300)