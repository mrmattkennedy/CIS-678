import random

class ANN:
    def __init__(self, training_set):
        with open(training_set, "r") as file:
            self.training_set = file.readlines()
        self.perceptron = [{i:random.uniform(-0.01, 0.01) for i in range(len(self.training_set[0].split()) - 1)} for j in range(10)]
        self.outputs = [0 for i in range(10)]
    def feed_forward(self):
        current_values = [int(i) for i in self.training_set[0].split()[:-1]]
        for dictionary in range(len(self.perceptron)):
            for value in range(len(self.perceptron[dictionary])):
                self.outputs[dictionary] += self.perceptron[dictionary][value] * current_values[value]

#        print([round(i, 3) for i in self.outputs])
        error = 0.5*sum([1-i for i in self.outputs]) ** 2
        print(error)

for _ in range(15):
    ann_ex = ANN("digits-training.data")
    ann_ex.feed_forward()
