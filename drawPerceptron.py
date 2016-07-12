import numpy as np
import matplotlib.pyplot as plt

def draw(input, w):
    xMin = np.min(input[:, 0])
    xMax = np.max(input[:, 0])
    yMin = np.min(input[:, 1])
    yMax = np.max(input[:, 1])
    plt.figure()
    plt.xlim(xMin - 0.2 * (xMax - xMin), xMax + 0.2 * (xMax - xMin))
    plt.ylim(yMin - 0.2 * (yMax - yMin), yMax + 0.2 * (yMax - yMin))
    if w[1] != 0:
        plt.plot((- w[0] - w[2] * input[:2, 1]) / w[1], input[:2, 1])
    elif w[2] != 0:
        plt.plot(input[:2, 0], (- w[0] - w[1] * input[:2, 0]) / w[2])        
    for c, i in [('g', 1), ('r', 0)]:
        indices = (input[:, 2] == i)
        plt.scatter(input[indices, 0], input[indices, 1], c=c, s=50)
