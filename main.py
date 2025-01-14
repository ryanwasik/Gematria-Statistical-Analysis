"""Gematria Statistics - written by Ryan"""
# computing
import string
from collections import Counter

# plotting
import matplotlib.pyplot as plt
import numpy as np

# general
import time

# Bible source: Project Gutenberg - KJV (https://www.gutenberg.org/cache/epub/30/pg30.txt)
# Preamble and Postscript edited with Vim Scripts


def read_text(f_loc="bible_kjv.txt"):
    """defaults as KJV Bible, edit parameter to test other sources"""
    with open(f_loc, "r") as bible_loc:
        bible_data = bible_loc.read()

    def clean_bible_list():  # isolating all unique words from text file
        bible_data.translate(str.maketrans('', '', string.punctuation))
        bible_data_unique_list = tuple(set([word.lower() for word in bible_data.split() if word.isalpha()]))
        return bible_data_unique_list

    return clean_bible_list()


def gematrify(_word):
    """return dict of gematria values of a word"""
    letter_nums = list(string.ascii_letters[:26])  # conversion of individual letters to numbers
    # Types of gematria equations:

    # sum of all letters
    english_ordinal_word = sum([letter_nums.index(word_letter) + 1 for word_letter in _word])

    # sum of all letters with a letters number % 9 (e.g. j = 1)
    full_reduction_word = sum([9 if x == 0 else x for x in [
        (letter_nums.index(word_letter) + 1) % 9 for word_letter in _word]])

    # sum of all letters with number index reversed (e.g. a = 27)
    rev_ordinal_word = sum([letter_nums[::-1].index(word_letter) + 2 for word_letter in _word])

    # sum of all letters with number % 9 and index reversed (e.g. r = 9)
    rev_reduction_word = sum([9 if x == 0 else x for x in [
        (letter_nums[::-1].index(word_letter) + 2) % 9 for word_letter in _word]])

    word_gem_dict = {"word": _word,
                     "eow": english_ordinal_word,
                     "frw": full_reduction_word,
                     "row": rev_ordinal_word,
                     "rrw": rev_reduction_word}

    return word_gem_dict


def occurrence_counter():
    """count the number of occurrences of gematria values"""
    gematrify_list = [gematrify(word) for word in read_text()]
    gem_types = list(gematrify_list[0].keys())[1:]
    occurrence_dict = {gem_type: Counter([word[gem_type] for word in gematrify_list]) for gem_type in gem_types}
    return occurrence_dict


def percent_chance():
    """evaluate the % chance an average word has the same value as another"""
    total_unique_words = len(read_text())
    print("[///] Percent chance any two words have the same gematria value:")
    for gem_type, gem_data in occurrence_counter().items():
        print(gem_type + ": " + str(round((len(gem_data.items()) / total_unique_words) * 100, 4)) + "%")


def plot_occurrences():
    plt.title('Gematria Frequency Statistics')
    plt.ylabel('Frequency')
    plt.xlabel('Gematria Value')
    # plt.text(0, 0, str(avg_percent_chance_counter(_list)) + "%")

    for gem_type, gem_data in occurrence_counter().items():
        sorted_data = (sorted(list(gem_data.items()), key=lambda x: x[0]))
        y = list(zip(*sorted_data))
        plt.plot(y[0], y[1], label=gem_type)
    plt.legend()
    print("[///] Completed in %s seconds" % (time.time() - start_time))
    plt.show()


if __name__ == "__main__":
    start_time = time.time()
    percent_chance()
    plot_occurrences()

