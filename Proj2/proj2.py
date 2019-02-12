#!/usr/bin/env python
import time
from itertools import chain
from operator import itemgetter

totals_list = [["atheism", 480],
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
total = 11293

def save_word_counts():
    training_data = open("forumTraining.data", "r")
    documents = [line for line in training_data.readlines()]
    words = [document.split() for document in documents]

    word_count = []
    word_count_file = open("word_counts.txt", "w")
    start_index = 0

    for topic in range(0, len(totals_list)):
        word_count_file.write(totals_list[topic][0] + "\n")
        word_count.clear()
        print(totals_list[topic][0])
        for i in range(start_index, start_index + totals_list[topic][1]):
            for word in words[i]:
                if word is not "to" and word is not "it" and word is not "of":
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

        start_index = start_index + totals_list[topic][1]
       
        for word in word_count:
            word_count_file.write(str(word[0]) + " " + str(word[1]) + "\n")
       
        

    print(len(word_count))
    time.sleep(2)


    word_count_file.close()
    training_data.close()

def load_word_counts():
    training_data = open("word_counts.txt", "r")
    words = [word.split() for word in training_data.readlines()]
    training_data.close()

#save_word_counts()
load_word_counts()
