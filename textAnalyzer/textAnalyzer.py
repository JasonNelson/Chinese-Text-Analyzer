#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
from stanfordcorenlp import StanfordCoreNLP

try:
    from tkinter import *
    import tkinter as tk
    from tkinter import filedialog
except:
    from Tkinter import *
    import Tkinter as tk
    from Tkinter import filedialog

def main():
    root = tk.Tk()
    root.geometry("700x700")
    root.title('Chinese Text Analysis')
    T = Text(root, height=4, width=100)
    T.pack(side=LEFT, fill=Y)

    # Establish connection to Stanford parser
    nlp = StanfordCoreNLP('http://localhost', port=9001, lang='zh')

    # set up dictionary for word level lookups and level counts
    word_level_dict = build_word_level_dict()
    word_levels = [0,0,0,0,0,0,0]
    non_HSK_words = []

    # set up dictionary for character level lookups and level counts
    character_level_dict = build_character_level_dict()
    character_levels = [0,0,0,0,0,0,0]
    non_HSK_characters = []

    # get user input
    # sample = get_input()
    sample = get_user_file(root)

    # tokenize Chinese input
    tokens = tokenize_input(sample, nlp)

    # get sentence lengths
    sentence_lengths = get_sentence_info(tokens)

    # remove punctuation from tokens
    tokens = remove_punctuation(tokens)

    # Group and count tokens based on their HSK level
    get_HSK_level_word_counts(tokens, word_level_dict, word_levels, non_HSK_words)
    total_tokens = len(tokens)

    # Get frequencies of words by HSK level
    word_frequencies = []
    get_HSK_level_word_frequencies(total_tokens, word_levels, word_frequencies)

    # Get minimum HSK level needed to read 90% of the words
    min_level_words = get_min_HSK_level_words(word_frequencies)

    # Group and count characters based on their HSK level
    sample = isolate_characters(sample)
    get_HSK_level_character_counts(sample, character_level_dict, character_levels, non_HSK_characters)

    # Get frequencies of characters by HSK level
    character_frequencies = []
    total_characters = len(sample)
    get_HSK_level_character_frequencies(total_characters, character_levels, character_frequencies)

    # Get minimum HSK level needed to read 90% of the characters
    min_level_characters = get_min_HSK_level_characters(character_frequencies)

    # Display results
    display_results(sentence_lengths, total_tokens, word_levels, non_HSK_words, word_frequencies, min_level_words, total_characters, character_levels, character_frequencies, min_level_characters, non_HSK_characters, T)

    root.mainloop()

def build_word_level_dict():
    with open("levels_data/HSK_1-6_word_data.txt") as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            word_level_dict = {rows[1]:rows[2] for rows in reader}
    file.close()
    return word_level_dict

def build_character_level_dict():
    with open("levels_data/HSK_1-6_character_data.txt") as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            character_level_dict = {rows[0]:rows[1] for rows in reader}
    file.close()
    return character_level_dict

def get_input():
    sample = input ('请输入测试语句: ')
    return sample

def get_user_file(root):
    # Close file browser after file is chosen
    root.update()
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd() + '/sample_data/', title="Select file", filetypes=[("Text Files", "*.txt")])
    with open(root.filename, "r") as f:
        sample = f.read()
        return sample

def tokenize_input(sample, nlp):
    tokens = nlp.word_tokenize(sample)
    # close server connection
    nlp.close()
    return tokens

def get_sentence_info(tokens):
    count = 0
    punct = ['。', '？', '」', '！']
    sentence_lengths = []
    # remove non-terminal punctuation
    exclude = '，：；——（）【】；‘“”/「《》@、#¥%&*-=+～·\n\t\r'
    tokens = [x for x in tokens if x not in exclude]
    for token in tokens:
        if token not in punct:
            count += 1
        else:
            sentence_lengths.append(count)
            count = 0
    return sentence_lengths

# To-do: remove digits 0-9, while preserving Chinese numbers
def remove_punctuation(tokens):
    exclude = '，：；。——（）【】；‘“”/？「」《》！@、#¥%&*-=+～·'
    return [x for x in tokens if x not in exclude]

def isolate_characters(sample):
    exclude = ' ，：；。——（）【】；‘“”/？「」《》！@、#¥%&*-=+～·\n\t\r'
    return [x for x in sample if x not in exclude]

def get_HSK_level_word_counts(tokens, word_level_dict, word_levels, non_HSK_words):
    for token in tokens:
        if token in word_level_dict:
            word_levels[int(word_level_dict[token]) - 1] += 1
        else:
            word_levels[6] += 1
            non_HSK_words.append(token)

def get_HSK_level_word_frequencies(total_tokens, word_levels, word_frequencies):
    for level in word_levels:
        word_frequencies.append(level/total_tokens)

def get_min_HSK_level_words(word_frequencies):
    sum = 0
    for i in range(0,5):
        sum += word_frequencies[i]
        if sum >= 0.9:
            return i+1
    return 6

