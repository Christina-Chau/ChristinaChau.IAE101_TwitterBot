# mytwitterbot.py
# IAE 101, Fall 2019
# Project 02 - Building a Twitterbot
# Name: Christina Chau
# netid: chrchau
# Student ID: 112720104

import sys
import simple_twit
import nltk
import pronouncing
import random

text = random.randint(0, 2)
my_corpus = nltk.corpus.gutenberg.words('shakespeare-hamlet.txt')
if text ==0:
    my_corpus = nltk.corpus.gutenberg.words('shakespeare-hamlet.txt')
    name = "Hamlet"
elif text ==1:
    name = "Macbeth"
    my_corpus = nltk.corpus.gutenberg.words('shakespeare-macbeth.txt')
else:
    my_corpus = nltk.corpus.gutenberg.words('shakespeare-caesar.txt')
    name = "Caesar"
bigrams = nltk.bigrams(my_corpus)
cfd = nltk.ConditionalFreqDist(bigrams)


def random_word_generator(source=None, num=1):
    result = []
    while source == None or not source[0].isalpha():
        source = random.choice(my_corpus)
    word = source
    result.append(word)
    while len(result) < num:
        if word in cfd:
            init_list = list(cfd[word].keys())
            choice_list = [x for x in init_list if x[0].isalpha()]
            if len(choice_list) > 0:
                newword = random.choice(choice_list)
                result.append(newword)
                word = newword
            else:
                word = None
                newword = None
        else:
            while newword == None or not newword[0].isalpha():
                newword = random.choice(my_corpus)
            result.append(newword)
            word = newword
    return result


def count_syllables(word):
    phones = pronouncing.phones_for_word(word)
    count_list = [pronouncing.syllable_count(x) for x in phones]
    if len(count_list) > 0:
        result = max(count_list)
    else:
        result = 0
    return result


def generate_line(line_num):
    count = 0  # syllable count
    prev = None
    line = "";
    if line_num == 0:  # if first line
        while count <= 5:
            word = random_word_generator(prev, 2)[1]
            count += count_syllables(word)
            if count < 5:
                line += word + " "
            elif count > 5:
                count -= count_syllables(word)
            else:
                line += word + " "
                break
    elif line_num == 1:  # if second line
        while count <= 7:
            word = random_word_generator(prev, 2)[1]
            count += count_syllables(word)
            if count < 7:
                line += word + " "
            elif count > 7:
                count -= count_syllables(word)
            else:
                line += word + " "
                break
    else:  # if last line
        while count <= 5:
            word = random_word_generator(prev, 2)[1]
            count += count_syllables(word)
            if count < 5:
                line += word + " "
            elif count > 5:
                count -= count_syllables(word)
            else:
                line += word + " "
                break

    return line


def generate_poem():
    poem = []
    for x in range(0, 3):
        poem.append(generate_line(x))
    complete = "\n".join(poem)
    return complete


def main():
    # This call to simple_twit.create_api will create the api object that
    # Tweepy needs in order to make authenticated requests to Twitter's API.
    # Do not remove or change this function call.
    # Pass the variable "api" holding this Tweepy API object as the first
    # argument to simple_twit functions.
    api = simple_twit.create_api()
    # YOUR CODE BEGINS HERE
    api.update_status("Today's haiku is from " + name + "\n" + generate_poem())
    simple_twit.version()


if __name__ == "__main__":
    main()