#!/usr/bin/env python
import time
from itertools import chain

atheism_total = 480
graphics_total = 584
mswindows_total = 572
pc_total = 590
mac_total = 578
xwindows_total = 593
forsale_total = 585
autos_total = 594
motorcycles_total = 598
baseball_total = 597
hockey_total = 600
cryptology_total = 595
electronics_total = 591
medicine_total = 594
space_total = 593
christianity_total = 598
guns_total = 545
mideastpolitics_total = 564
politics_total = 465
religion_total = 377
total = 11293

def get_word_counts():
    training_data = open("forumTraining.data", "r")
    documents = [line for line in training_data.readlines()]
    words = [document.split() for document in documents]

    word_count = []
    for i in range(0, 480):
        print(i)
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

    print(len(word_count))
    time.sleep(2)

    """
    for word in word_count:
        if (word[1] > 1):
            print(word[0] + ": " + str(word[1]))
    """
    training_data.close()

get_word_counts()