def get_HSK_level_character_counts(sample, character_level_dict, character_levels, non_HSK_characters):
    for character in sample:
        if character in character_level_dict:
            character_levels[int(character_level_dict[character]) - 1] += 1
        else:
            character_levels[6] += 1
            non_HSK_characters.append(character)

def get_HSK_level_character_frequencies(total_characters, character_levels, character_frequencies):
    for level in character_levels:
        character_frequencies.append(level/total_characters)

def get_min_HSK_level_characters(character_frequencies):
    sum = 0
    for i in range(0,5):
        sum += character_frequencies[i]
        if sum >= 0.9:
            return i+1
    return 6

def display_results(sentence_lengths, total_tokens, word_levels, non_HSK_words, word_frequencies, min_level_words, total_characters, character_levels, character_frequencies, min_level_characters, non_HSK_characters, T):

    T.insert(END, '\nTotal number of words in text:        {}'.format(total_tokens))
    T.insert(END, '\nTotal number of sentences in text:    {}'.format(len(sentence_lengths)))
    T.insert(END, '\nAverage number of words per sentence: {}'.format(total_tokens // len(sentence_lengths)))
    T.insert(END, '\nMinimum level to read 90% of words:      HSK {}'.format(min_level_words))
    T.insert(END, '\nMinimum level to read 90% of characters: HSK {}'.format(min_level_characters))

    T.insert(END, '\n\nPercentage of sentences with 0-8 words:   {:.1%}'.format(sum(i < 8 for i in sentence_lengths) / len(sentence_lengths)))
    T.insert(END, '\nPercentage of sentences with 9-11 words:  {:.1%}'.format(sum(8 < i < 12 for i in sentence_lengths) / len(sentence_lengths)))
    T.insert(END, '\nPercentage of sentences with 12-14 words: {:.1%}'.format(sum(11 < i < 15 for i in sentence_lengths) / len(sentence_lengths)))
    T.insert(END, '\nPercentage of sentences with 15-16 words: {:.1%}'.format(sum(14 < i < 17 for i in sentence_lengths) / len(sentence_lengths)))
    T.insert(END, '\nPercentage of sentences with 17-20 words: {:.1%}'.format(sum(16 < i < 21 for i in sentence_lengths) / len(sentence_lengths)))
    T.insert(END, '\nPercentage of sentences with 21-24 words: {:.1%}'.format(sum(20 < i < 25 for i in sentence_lengths) / len(sentence_lengths)))
    T.insert(END, '\nPercentage of sentences with 25-28 words: {:.1%}'.format(sum(24 < i < 29 for i in sentence_lengths) / len(sentence_lengths)))
    T.insert(END, '\nPercentage of sentences with 29+ words:   {:.1%}'.format(sum(i > 28 for i in sentence_lengths) / len(sentence_lengths)))

    T.insert(END, '\n\nNumber of HSK 6 words: {} Frequency: {:.1%}'.format(word_levels[5], word_frequencies[5]))
    T.insert(END, '\nNumber of HSK 5 words: {} Frequency: {:.1%}'.format(word_levels[4], word_frequencies[4]))
    T.insert(END, '\nNumber of HSK 4 words: {} Frequency: {:.1%}'.format(word_levels[3], word_frequencies[3]))
    T.insert(END, '\nNumber of HSK 3 words: {} Frequency: {:.1%}'.format(word_levels[2], word_frequencies[2]))
    T.insert(END, '\nNumber of HSK 2 words: {} Frequency: {:.1%}'.format(word_levels[1], word_frequencies[1]))
    T.insert(END, '\nNumber of HSK 1 words: {} Frequency: {:.1%}'.format(word_levels[0], word_frequencies[0]))
    T.insert(END, '\nNumber of words not found in HSK: {} Frequency: {:.1%}'.format(word_levels[6], word_frequencies[6]))
    T.insert(END, '\n\nNon HSK words: {}'.format(non_HSK_words))

    T.insert(END, '\n\nTotal number of characters in text:       {}'.format(total_characters))

    T.insert(END, '\n\nNumber of HSK 6 characters: {} Frequency: {:.1%}'.format(character_levels[5], character_frequencies[5]))
    T.insert(END, '\nNumber of HSK 5 characters: {} Frequency: {:.1%}'.format(character_levels[4], character_frequencies[4]))
    T.insert(END, '\nNumber of HSK 4 characters: {} Frequency: {:.1%}'.format(character_levels[3], character_frequencies[3]))
    T.insert(END, '\nNumber of HSK 3 characters: {} Frequency: {:.1%}'.format(character_levels[2], character_frequencies[2]))
    T.insert(END, '\nNumber of HSK 2 characters: {} Frequency: {:.1%}'.format(character_levels[1], character_frequencies[1]))
    T.insert(END, '\nNumber of HSK 1 characters: {} Frequency: {:.1%}'.format(character_levels[0], character_frequencies[0]))
    T.insert(END, '\nNumber of characters not found in HSK: {} Frequency: {:.1%}'.format(character_levels[6], character_frequencies[6]))

    T.insert(END, '\n\nNon HSK characters: {}'.format(non_HSK_characters))

if __name__ == '__main__':
    main()
