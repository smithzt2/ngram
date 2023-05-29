#!/usr/bin/env python3
########################################################################################################################
########################################################################################################################
#
#                                                   ngram.py
#                                                 Zachary Smith
#                                                 Spring 2021
#
########################################################################################################################
########################################################################################################################
#
#                                               use: "python ngram.py N M FILE-1...FILE-X"
#                                               note: file number is arbitrary and can be any amount
#                                               N is the n in nGram, M is the number of sentences to generate
#
########################################################################################################################
########################################################################################################################
#
#                   ngram.py takes in an arbitrary number of text files and generates sentences.
#                   This is accomplished by generating an ngram model from the text contained in the input files.
#                   The model is then used in the generation of new sentences.
#
#                   For Testing purposes,
#                       The Adventures of Sherlock Holmes, by Arthur Conan Doyle
#                       The Great Gatsby, by F. Scott Fitzgerald
#                       The Picture of Dorian Gray, by Oscar Wilde
#                       Alice's Adventures in Wonderland, by Lewis Carroll
#                   were used.
#
########################################################################################################################
########################################################################################################################

from sys import argv
import re
import random
import sys


def main():
    # General Setup from user input
    n = argv[1]
    m = argv[2]
    preFiles = argv[3:len(argv)]

    # Generate end/start tag
    eT = endTag(int(n))

    # Pre-process txt files
    for f in preFiles:
        trainData = ""
        # Open file and add initial start tag
        file = "<START>" + open(f, "r", encoding="utf8").read()

        # remove quotation marks, commas, parenthesis and other literary characters
        file = re.sub(r'["“”,();\'’:_—-]', "", file)
        # substitute end tags for punctuation
        file = re.sub(r"[.!?]", eT, file)

        # Add cleaned input to master data
        trainData += file.strip()



    # Train the model
    model = choochoo(trainData, n)

    # Generate Sentences
    m = int(m)
    c = 1
    while m > 0:
        print("\nSentence ", c, ":")
        sentenceGen(model, n)
        m -= 1
        c += 1


# Generates Sentences
# Each word is picked based on the previous n-1 words
# Determined by a random number between 0 and the number of occurrences of the n-1 previous words
def sentenceGen(model, n):
    n = int(n)
    used = 0
    i = 0
    x = 0
    word = ""
    size = len(model)
    sentence = startTag(n)
    space = " "

    while word != '<END>':
        candidates = ""
        used = 0
        j = 0
        sentence = sentence.strip()

        # Get n-1 gram as outer dict key, history
        slicer = i + n - 1
        words = sentence.split()
        history = words[i:slicer]


        # Sum total times history occurs, as totalOccurences
        hist = space.join(history)
        try:
            tgt = model[hist]
        except KeyError:
            print("KEY ERROR: LINE 101:", sentence)
            print("Slicer: ", slicer, "I: ", i, "History: ", history, "Hist: ", hist)
            i += 1
            break
        values = tgt.values()
        totalOccurences = sum(values)

        # get a random number between 0-totalOccurences
        r = random.randint(1, totalOccurences)


        # Get word that occurs
        while used < r:
            #print("Used: ", used)
            #print("R: ", r)
            try:
                candidates = model[hist]
            except KeyError:
                print("KEY ERROR: LINE 118:", sentence)
                print("Slicer: ", slicer, "I: ", i, history)
                i += 1
                break
            candidates = list(candidates.keys())
            word = candidates[j]
            j += 1
            used += model[hist][word]

        i += 1
        if word != "<END>":
            sentence += " "
            sentence += word
        # print("WORD: ", word)

    sentence = sentence.split()
    while sentence.__contains__("<START>"):
        sentence.remove("<START>")
    sentence = space.join(sentence)
    print(sentence)


# Generates the end tag based on ngram size, n-1 <START> appended after <END>
def endTag(n):
    e = " <END>"
    while n > 1:
        e += " <START>"
        n -= 1
    return e


# Generates the Start tag based on ngram size
def startTag(n):
    n = int(n)
    s = ""
    while n > 1:
        s += "<START> "
        n -= 1
    return s


# Generates a Dict where
# Key 1 is a n-1 gram, key2 is the nth word and Occurrence is how often it was the trailing word for that n-1 gram
# [key1 [Key2 Occurrence]]
def choochoo(trainData, n):
    n = int(n)
    data = {}
    words = trainData.split()
    size = len(words)
    i = 0

    # Generate data, a nested dict structure discussed above
    while i < size - n:
        key1 = ""
        slicer = i + n - 1

        history = words[i:slicer]
        for f in history:
            key1 = key1 + " " + f

        followWord = words[slicer]
        key1 = key1.strip()
        followWord = followWord.strip()
        key2 = {followWord: int(1)}

        #################################################
        # Populate Dictionary

        if key1 in data:

            if followWord in data[key1]:
                data[key1][followWord] += 1

            else:
                data[key1][followWord] = 1

        else:
            data[key1] = {}
            data[key1][followWord] = 1

        ##################################################

        i += 1

    return data


if __name__ == "__main__":
    main()






