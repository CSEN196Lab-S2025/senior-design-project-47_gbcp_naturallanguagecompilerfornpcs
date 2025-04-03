import sys
import spacy
import nltk
from nltk.corpus import wordnet as wn
#nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")

def get_hypernyms(word):
    synsets = wn.synsets(word)
    hypernyms_list = []
    if not synsets:
        return None
    for i in range(len(synsets)):
        hypernyms = synsets[i].hypernyms()
        hypernyms_list.append([lemma.name() for synset in hypernyms for lemma in synset.lemmas()])
    return hypernyms_list

def get_synonyms(word):
    synsets = wn.synsets(word)
    
    # Initialize an empty list to store the synonyms
    synonyms_list = []
    
    if not synsets:
        return None

    for synset in synsets:
        # Collect synonyms from the lemmas in each synset
        for lemma in synset.lemmas():
            if lemma.name() not in synonyms_list:  # Avoid duplicates
                synonyms_list.append(lemma.name())
    
    return synonyms_list

print(get_synonyms(sys.argv[1]))




