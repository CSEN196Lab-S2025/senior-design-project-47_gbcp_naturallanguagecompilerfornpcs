import sys
import re
import string
import spacy
import inflect
import nltk
from nltk.corpus import wordnet as wn
from typeguard import typeguard_ignore

nlp = spacy.load("en_core_web_sm")

inflect_eng = inflect.engine()



def is_plural(word):
    doc = nlp(word)
    for token in doc:
        # Compare the word with its lemma (singular form for nouns)
        return token.lemma_ != token.text

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
        return ["_"]

    for synset in synsets:
        # Collect synonyms from the lemmas in each synset
        for lemma in synset.lemmas():
            if lemma.name() not in synonyms_list:  # Avoid duplicates
                synonyms_list.append(lemma.name())
    
    return synonyms_list

#test comment
dict1 = {
    "water": "ooa",
    "heat": "sow",
}

dict2 = {
    "no": "wi",
    "region": "fayon",
    "cavern": "rodowne",
    "darkness": "ko",
}

dict3 = {
    "depth": "kora",
    "ground": "tatak",
    "know": "banan",
}

dict4 = {
    "air": "ooawi",
    "shore": "iros",
}

dict5 = {
    "light": "kowi",
}

dicts = [dict1,dict2,dict3,dict4,dict5]
def translateWord(word, level):
    for i in range(0, level, 1):
        if (dicts[i].get(word, -1) != -1): #word found
            translate_flag[i] = True
            return dicts[i].get(word, -1)
    hypernym = get_synonyms(word)
    for i in range(0, level, 1):
        for j in range(len(hypernym)):
            if (dicts[i].get(hypernym[j], -1) != -1): #word found
                translate_flag[i] = True
                return dicts[i].get(hypernym[j], -1)
    translate_flag[i] = False
    return word
    
def startsWithWhite(file_path):
    with open(file_path, 'r') as file:
        start = file.read(1)
        #set of characters that includes whitespace and punctuation
        whitespace_and_punctuation = string.whitespace + string.punctuation
        #check if the first char is in that set
        return any(char in whitespace_and_punctuation for char in start)

def plural_rule():
    cur = 0
    while cur < len(words):
        if (plural_flag[cur] & translate_flag[cur]):
            if words[cur].startswith("a"):
                words[cur] = "y" + words[cur]
            else:
                words[cur] = "a" + words[cur]
        cur+=1
def wi_rule():
    cur = 0
    while cur < len(words):
        if words[cur] == "wi":
            if cur != len(words)-1:
                words.pop(cur)
                whitespaces.pop(cur)
                plural_flag.pop(cur)
                if words[cur].endswith("wi"):
                    words[cur] = words[cur][:-2]
                else:
                    words[cur] = words[cur] + "wi"
        cur+=1
#read command line input
if len(sys.argv) > 1:
    inputFile = sys.argv[1]
    level = int(sys.argv[2])
else:
    print("Need input file name as argument")
    exit()

#add _t to end of outputFile name before .txt
main_part, extension = inputFile.rsplit('.', 1)
outputFile = main_part + '_t.' + extension

#read input file
with open(inputFile, 'r') as file:
    content = file.read()
words = re.split(r'[\s,!.?\'":]+', content)
translate_flag = [False] * len(words)
plural_flag = [False] * len(words)
cur = 0
while cur < len(words):
    if is_plural(words[cur]):
        plural_flag[cur] = True
    else:
        plural_flag[cur] = False
    cur = cur+1
punctuation = re.escape(string.punctuation) 
pattern = rf'[\s{punctuation}]+'
whitespaces = re.findall(pattern, content)
whitespaces.append("")

#translate all the words
for i in range(len(words)):
    words[i] = translateWord(words[i], level)

#specific rules per level:
if level>=1:
    print("Translating level 1!")

if level>=2:
    print("Translating level 2!")
    wi_rule()

if level>=3:
    print("Translating level 3!")
    plural_rule()

if level>=4:
    print("Translating level 4!")

if level>=5:
    print("Translating level 5!")




#write to the file with correct whitespace placement
with open(outputFile, 'w') as file:
    whiteCur = 0
    print(words[0])
    for i in range(len(words)):
        file.write(words[i])
        if whiteCur < len(whitespaces):
            file.write(whitespaces[whiteCur])
            whiteCur += 1
