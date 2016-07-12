import numpy as np

def Heaviside (x):
    return 1 if x >= 0 else 0

class Perceptron:
    def __init__ (self, *weights):
        self.weights = np.array(weights)

    def activate (self, *input):
        input = np.hstack(([1], input))
        return Heaviside(np.sum(self.weights * input))
