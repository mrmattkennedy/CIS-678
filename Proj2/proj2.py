#!/usr/bin/env python
import time
from nltk.corpus import wordnet as wn
from nltk import PorterStemmer
from itertools import chain
from operator import itemgetter
from math import log
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


"""
Document classifier class
Instance variables:
total - Total number of docs
total_types - Total number of doc types
words - total number of words
class_probability - the probability for a document type
word_category_probabilities - probability for a word in a category
test_documents - the test data
"""
class doc_classifier:
    def __init__(self):
        self.totals_list = [["atheism", 480],
                       ["graphics", 584],
                       ["mswindows", 572],
                       ["pc", 590],
                       ["mac", 578],
                       ["windows", 593],
                       ["forsale", 585],
                       ["autos", 594],
                       ["motorcycles", 598],
                       ["baseball", 597],
                       ["hockey", 600],
                       ["cryptology", 595],
                       ["electronics", 591],
                       ["medicine", 594],
                       ["space", 593],
                       ["christianity", 598],
                       ["guns", 545],
                       ["mideastpolitics", 564],
                       ["politics", 465],
                       ["religion", 377]]
        self.total = 11293
        self.total_types = 20
        self.words = []
        self.class_probability = []
        self.word_category_probabilities= []
        self.test_documents = []

    """
    Gets the word counts for each document type and saves to a file.
    Much faster to read the counts.
    """
    def save_word_counts(self, file_name):
        training_data = open("forumTraining.data", "r")
        documents = [line for line in training_data.readlines()]
        words = [document.split() for document in documents]
        ps = PorterStemmer() #stemmer for use if desired

        word_count = [] #used to store count of word per category
        word_count_file = open(file_name, "w")
        start_index = 0
        
        for topic in range(0, len(self.totals_list)): #topic is the number of document types
            word_count_file.write(self.totals_list[topic][0] + " -1" + "\n") #-1 to show this is category, not a word in it.
            word_count.clear()
            print(self.totals_list[topic][0])
            for i in range(start_index, start_index + self.totals_list[topic][1]):
                for word in words[i]:
                    if (len(word) > 2 and word != "the" and word != "and" and
                        word != "you" and word != "she" and word != "him" and word != "her" and
                        word != "his" and word != "hers" and word != "yours" and word != "they" and
                        word != "their" and word != "them" and word != "yours" and word != "mine"):
                        """
                        #This section is useful for getting default use case of words to determine if adjectives, and to stem words.
                        descriptions = wn.synsets(word)
                        if len(descriptions) > 0 and descriptions[0].pos() == "a" or len(descriptions) == 0:
                            continue
                        word = ps.stem(word)
                        """
                        #see if the word exists, and add 1 to the count. If not, continue
                        if any(word in current_word for current_word in word_count):
                            index = [i for i, lst in enumerate(word_count) if word in lst][0] #get first instance of word in word_count
                            word_count[index][1] = word_count[index][1] + 1
                            continue

                        temp_list = [word, 1]
                        word_count.append(temp_list)
                        
            #move to next topic
            start_index = start_index + self.totals_list[topic][1]

            #write word and counts to file for easier access later
            for word in word_count:
                if (word[1] != 1):
                   word_count_file.write(str(word[0]) + " " + str(word[1]) + "\n")

        word_count_file.close()
        training_data.close()

    """
    Loads the word counts from the saved file.
    """
    def load_word_counts(self, file_name):
        training_data = open(file_name, "r")
        self.words = [word.split() for word in training_data.readlines()]
        self.words = [[word[0], int(word[1])] for word in self.words]
        training_data.close()

    """
    Gets the necessary probabilities for words in a given document type.
    """
    def get_probabilities(self):
        #get the probability of the class and save it as an instance variable
        self.class_probability = [type[1]/self.total for type in self.totals_list]
        start_index = 0
        topic_words = []
        temp_list = []
        word = 0

        #Gets the words by category
        while word < len(self.words):
            #if the list isn't empty and the occurance count is -1, then a new topic has been reached.
            if self.words[word][1] == -1 and len(temp_list) > 0:
                topic_words.append(temp_list.copy())
                temp_list.clear()

            temp_list.append(self.words[word])
            word+=1
        #necessary for last topic to call this one more time
        topic_words.append(temp_list.copy())

        #get total words in each category
        total_words_per_category = [len(category) - 1 for category in topic_words]
        temp_list.clear()
        
        #Total number of words, or total vocabulary
        for topic in topic_words:
            for word in topic:
                if word[1] != -1:
                    temp_list.append(word[0])

        vocabulary = len(set(temp_list))
        self.word_category_probabilities = []
        current_topic_index = 0

        #Gets the probability of a word in the entire vocabulary.
        for topic in topic_words:
            temp_list.clear()
            temp_list.append(topic[0])

            #P(w|c)
            for word in topic[1:]:
                temp_probability = [word[0], (word[1] + 1)/(total_words_per_category[current_topic_index] + vocabulary)]
                temp_list.append(temp_probability)

            self.word_category_probabilities.append(temp_list.copy())
            current_topic_index+=1

    """
    Loads the test documents
    """
    def load_test_data(self):
        test_data = open("forumTest.data", "r")
        self.test_documents = [line for line in test_data.readlines()]
        test_data.close()

    """
    Classifies much faster than nested for loops. Uses multiple parallel lists
    and the in keyword.
    """
    def classify_fast(self, filename):
        total = 0
        totalRight = 0
        #list of lists, used to hold all the words
        doc_type_words = []
        #list of lists, used to hold probabilities
        doc_type_words_probs = []
        times_file = open(filename, "w")
        ps = PorterStemmer()

        #Move large list into the two parallel lists
        for category in self.word_category_probabilities:
            temp_word_list = []
            temp_prob_list = []
            for word_and_prob in category:
                if (word_and_prob[1] != -1):
                    temp_word_list.append(word_and_prob[0])
                    temp_prob_list.append(word_and_prob[1])
            
                
            doc_type_words.append(temp_word_list.copy())
            doc_type_words_probs.append(temp_prob_list.copy())

        startTime = time.time()
        #Loop through every document in the test documents
        for document in self.test_documents:
            document_words = document.split()
            correct_type = document_words[0] #First word is the correct document type
            all_word_probabilities = []
            
            classifications = [1 for i in range(self.total_types)]
            #for each word in document, check if it is in the word_category_probabilities list. If so, get the probability.
            for word in document_words[1:]:
                if (len(word) > 2 and word != "the" and word != "and" and
                        word != "you" and word != "she" and word != "him" and word != "her" and
                        word != "his" and word != "hers" and word != "yours" and word != "they" and
                        word != "their" and word != "them" and word != "yours" and word != "mine"):
                    
                    word_probability_per_category = []

                    """
                    descriptions = wn.synsets(word)
                    if len(descriptions) > 0 and descriptions[0].pos() == "a" or len(descriptions) == 0:
                        continue
                    word = ps.stem(word)
                    """
                    #Check every category for a word. If it exists, get the probability. If not, use -1 placeholder.
                    for category in range(len(doc_type_words)):
                        if word in doc_type_words[category]:
                            index = doc_type_words[category].index(word)
                            word_probability_per_category.append(doc_type_words_probs[category][index])
                        else:
                            word_probability_per_category.append(-1)
                    all_word_probabilities.append(word_probability_per_category.copy())

            #multiple logs together as well as class probability
            for word_probability in all_word_probabilities:
                for category in range(len(word_probability)):
                    if word_probability[category] == -1:
                        continue
                    classifications[category] += log(word_probability[category])


            for doc_type in range(len(classifications)):
                classifications[doc_type] += log(self.class_probability[doc_type])

            total+=1
            if self.totals_list[classifications.index(max(classifications))][0] == correct_type:
                totalRight+=1
                
            print(str(total) + "/" + str(len(self.test_documents)) + ", " + str(round(totalRight/total, 2)))
            endTime = time.time()
            times_file.write(str(round(totalRight/total, 2)) + " " + str(endTime - startTime) + "\n")
            
        times_file.close()


    """
    Plot the data points using matplotlib.
    If an iteration is specific, then use that specific iteration
    """
    def plot_points(self, iteration=-1):
        data = []
        num_sets = 6
        
        #Read the data in from the files
        for i in range(1, num_sets + 1):
            with open("times/times_iter" + str(i) + ".data") as file:
                tmp = [[float(value[0]), float(value[1])] for value in (line.split() for line in file)]
            data.append(tmp.copy())

        #Create a legend
        legend_list = ["Slow speed, poor result",
                       "Removed nested loops",
                       "Removed words used once, fixed classifier, good result",
                       "Used stemmer, removed adjectives, ok result",
                       "No stemmer, removed adjectives and pronouns, ok result",
                       "Stemmer, all words, ok result"]
        #Use a color rainbow
        colors = cm.rainbow(np.linspace(0, 1, num_sets))

        #If no iteration was specified, then plot all iterations
        if iteration == -1:        
            for dataset in range(num_sets):
                y = [point[0] for point in data[dataset]]
                x = [point[1] for point in data[dataset]]
                plt.scatter(x, y, color=colors[dataset], linewidth=1, s=1)
            lgnd = plt.legend(legend_list)
        else:
            y = [point[0] for point in data[iteration]]
            x = [point[1] for point in data[iteration]]
            plt.scatter(x, y, color=colors[iteration], linewidth=1, s=1)
            lgnd = plt.legend([legend_list[iteration]])

        #Set size of legend icons to see colors easier
        for handle in lgnd.legendHandles:
            handle._sizes = [10]
        plt.xlabel("Time (s)")
        plt.ylabel("Classification rate")
        plt.show()
        
"""
classifier = doc_classifier()
classifier.save_word_counts("word_counts/word_counts_stemmer.txt")
classifier.load_word_counts("word_counts/word_counts_stemmer.txt")
classifier.get_probabilities()
classifier.load_test_data()
classifier.classify_fast("times/times_iter7.data")
classifier.plot_points(-1)
"""
