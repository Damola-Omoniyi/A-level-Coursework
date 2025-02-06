import math
import random


def sigmoid(x):
    y = (1 / (1 + math.e ** (-x)))
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

        Wd0 = (15, 0)  # attack
        Wd1 = (1, 10)  # jump
        Wd2 = (1, 15)  # block
        Wd3 = (15, 5)  # move away
        Wd4 = (10, 15)  # move towards
        Wd5 = (15, 2)  # special move
        Wd6 = (10, 3)  # idle

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
        self.layers[0] = self.input_layer
        layer_index = 0
        w_index = 0
        for layer in self.layers:
            node_index = 0
            for node in layer:
                if layer_index > 0:
                    res = mat_mul(self.weights[w_index][1], self.layers[layer_index - 1])
                    # res = sigmoid(res)
                    self.layers[layer_index][node_index] = res
                    node_index += 1
                    w_index += 1
            # print(self.layers[layer_index].index(max(self.layers[layer_index])))
            layer_index += 1

    def action(self):
        self.actions = ["attack", "jump", "block", "move away", "move towards", "special move", "idle"]
        action = self.layers[3].index(max(self.layers[3]))  # Select action with the highest value
        action_name = self.actions[action]  # Map index to action
        # print(action_name)
        self.action_stack.append(action)
        # print(self.layers[3])
        return action_name

    def perform(self):
        # print(self.input_layer)
        self.calc()
        return self.action()

ai = AI()
ai.input_layer = [12, 0, 0, 0, 1, 0.5]

#0-DISTANCE
#1- JUMPS
#2- ATTACKS
#3- BLOCK TIME
#4- HEALTH
#5- POWER

# ai.perform()
results = {"attack":0, "jump":0, "block":0, "move away":0, "move towards":0, "special move":0, "idle":0}

import itertools

def test_function(input_list):
    ai.input_layer = input_list
    results[ai.perform()] += 1
    # print(ai.perform(), results)
    # This is a dummy test function that simply returns the sum of the elements
    # print(input_list)

def generate_combinations_and_test():
    # Generate all combinations of length 6 with elements between 0 and 10
    combinations = itertools.product(range(11), repeat=6)

    results = []

    for combination in combinations:
        # Convert combination to a list
        combination = list(combination)

        # Divide the last two elements by 10
        combination[-2] /= 10
        combination[-1] /= 10

        # Run the test function with the modified combination
        test_function(combination)

generate_combinations_and_test()

import matplotlib.pyplot as plt

# Data
data = results

# Prepare data for plotting
labels = list(data.keys())
values = list(data.values())

# Create a figure with two subplots (1 row, 2 columns)
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Bar chart
axs[0].bar(labels, values, color='skyblue')
axs[0].set_title('Action Counts (Bar Chart)')
axs[0].set_ylabel('Count')
axs[0].set_xlabel('Actions')

# Pie chart
axs[1].pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
axs[1].set_title('Action Distribution (Pie Chart)')

# Adjust layout for better spacing
plt.tight_layout()

# Show the plot
plt.show()
print(results)