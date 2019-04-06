import math
import random
import time

class ANN:
    def __init__(self, training_set, test_set = None):
        with open(training_set, "r") as file:
            self.training_set = file.readlines()
        if test_set is not None:
            with open(test_set, "r") as file:
                self.test_set = file.readlines()

        self.num_inputs = len(self.training_set[0].rstrip().split()[:-1])
        self.num_outputs = len(set([i.split()[-1] for i in self.training_set]))
        self.num_hidden = math.ceil((2/3) * (self.num_inputs + self.num_outputs))
        self.input_hidden = [[random.uniform(-0.01, 0.01) for i in range(self.num_hidden)] for j in range(self.num_inputs - 1)]
        self.hidden_output = [[random.uniform(-0.01, 0.01) for i in range(self.num_hidden)] for j in range(self.num_outputs)]
        #self.input_hidden = [[1, 1, 0.5],[1,-1,2]]
        #self.hidden_output = [[1, 1.5, -1]]
        self.hidden_values = [0 for i in range(self.num_hidden - 1)]
        self.hidden_values.insert(0, 1)
        self.outputs = [0 for i in range(self.num_outputs)]
        self.target = 1
        self.learning_rate = 0.5
        self.total_error = -999

    def feed_forward(self):
        count = 0
        while True:
            count+=1
            #print(count)
            for data in range(len(self.training_set)):
                current_values = [float(i)/16 for i in self.training_set[data].split()[:-1]]
                #current_values = [int(i) for i in self.training_set[data].rstrip().split()[:-1]]
                #print(self.training_set)
                current_values = [-1 if i == 0.0 else i for i in current_values]
        #            print(current_values)
                print("Hidden vals: " + str(len(self.hidden_values)) + "\ninput hidden: " + str(len(self.input_hidden)) + "\ninput hidden[i]: " + str(len(self.input_hidden[0])) + "\nCurrent vals: " + str(len(current_values)))
                for val_input in range(len(self.input_hidden)):
                    for weight in range(len(self.input_hidden[val_input])):
                        #print(val_input)
                        #print(str(self.input_hidden[val_input][weight]) + " x " + str(current_values[val_input]) + " = " + str(self.input_hidden[val_input][weight] * current_values[val_input]))
                        self.hidden_values[val_input + 1] += self.input_hidden[val_input][weight] * current_values[weight]
                self.hidden_values = [1/(1+math.exp(-i)) for i in self.hidden_values[1:]]
                self.hidden_values.insert(0, 1)
                #print("Outputs:" + str(len(self.outputs)) + "\nHidden output:" + str(len(self.hidden_output)) + "\nHidden output[0]:" + str(len(self.hidden_output[0])) + "\nHidden values:" + str(len(self.hidden_values)))
                for val_hidden in range(len(self.hidden_output)):
                    for weight in range(len(self.hidden_output[val_hidden])):
                 #       print(str(val_hidden) + "," + str(weight))
                        self.outputs[val_hidden] += self.hidden_output[val_hidden][weight] * self.hidden_values[weight]
                self.outputs = [1/(1+math.exp(-i)) for i in self.outputs]
                
        #            print(str(self.total_error - sum([0.5 * ((1 - i) ** 2) for i in self.outputs])))
                if self.total_error - sum([0.5 * ((1 - i) ** 2) for i in self.outputs]) == 0.0:
                    return
                self.total_error = sum([0.5 * ((1 - i) ** 2) for i in self.outputs])

                self.back_propogate(current_values)
               # print(self.input_hidden)
                #print(self.hidden_output)

    def back_propogate(self, current_values):
        output_errors = [i*(1-i)*(self.target-i) for i in self.outputs]
        #hidden = h(1-h)sum(weight * error) for each output unit
        #0 = hidden to output 0, 1, 2...n
        #[-0.04736510639237634]
        #[[1, 1.5, -1]]
        
        hidden_output_error_sums = [0 for i in range(self.num_hidden - 1)]
        for hidden_output_weight in range(len(output_errors)):
            for hidden_node in range(len(self.hidden_output[hidden_output_weight][1:])): #all but bias
                #print(str(self.hidden_output[hidden_output_weight][hidden_node]) + " x " + str(output_errors[hidden_output_weight]) + ", weight is " + str(hidden_node))
                hidden_output_error_sums[hidden_node] += self.hidden_output[hidden_output_weight][hidden_node + 1]*output_errors[hidden_output_weight]
#        hidden_errors = [self.hidden_values[h]*(1-self.hidden_values[h] * hidden_output_error_sums[h]) for h in range(self.hidden_values)]
        #print("errs are " + str(hidden_output_error_sums))
        hidden_errors = [0 for h in range(self.num_hidden)]
        for h in range(self.num_hidden - 1):
            hidden_errors[h] = self.hidden_values[h+1]*(1-self.hidden_values[h+1]) * hidden_output_error_sums[h]
        #hidden_errors = [i*(1-i)* for i in self.hidden_values[1:]] #get weight
        #print("Hidden errors are " + str(hidden_errors))
        #print("Output errors are " + str(output_errors))
        self.learn(current_values, output_errors, hidden_errors)

    def learn(self, current_values, output_errors, hidden_errors):
        #w_ij = w_ij + learningrate * error(j) * value(j)
        #wnew = old + 0.5(learning_rate)(current_val)(1+Y)(1-Y)(Y-T
        #print(len(output_errors))
        #print(len(self.hidden_values))
        for val_hidden in range(len(self.hidden_output)):
            for weight in range(len(self.hidden_output[val_hidden])):
                self.hidden_output[val_hidden][weight] += self.learning_rate * output_errors[val_hidden] * self.hidden_values[weight]
                #self.hidden_output[val_hidden][weight] += (0.5 * self.learning_rate) * (self.hidden_values[val_hidden]) * (1+output_errors[weight]) * (1-output_errors[weight]) * (output_errors[weight] - self.target)

        for val_input in range(len(self.input_hidden)):
            for weight in range(len(self.input_hidden[val_input])):
                self.input_hidden[val_input][weight] += self.learning_rate * hidden_errors[val_input] * current_values[weight]
                #self.input_hidden[val_input][weight] += (0.5 * self.learning_rate) * (current_values[val_input]) * (1+hidden_errors[weight]) * (1-hidden_errors[weight]) * (hidden_errors[weight] - self.target)
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
    #ann_ex.predict()
