import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pylab import *
import mpl_toolkits.mplot3d.axes3d as p3

def plotAnimations(Ez, LEN, TIME, AnimZmax, AnimZmin, velocidade = 1, intervalo = 5):
    plt.style.use('seaborn-pastel')
    # Cria a figura
    fig = plt.figure()
    anim = p3.Axes3D(fig)
    anim = plt.axes(projection='3d')

    # Nomeia as figuras
    #anim.canvas.set_window_title('Animações')

    # Seta os limites para o eixo z
    if(AnimZmax != None):
            anim.set_zlim3d(AnimZmin, AnimZmax)

    # Nomeia os eixos
    anim.set_xlabel("Eixo X")
    anim.set_ylabel("Eixo Y")

    # Vetores utilizados como eixo X e Y e Z
    x = np.linspace(-100, 100, 101)
    y = np.linspace(-100, 100, 101)
    X, Y = np.meshgrid(x, y)
    Z = Ez[0]

    # Inicializa os gráficos
    line = anim.plot_surface(X, Y, Z, cmap='seismic')

    # Função que atualiza a animação
    def updateData(n, line, AnimZmin, AnimZmax):
        anim.clear()
        line = anim.plot_surface(X, Y, Ez[n*velocidade],rcount = 80 , ccount = 80, cmap='seismic')
        if(AnimZmax != None):
            anim.set_zlim3d(AnimZmin, AnimZmax)
        return line , anim

    simulation = animation.FuncAnimation(fig, updateData, fargs = {line, AnimZmin, AnimZmax},  blit=False, frames=TIME//velocidade, interval=intervalo, repeat=False)

    plt.show()

    

