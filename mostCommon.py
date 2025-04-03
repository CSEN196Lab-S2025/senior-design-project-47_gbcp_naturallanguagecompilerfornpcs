import sys
import re

import spacy
import nltk
from nltk.corpus import wordnet as wn

nlp = spacy.load("en_core_web_sm")
nltk.download('wordnet')

freq = {}
word_mappings = {}  # New dictionary to track original words that map to each synonym/hypernym

def get_synonyms(word):
    synsets = wn.synsets(word)
    synonyms_list = []
    if not synsets:
        return ["_"]
    for synset in synsets:
        for lemma in synset.lemmas():
            if lemma.name() not in synonyms_list:
                synonyms_list.append(lemma.name())
    return synonyms_list

def get_hypernyms(word):
    synsets = wn.synsets(word)
    if not synsets:
        return ["_"]
    hypernyms = synsets[0].hypernyms()
    return [lemma.name() for synset in hypernyms for lemma in synset.lemmas()]

def increment_freq(word, original_word):
    if word in freq:
        freq[word] += 1
    else:
        freq[word] = 1
    if word in word_mappings:
        word_mappings[word].add(original_word)
    else:
        word_mappings[word] = {original_word}

if len(sys.argv) > 3:
    inputFile = sys.argv[1] 
    outputFile = sys.argv[2]
    selector = sys.argv[3]
else:
    print("proper usage: python3 " + sys.argv[0] + " [file to read] [file to write] [0 or 1 for synonym or hypernym, respectively]")
    exit()

with open(inputFile, 'r') as file:
    content = file.read()
words = re.split(r'[\s,!.();{}[\]?\'":]+', content)
wordSet = set(words)

for word in wordSet:
    if selector == "0":
        hypers = get_synonyms(word)
    else:
        hypers = get_hypernyms(word)
    if len(hypers) > 0:
        increment_freq(hypers[0], word)  # Pass both the synonym/hypernym and original word

with open(outputFile, 'w') as f:
    for key, value in sorted(freq.items(), key=lambda item: item[1]):
        # Convert the set of original words to a sorted, comma-separated string
        original_words = ", ".join(sorted(word_mappings[key]))
        f.write(f"{key}: {value} (from: {original_words})\n")
