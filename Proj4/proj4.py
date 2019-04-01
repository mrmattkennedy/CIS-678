import math
import random
import time

class ANN:
    def __init__(self, training_set, test_set):
        with open(training_set, "r") as file:
            self.training_set = file.readlines()
        with open(test_set, "r") as file:
            self.test_set = file.readlines()

        self.num_inputs = len(self.training_set[0].split()[:-1])
        self.num_outputs = len(set([i.split()[-1] for i in self.training_set]))
        self.num_hidden = math.ceil((2/3) * (self.num_inputs + self.num_outputs))
        self.input_hidden = [[random.uniform(-0.01, 0.01) for i in range(self.num_hidden)] for j in range(self.num_inputs)]
        self.hidden_output = [[random.uniform(-0.01, 0.01) for i in range(self.num_outputs)] for j in range(self.num_hidden)]
        self.hidden_values = [0 for i in range(self.num_hidden)]
        self.outputs = [0 for i in range(self.num_outputs)]
        self.target = 0.5
        self.learning_rate = 0.01
        self.total_error = -999

    def feed_forward(self):
        count = 0
        while True:
            count+=1
            print(count)
            for data in range(len(self.training_set)):
                current_values = [float(i)/16 for i in self.training_set[data].split()[:-1]]
                current_values = [-1 if i == 0.0 else i for i in current_values]
    #            print(current_values)
                for val_input in range(len(self.input_hidden)):
                    for weight in range(len(self.input_hidden[val_input])):
                        self.hidden_values[weight] += self.input_hidden[val_input][weight] * current_values[val_input]
     
                self.hidden_values = [1/(1+math.exp(-i)) for i in self.hidden_values]
                for val_hidden in range(len(self.hidden_values)):
                    for weight in range(len(self.hidden_output[val_hidden])):
                        self.outputs[weight] += self.hidden_output[val_hidden][weight] * self.hidden_values[val_hidden]
                self.outputs = [math.exp(i)/sum([math.exp(j) for j in self.outputs]) for i in self.outputs]
    #            print(str(self.total_error - sum([0.5 * ((1 - i) ** 2) for i in self.outputs])))
                if self.total_error - sum([0.5 * ((1 - i) ** 2) for i in self.outputs]) == 0.0:
                    return
                self.total_error = sum([0.5 * ((1 - i) ** 2) for i in self.outputs])
                self.back_propogate(current_values)

    def back_propogate(self, current_values):
        output_errors = [i*(1-i)*(self.target-i) for i in self.outputs]
        #hidden = h(1-h)sum(weight * error) for each output unit
        #0 = hidden to output 0, 1, 2...n
        hidden_errors = [h * (1 - h) * sum(j) for j in self.hidden_output for h in self.hidden_values]
#        print("Hidden errors are " + str(hidden_errors))
        self.learn(current_values, output_errors, hidden_errors)

    def learn(self, current_values, output_errors, hidden_errors):
        #w_ij = w_ij + learningrate * error(j) * value(j)
        #wnew = old + 0.5(learning_rate)(current_val)(1+Y)(1-Y)(Y-T
        for val_hidden in range(len(self.hidden_values)):
            for weight in range(len(self.hidden_output[val_hidden])):
                #self.hidden_output[val_hidden][weight] += self.learning_rate * output_errors[weight] * self.hidden_values[val_hidden]
                self.hidden_output[val_hidden][weight] += (0.5 * self.learning_rate) * (self.hidden_values[val_hidden]) * (1+output_errors[weight]) * (1-output_errors[weight]) * (output_errors[weight] - self.target)

        for val_input in range(len(self.input_hidden)):
            for weight in range(len(self.input_hidden[val_input])):
                #self.input_hidden[val_input][weight] += self.learning_rate * hidden_errors[weight] * current_values[val_hidden]
                self.input_hidden[val_input][weight] += (0.5 * self.learning_rate) * (current_values[val_input]) * (1+hidden_errors[weight]) * (1-hidden_errors[weight]) * (hidden_errors[weight] - self.target)
    def predict(self):
        """
        file_to_open = open("weights.txt", "w")
        for val_input in range(len(self.input_hidden)):
            for weight in range(len(self.input_hidden[val_input])):
                file_to_open.write(str(val_input) + "," + str(weight) + ": " + str(self.input_hidden[val_input][weight]) + "\n")
       """
#        weight_file = open("values.txt", "w")

 #       file_to_open.close()
        total = 0
        total_right = 0
        for data in range(len(self.test_set)):
            current_values = [float(i)/16 for i in self.training_set[data].split()[:-1]]
            current_values = [-1 if i == 0.0 else i for i in current_values]
            #print(current_values)
            self.hidden_values = [0 for i in range(self.num_hidden)]
            self.outputs = [0 for i in range(self.num_outputs)]
             #weight_file.write("\n\n" + str(current_values) + "\n\n")
            for val_input in range(len(self.input_hidden)):
                for weight in range(len(self.input_hidden[val_input])):
                    #print(str(val_input) + "," + str(weight) + ": " + str(self.input_hidden[val_input][weight]))
                    self.hidden_values[weight] += self.input_hidden[val_input][weight] * current_values[val_input]
                    if math.isnan(self.hidden_values[weight]):
   #                     weight_file.close()
                        return
                    #weight_file.write(str(val_input) + "," + str(weight) + "\t" + str(self.input_hidden[val_input][weight]) + ":" + str(current_values[val_input]) + "\t" +str(self.hidden_values[weight]) + "\n")

  
    #        self.hidden_values = [1/(1+math.exp(-i)) for i in self.hidden_values]
            #print(self.hidden_values[0])
            for val_hidden in range(len(self.hidden_values)):
                for weight in range(len(self.hidden_output[val_hidden])):
                    self.outputs[weight] += self.hidden_output[val_hidden][weight] * self.hidden_values[val_hidden]

            #self.back_propogate(current_values)
            self.total_error = sum([0.5 * ((1 - i) ** 2) for i in self.outputs])
            total+=1
            if self.outputs.index(max(self.outputs)) + 1 == self.training_set[data].split()[-1]:
                total_right+=1
            print(str(total) + ":" + str(total_right))
            #print(str(self.outputs.index(max(self.outputs)) + 1) + ":" + str(self.training_set[data].split()[-1]))
 #           print(self.outputs)
#            time.sleep(0.5)
        return

for _ in range(1):
    ann_ex = ANN("digits-training.data", "digits-test.data")
    ann_ex.feed_forward()
    ann_ex.predict()
