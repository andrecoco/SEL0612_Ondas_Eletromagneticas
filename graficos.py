import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.pylab import *

def plotAnimations(i, v, LEN, TIME, dz, tomarMedia, velocidade, intervalo):
    plt.style.use('seaborn-pastel')

    # Cria as figuras
    estatVolt = figure(num = 1, figsize = (8, 6))
    estatCurr = figure(num = 2, figsize = (8, 6))
    anim = figure(num = 0, figsize = (8, 6))

    # Nomeia as figuras
    anim.canvas.set_window_title('Animações')
    estatVolt.canvas.set_window_title('Gráficos Estáticos da Tensao')
    estatCurr.canvas.set_window_title('Gráficos Estáticos da Corrente')

    #Cria os subplots de cada figura
    voltAnim = subplot2grid((2, 1), (0, 0), fig=anim)
    currAnim = subplot2grid((2, 1), (1, 0), fig=anim)

    voltMiddle = subplot2grid((3, 1), (0, 0), fig=estatVolt)
    voltEnd = subplot2grid((3, 1), (1, 0), fig=estatVolt)
    voltEstationary = subplot2grid((3, 1), (2, 0), fig=estatVolt)
    
    currMiddle = subplot2grid((3, 1), (0, 0), fig=estatCurr)
    currEnd = subplot2grid((3, 1), (1, 0), fig=estatCurr)
    currEstationary = subplot2grid((3, 1), (2, 0), fig=estatCurr)

    # Configura os titulos dos subplots
    if(tomarMedia):
        voltAnim.set_title('Tensão (com filtro de média)')
        currAnim.set_title('Corrente (com filtro de média)')

        voltMiddle.set_title('Tensão após Percorrer Metade da Linha de Transmissão (com filtro de média)')
        voltEnd.set_title('Tensão após uma Reflexão (com filtro de média)')
        voltEstationary.set_title('Tensão no Regime Estacionário (com filtro de média)')

        currMiddle.set_title('Corrente após Percorrer Metade da Linha de Transmissão (com filtro de média)')
        currEnd.set_title('Corrente após uma Reflexão (com filtro de média)')
        currEstationary.set_title('Corrente no Regime Estacionário (com filtro de média)')
    else:
        voltAnim.set_title('Tensão')
        currAnim.set_title('Corrente')

        voltMiddle.set_title('Tensão após Percorrer Metade da Linha de Transmissão')
        voltEnd.set_title('Tensão após uma Reflexão')
        voltEstationary.set_title('Tensão no Regime Estacionário')

        currMiddle.set_title('Corrente após Percorrer Metade da Linha de Transmissão')
        currEnd.set_title('Corrente após uma Reflexão')
        currEstationary.set_title('Corrente no Regime Estacionário')

    # Seta os limites para o eixo y
    voltAnim.set_ylim(-3,3)
    currAnim.set_ylim(-0.05,0.05)

    voltMiddle.set_ylim(-3,3)
    voltEnd.set_ylim(-3,3)
    voltEstationary.set_ylim(-3,3)

    currMiddle.set_ylim(-0.05,0.05)
    currEnd.set_ylim(-0.05,0.05)
    currEstationary.set_ylim(-0.05,0.05)

    # Seta os limites para o eixo x
    voltAnim.set_xlim(0,LEN)
    currAnim.set_xlim(0,LEN+1)

    voltMiddle.set_xlim(0,LEN)
    voltEnd.set_xlim(0,LEN)
    voltEstationary.set_xlim(0,LEN)

    currMiddle.set_xlim(0,LEN+1)
    currEnd.set_xlim(0,LEN+1)
    currEstationary.set_xlim(0,LEN+1)

    # Seta os ticklabels para o eixo x
    voltAnim.set_xticklabels(voltAnim.get_xticks()/LEN)
    currAnim.set_xticklabels(currAnim.get_xticks()/LEN)

    voltMiddle.set_xticklabels(voltMiddle.get_xticks()/LEN)
    voltEnd.set_xticklabels(voltEnd.get_xticks()/LEN)
    voltEstationary.set_xticklabels(voltEstationary.get_xticks()/LEN)

    currMiddle.set_xticklabels(currMiddle.get_xticks()/LEN)
    currEnd.set_xticklabels(currEnd.get_xticks()/LEN)
    currEstationary.set_xticklabels(currEstationary.get_xticks()/LEN)

    # Aciona o modo 'grid'
    voltAnim.grid(True)
    currAnim.grid(True)
    
    voltMiddle.grid(True)
    voltEnd.grid(True)
    voltEstationary.grid(True)

    currMiddle.grid(True)
    currEnd.grid(True)
    currEstationary.grid(True)

    # Nomeia os eixos
    voltAnim.set_xlabel("Posição (m)")
    voltAnim.set_ylabel("Tensão (V)")
    currAnim.set_xlabel("Posição (m)")
    currAnim.set_ylabel("Corrente (A)")

    voltMiddle.set_xlabel("Posição (m)")
    voltMiddle.set_ylabel("Tensão (V)")
    voltEnd.set_xlabel("Posição (m)")
    voltEnd.set_ylabel("Tensão (V)")
    voltEstationary.set_xlabel("Posição (m)")
    voltEstationary.set_ylabel("Tensão (V)")

    currMiddle.set_xlabel("Posição (m)")
    currMiddle.set_ylabel("Corrente (A)")
    currEnd.set_xlabel("Posição (m)")
    currEnd.set_ylabel("Corrente (A)")
    currEstationary.set_xlabel("Posição (m)")
    currEstationary.set_ylabel("Corrente (A)")

    # Vetores utilizados como eixo x
    tensaoEixoX= np.arange(LEN)
    correnteEixoX= np.arange(LEN+1)

    # Ajeita o Layout
    anim.tight_layout()
    estatVolt.tight_layout()
    estatCurr.tight_layout()

    # Inicializa os gráficos
    if(tomarMedia):
        p011, = voltAnim.plot(np.convolve(v[0], np.ones(5)*(1/5),mode="same"), 'r-')
        p021, = currAnim.plot(np.convolve(i[0], np.ones(5)*(1/5),mode="same"), 'b-')

        p111, = voltMiddle.plot(np.convolve(v[TIME//20], np.ones(5)*(1/5),mode="same"), 'r-')
        p121, = voltEnd.plot(np.convolve(v[TIME//10 + TIME//40], np.ones(5)*(1/5),mode="same"), 'r-')
        p131, = voltEstationary.plot(np.convolve(v[TIME - 1], np.ones(5)*(1/5),mode="same"), 'r-')

        p211, = currMiddle.plot(np.convolve(i[TIME//20], np.ones(5)*(1/5),mode="same"), 'b-')
        p221, = currEnd.plot(np.convolve(i[TIME//10 + TIME//40], np.ones(5)*(1/5),mode="same"), 'b-')
        p231, = currEstationary.plot(np.convolve(i[TIME - 1], np.ones(5)*(1/5),mode="same"), 'b-')
    else:
        p011, = voltAnim.plot(v[0], 'r-')
        p021, = currAnim.plot(i[0], 'b-')

        p111, = voltMiddle.plot(v[TIME//20], 'r-')
        p121, = voltEnd.plot(v[TIME//10 + TIME//40], 'r-')
        p131, = voltEstationary.plot(v[TIME - 1], 'r-')

        p211, = currMiddle.plot(i[TIME//20], 'b-')
        p221, = currEnd.plot(i[TIME//10 + TIME//40], 'b-')
        p231, = currEstationary.plot(i[TIME - 1], 'b-')

    # Função que atualiza a animação
    def updateData(n):
        if(tomarMedia):
            p011.set_data(tensaoEixoX, np.convolve(v[n*velocidade], np.ones(5)*(1/5),mode="same"))
            p021.set_data(correnteEixoX, np.convolve(i[n*velocidade], np.ones(5)*(1/5),mode="same"))
        else:
            p011.set_data(tensaoEixoX, v[n*velocidade])
            p021.set_data(correnteEixoX, i[n*velocidade])

        return p011, p021

    simulation = animation.FuncAnimation(anim, updateData, blit=True, frames=TIME//velocidade, interval=intervalo, repeat=False)

    plt.show()
    # Descomente a próxima linha se deseja salvar a animação
    # simulation.save(filename='animacao.mp4',fps=30,dpi=300)