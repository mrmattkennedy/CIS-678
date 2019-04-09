import math
import random
import time

"""
Artificial Neural Network. Made to work generically with any training set provided.
"""
class ANN:
    def __init__(self, training_set, test_set = None, learning_rate = 0.001):
        with open(training_set, "r") as file:
            self.training_set = file.readlines()
        if test_set is not None:
            with open(test_set, "r") as file:
                self.test_set = file.readlines()

        self.num_inputs = len(self.training_set[0].rstrip().split()[:-1])
        self.num_outputs = len(set([i.split()[-1] for i in self.training_set]))
        self.num_hidden = math.ceil((2/3) * (self.num_inputs + self.num_outputs))
        self.input_hidden = [[random.uniform(-0.01, 0.01) for i in range(self.num_hidden)] for j in range(self.num_hidden - 1)]
        self.hidden_output = [[random.uniform(-0.01, 0.01) for i in range(self.num_hidden)] for j in range(self.num_outputs)]
        self.hidden_values = [0 for i in range(self.num_hidden - 1)]
        self.hidden_values.insert(0, 1)
        self.outputs = [0 for i in range(self.num_outputs)]
        self.target = 1
        self.learning_rate = learning_rate
        self.total_error = 999
        self.total_right = 0
        self.total_iterations = 0
        
    def reset(self):
        print(str(self.total_right) + "/" + str(self.total_iterations * 1797) + ", " + str(round((self.total_right / (self.total_iterations * 1797)) * 100, 2)) + "% accuracy")
        self.total_right = 0
        self.total_iterations = 0

    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate

    def feed_forward(self):
        count = 0
        while True:
            for data in range(len(self.training_set)):
                current_values = [float(i)/16 for i in self.training_set[data].split()[:-1]]
                current_values = [-1 if i == 0.0 else i for i in current_values]
                
                for val_input in range(len(self.input_hidden)):
                    for weight in range(len(self.input_hidden[val_input])):
                        self.hidden_values[weight] += self.input_hidden[val_input][weight] * current_values[weight]
                self.hidden_values = [(2/(1+math.exp(-i))) - 1 for i in self.hidden_values[1:]]
                self.hidden_values.insert(0, 1)
                for val_hidden in range(len(self.hidden_output)):
                    for weight in range(len(self.hidden_output[val_hidden])):
                        self.outputs[val_hidden] += self.hidden_output[val_hidden][weight] * self.hidden_values[val_hidden]
                self.outputs = [(math.exp(i)/sum([math.exp(j) for j in self.outputs])) for i in self.outputs]
                if (self.total_error - sum([0.5 * ((1 - i) ** 2) for i in self.outputs])) <= 0.00000001:
                    return
                self.total_error = sum([0.5 * ((1 - i) ** 2) for i in self.outputs])
                self.back_propogate(current_values)

    def back_propogate(self, current_values):
        output_errors = [i*(1-i)*(self.target-i) for i in self.outputs]
        #hidden = h(1-h)sum(weight * error) for each output unit
        #0 = hidden to output 0, 1, 2...n        
        hidden_output_error_sums = [0 for i in range(self.num_hidden - 1)]
        for hidden_output_weight in range(len(output_errors)):
            for hidden_node in range(len(self.hidden_output[hidden_output_weight][1:])): #all but bias
                hidden_output_error_sums[hidden_node] += self.hidden_output[hidden_output_weight][hidden_node + 1]*output_errors[hidden_output_weight]
        hidden_errors = [0 for h in range(self.num_hidden)]
        for h in range(self.num_hidden - 1):
            hidden_errors[h] = self.hidden_values[h+1]*(1-self.hidden_values[h+1]) * hidden_output_error_sums[h]
        self.learn(current_values, output_errors, hidden_errors)

    def learn(self, current_values, output_errors, hidden_errors):
        #w_ij = w_ij + learningrate * error(j) * value(j)
        #wnew = old + 0.5(learning_rate)(current_val)(1+Y)(1-Y)(Y-T)
        for val_hidden in range(len(self.hidden_output)):
            for weight in range(len(self.hidden_output[val_hidden])):
                self.hidden_output[val_hidden][weight] += self.learning_rate * output_errors[val_hidden] * self.hidden_values[weight]
                #self.hidden_output[val_hidden][weight] += (0.5 * self.learning_rate) * (self.hidden_values[val_hidden]) * (1+output_errors[weight]) * (1-output_errors[weight]) * (output_errors[weight] - self.target)
                
        for val_input in range(len(self.input_hidden)):
            for weight in range(len(self.input_hidden[val_input])):
                self.input_hidden[val_input][weight] += self.learning_rate * hidden_errors[val_input] * current_values[weight]
                #self.input_hidden[val_input][weight] += (0.5 * self.learning_rate) * (current_values[val_input]) * (1+hidden_errors[weight]) * (1-hidden_errors[weight]) * (hidden_errors[weight] - self.target)
    def predict(self):
        total = 0
        total_right = 0
        for data in range(len(self.test_set)):
            current_values = [float(i)/16 for i in self.training_set[data].split()[:-1]]
            current_values = [-1 if i == 0.0 else i for i in current_values]
            self.hidden_values = [0 for i in range(self.num_hidden)]
            self.outputs = [0 for i in range(self.num_outputs)]
            for val_input in range(len(self.input_hidden)):
                for weight in range(len(self.input_hidden[val_input])):
                    self.hidden_values[weight] += self.input_hidden[val_input][weight] * current_values[val_input]
                    if math.isnan(self.hidden_values[weight]):
                        return
            for val_hidden in range(len(self.hidden_output)):
                for weight in range(len(self.hidden_output[val_hidden])):
                    self.outputs[val_hidden] += self.hidden_output[val_hidden][weight] * self.hidden_values[val_hidden]

            self.total_error = sum([0.5 * ((1 - i) ** 2) for i in self.outputs])
            total+=1
            if int(self.outputs.index(max(self.outputs))) == int(self.training_set[data].split()[-1]):
                total_right+=1
        self.total_right += total_right
        self.total_iterations += 1
        return

for i in range(10):
    ann_ex = ANN("digits-training.data", "digits-test.data")
    print("Learning rate is " + str(1/((i+1) * 1000)))
    for _ in range(5):
        ann_ex.set_learning_rate(1/((i+1) * 1000))
        ann_ex.feed_forward()
        ann_ex.predict()
    ann_ex.reset()
