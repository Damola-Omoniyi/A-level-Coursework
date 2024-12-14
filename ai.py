import math
import random

def sigmoid(x):
    y = 1 / (1 + math.e ** (-x))
    return y
def mat_mul(a, b):
    sm = 0
    for i in range(len(a)):
        sm += a[i] * b[i]
    return sm

class AI:
    def __init__(self):
        self.input_layer = [0, 0, 0, 0, 0, 0]
        Wb0 = (0.05, 10, 5, 0.01, 2, 10)
        Wb1 = (1, 2, 2.5, 7.5, 10, 2)
        Wb2 = (10, 0.05, 0.1, 11, 8, 0.1)

        Wc0 = (2, 6.5, 10)
        Wc1 = (12, 4.5, 1.5)

        Wd0 = (15, 2)  # attack
        Wd1 = (7, 10)  # jump
        Wd2 = (5, 15)  # block
        Wd3 = (3.5, 10)  # move away
        Wd4 = (10, 3)  # move towards
        Wd5 = (15, 2)  # special move
        Wd6 = (0.01, 3)  # idle

        b0 = 1
        b1 = 1
        b2 = 1

        c0 = 1
        c1 = 1

        d0 = 1
        d1 = 1
        d2 = 1
        d3 = 1
        d4 = 1
        d5 = 1
        d6 = 1

        self.layers = [self.input_layer,
                  [b0, b1, b2],
                  [c0, c1],
                  [d0, d1, d2, d3, d4, d5, d6]]
        self.weights = [[b0, Wb0], [b1, Wb1], [b2, Wb2], [c0, Wc0], [c1, Wc1], [d0, Wd0], [d1, Wd1], [d2, Wd2],
                        [d3, Wd3],
                   [d4, Wd4], [d5, Wd5], [d6, Wd6]]
        self.action_stack = []

    def calc(self):
        layer_index = 0
        w_index = 0
        for layer in self.layers:
            node_index = 0
            for node in layer:
                if layer_index > 0:
                    res = mat_mul(self.weights[w_index][1], self.layers[layer_index - 1])
                    res = sigmoid(res)
                    self.layers[layer_index][node_index] = res
                    node_index += 1
                    w_index += 1
            layer_index += 1

    def action(self):
        action = random.choice(self.layers[3])
        action = self.layers[3].index(action)
        self.action_stack.append(action)

    def perform(self):
        self.calc()
        self.action()