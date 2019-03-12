import time
import itertools
from math import log
from collections import deque

training_set = []

class Node:
    def __init__(self, attribute, value = None, parent = None, children = []):
        self.parent = parent
        self.value = value
        self.attribute = attribute
        self.children = children
        
    def add_child(self, child):
        self.children.append(child)
    """
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.attribute)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
    def __repr__(self):
        return '<tree node representation>'
    """
    
class decision_tree:
    def __init__(self):
        with open("fishing.data", "r") as file:
            self.training_set = deque(file.readlines())
            
        self.classes = self.training_set[1].rstrip().split(",")
        self.attributes = []
        for attribute in range(int(self.training_set[2])):
            tmp = self.training_set[attribute + 3].rstrip().split(",")
            self.attributes.append(tmp)

    def create_leaf(self, branch_value = None, training_set = None, classes = None, class_entropy = None, attributes = None, parent = None):
        if training_set is None:
            training_set = self.training_set
            training_set = deque(itertools.islice(training_set, int(training_set[2]) + 4, len(training_set)))
        if classes is None:
            classes = self.classes
        if attributes is None:
            attributes = self.attributes
        #get all classes possible to create possibilities of it being a given class. Used for entropy of S
        class_probabilities = deque()
        attribute_totals_per_class = deque()
        for possible_class in range(len(self.classes)):
            class_probabilities.append(0)
        print(parent.attribute)
        print(len(parent.children))
        #get all attributes and count totals for given class
        for possible_attribute in range(len(attributes)):
            tmp = []
            for possible_val in range(len(attributes[possible_attribute]) - 2):
                tmp.append([0 for poss_class in classes])
            attribute_totals_per_class.append(tmp)

        matching_values = [self.attributes.index(item) for item in attributes]
        #get the probabilities of an attribute in a given class
        for item in range(len(training_set)):
            current_item = training_set[item].rstrip().split(',')
            #get class probs
            item_class = current_item[-1]
            class_probabilities[classes.index(item_class)] += 1
            
            #get attr probs per class
            for attr in range(len(matching_values)):
                attr_index = attributes[attr][2:].index(current_item[matching_values[attr]])
                attribute_totals_per_class[attr][attr_index][classes.index(item_class)] += 1
                
        count = 0
        total = sum(class_probabilities)
        if total is 0:
            return
        class_probabilities = [float(prob/total) for prob in class_probabilities]

        if class_entropy is None:
            total_entropy = 0
            for prob in class_probabilities:
                total_entropy -= prob * log(prob, len(classes))
            class_entropy = total_entropy
            
        attribute_entropies = []
        total_entropies = []
        gains = []
        #print(attribute_totals_per_class)
        for attr in range(len(attributes)):
            attribute_entropies.clear()
            for value in range(len(attributes[attr]) - 2): #offset for name and # values
                total_attr = sum(attribute_totals_per_class[attr][value])
                if total_attr == 0:
                    attr_prob = [0 for count in attribute_totals_per_class[attr][value]]
                else:
                    attr_prob = [float(count/total_attr) for count in attribute_totals_per_class[attr][value]]
                attr_entropy = 0
                for prob in attr_prob:
                    if (prob != 0):
                        attr_entropy -= prob * log(prob, len(classes))
                attribute_entropies.append(attr_entropy)
            gain = class_entropy
            for i in range(len(attribute_entropies)):
                gain -= attribute_entropies[i] * float(sum(attribute_totals_per_class[attr][i])/total)
            gains.append(gain)
            total_entropies.append(attribute_entropies.copy())

        max_attribute = attributes[gains.index(max(gains))]
        max_attribute_index = attributes.index(max_attribute)
        #print(max_attribute)
        current = Node(max_attribute, branch_value, parent)
        parent.add_child(current)
        new_attributes = attributes.copy()
        new_attributes.remove(max_attribute)
        #print(gains)
        #print(parent.attribute)
        for value in range(2, len(attributes[attributes.index(max_attribute)])):
            if total_entropies[max_attribute_index][value - 2] == 0:
                for item in range(len(training_set)):
                    current_item = training_set[item].rstrip().split(',')
                    if max_attribute[value] == current_item[max_attribute_index]:
                        end = Node(current_item[len(current_item)-1], max_attribute[value], current)
                        current.add_child(end)
                        break
            else:      
                new_training_set = []
                for item in range(len(training_set)):
                    current_item = training_set[item].rstrip().split(',')
                    if max_attribute[value] == current_item[max_attribute_index]:
                        new_training_set.append(training_set[item].rstrip())
                #create_leaf(self, branch_value = None, training_set = None, classes = None, class_entropy = None, new_attributes = None, parent = None):
                self.create_leaf(max_attribute[value], new_training_set, classes, total_entropies[max_attribute_index][value - 2], new_attributes, parent=current)
                

startTime = time.time()    
root = Node(None)
dt = decision_tree()
dt.create_leaf(parent=root)
print(str(time.time() - startTime))
temp = root
#for child in root.children:
    #print(child.attribute)
    
print(len(root.children))
