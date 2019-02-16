#!/usr/bin/env python
import time
from itertools import chain
from operator import itemgetter
import time
from math import log


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

        word_count = []
        word_count_file = open(file_name, "w")
        start_index = 0

        for topic in range(0, len(self.totals_list)):
            word_count_file.write(self.totals_list[topic][0] + " -1" + "\n")
            word_count.clear()
            print(self.totals_list[topic][0])
            for i in range(start_index, start_index + self.totals_list[topic][1]):
                for word in words[i]:
                    if len(word) > 2 and word != "the" and word != "and":
                        if len(word_count) == 0:
                            temp_list = [word, 1]
                            word_count.append(temp_list)
                            continue
                        else:
                            if any(word in current_word for current_word in word_count):
                                index = [i for i, lst in enumerate(word_count) if word in lst][0] 
                                word_count[index][1] = word_count[index][1] + 1
                                continue

                            temp_list = [word, 1]
                            word_count.append(temp_list)

            start_index = start_index + self.totals_list[topic][1]
           
            for word in word_count:
                word_count_file.write(str(word[0]) + " " + str(word[1]) + "\n")

        print(len(word_count))
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
    def classify_words(self):
        self.class_probability = [type[1]/self.total for type in self.totals_list]
        start_index = 0
        topic_words = []
        temp_list = []
        word = 0

        #Gets the words by category 
        while word < len(self.words):
            if self.words[word][1] == -1 and len(temp_list) > 0:
                topic_words.append(temp_list.copy())
                temp_list.clear()
                
            temp_list.append(self.words[word])
            word+=1
        topic_words.append(temp_list.copy())
        
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
            
            for word in topic[1:]:
                temp_probability = [word[0], (word[1])/(total_words_per_category[current_topic_index] + vocabulary)]
                #print(temp_probability)
                temp_list.append(temp_probability)

            self.word_category_probabilities.append(temp_list.copy())
            current_topic_index+=1

        #print(len(self.word_category_probabilities))            #[
        #print(len(self.word_category_probabilities[0]))          #[category
        #print(len(self.word_category_probabilities[0][0]))        #[word/prob
        #print(probability)

    """
    Loads the test documents
    """
    def load_test_data(self):
        test_data = open("forumTest.data", "r")
        self.test_documents = [line for line in test_data.readlines()]
        test_data.close()

    """
    Performs the classifications
    """
    def classify(self):
        total = 0
        totalRight = 0
        start_time = time.time()
        times = []
        times_file = open("times.data", "w")
        #loops
        for document in self.test_documents:
            document_words = document.split()
            correct_type = document_words[0]
            all_word_probabilities = []
            classifications = [1 for i in range(self.total_types)]

            #for each word in document, check if it is in the word_category_probabilities list. If so, get the probability.
            for word in document_words:
                word_probability_per_category = []
                for category in self.word_category_probabilities:
                    found = False
                    for probability in category:
                        if probability[1] == -1:
                            continue
                        if probability[0] == word:
                            word_probability_per_category.append(probability[1])
                            found = True
                            break

                    if not found:
                        word_probability_per_category.append(-1)
                all_word_probabilities.append(word_probability_per_category.copy())

            #multiple logs together as well as class probability
            for word_probability in all_word_probabilities:
                for category in range(len(word_probability)):
                    if word_probability[category] == -1:
                        continue
                    classifications[category] *= log(word_probability[category])

            for doc_type in range(len(classifications)):
                classifications[doc_type] *= self.class_probability[doc_type]

            #print(classifications)
            #print(self.totals_list[classifications.index(max(classifications))][0] + ", " + correct_type)
            total+=1
            if self.totals_list[classifications.index(max(classifications))][0] == correct_type:
                totalRight+=1

            end_time = time.time()
            print(str(total) + "/" + str(len(self.test_documents)) + ", " + str(round(totalRight/total, 2)))       
            times_file.write(str(round(totalRight/total, 2)) + " " + str(end_time - start_time) + "\n")
            
        times_file.close()
        
            

classifier = doc_classifier()
#classifier.save_word_counts("word_counts_noarticles.txt")
classifier.load_word_counts("word_counts_noarticles.txt")
classifier.classify_words()
classifier.load_test_data()
classifier.classify()
