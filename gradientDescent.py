import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

# grad must be the gradient of f
def gradDesc (f, grad, xRange = [-1.2, 1.2], yRange = [-1.2, 1.2], gamma = 0.2, steps = 5, start = [0, 0]):
    fig = plt.figure(figsize = (20, 10))

    descX = [start[0]]
    descY = [start[1]]
    for i in range(1, steps):
        g = grad(descX[i - 1], descY[i - 1])
        descX += [descX[i - 1] - gamma * g[0]]
        descY += [descY[i - 1] - gamma * g[1]]

    x, y = np.meshgrid(
        np.linspace(xRange[0], xRange[1], 200),
        np.linspace(yRange[0], yRange[1], 200)
    )
    vf = np.vectorize(f)
    z = vf(x, y)

    ax = fig.add_subplot(1, 2, 1, projection = '3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(elev=60, azim=-70)
    ax.plot_surface(x, y, z, cmap=cm.gray)
    ax.plot(descX, descY, vf(descX, descY), c = 'r', linewidth=3)

    ax = fig.add_subplot(1, 2, 2)
    ax.contourf(x, y, z, cmap=cm.gray)
    ax.arrow(descX[0], descY[0], (descX[0] - descX[1]) / gamma, (descY[0] - descY[1]) / gamma, color = 'b')
    ax.scatter(descX, descY, c = 'r', s=40)
    plt.show()

def h1 (x, y):
    return 0.5 * x * x - 0.25 * y * y + 3

def h2 (x, y):
    return 2 * x + 1 - np.exp(y)

def F (x, y):
    return np.sin(h1(x, y)) * np.cos(h2(x, y))

def gradF (x, y):
    return [
        np.cos(h1(x, y)) * x * np.cos(h2(x, y)) - 2 * np.sin(h1(x, y)) * np.sin(h2(x, y)),
        -0.5 * np.cos(h1(x, y)) * y * np.cos(h2(x, y)) + np.sin(h1(x, y)) * np.sin(h2(x, y)) * np.exp(y)
    ]

def example ():
    gradDesc(F, gradF, start = [0.2, 0.4], steps = 20, gamma = 0.2)
