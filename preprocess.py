import os
import sys
from typing import List
import re
from collections import defaultdict


class Tokenizer:
    text: str
    tokens: List[str]

    def __init__(self, text):
        self.text = text
        # self.text = "The current population of U.S.A. is 332,087,410 as of Friday, 01/22/2021, based on Worldometer elaboration of the latest United Nations’ data."
        self.tokens = []

    def is_title(self, word):
        return re.match(r"(Dr|Mr|Mrs|Esq|Hon|Jr|Ms|Msgr|Prof|Rev|Sr|St)\.", word)

    def is_acronym(self, word):
        return re.match(r"[A-Z]\.", word)

    def remove_contractions(self, word):
        word = re.sub(r"\b(are|could|did|do|had|have|might|must|is|would|should|has|does|were)n't\b", r'\1 not', word, flags=re.IGNORECASE)
        word = re.sub(r"\bcan't\b", 'can not', word, flags=re.IGNORECASE)
        word = re.sub(r"\bwon't\b", 'will not', word, flags=re.IGNORECASE)
        word = re.sub(r"\bshan't\b", 'shall not', word, flags=re.IGNORECASE)

        word = re.sub(r"\bI'm\b", 'I am', word, flags=re.IGNORECASE)
        word = re.sub(r"\b(.*)'ve\b", r'\1 have', word, flags=re.IGNORECASE)
        word = re.sub(r"\blet's\b", 'let us', word, flags=re.IGNORECASE)

        word = re.sub(r"(.*)'re\b", r'\1 are', word, flags=re.IGNORECASE)

        word = re.sub(r"\b(.*)'d\b", r'\1 would', word, flags=re.IGNORECASE)

        word = re.sub(r"\b(.*)'ll\b", r'\1 will', word, flags=re.IGNORECASE)

        word = re.sub(r"\b(she|he|there|what|where|who|that)'s\b", r'\1 is', word, flags=re.IGNORECASE) #replace is contractions
        word = re.sub(r"\b([A-Z][a-z]*)'s\b", r"\1 's", word, flags=re.IGNORECASE) #replace any possessives
        return word

    def go(self):
        problemsymbols = ["?", "(", ")", "!", "?", "[", "]", "{", "}", "/", "\\", "|", '"', ',']
        for word in self.text.split(' '):
            multiplewords = re.split(r'([?()!?\[\]{}/\\\|\",])', word)
            word = ""
            for k in multiplewords:
                word = word + " " + k
            if word == "" or word == " " or word == "  " or word == ' ':
                continue
            if word[-1] == ".":
                if self.is_title(word):
                    self.tokens.append(word)
                    continue
                if self.is_acronym(word):
                    self.tokens.append(word)
                    continue
                word = word[0:-1] + " ."
            if word[-1] == "'":
                word = word[0:-1] + " '"
            if (word[-2] + word[-1]) == "'s":
                word = word[:-2]

            word = self.remove_contractions(word)

            #If its now actually two tokens or more, add each individually
            moretokens = word.split(' ')
            for x in moretokens:
                if x != "" and x != " ":
                    self.tokens.append(x)

        return self.tokens


def tokenizeFromFile(f):
    return tokenizeFromString(readFile(f))

def tokenizeFromString(s):
    return tokenizeText(removeSGML(s))

def readFile(f) -> str:
    text = ""
    for line in f:
        text += line
        text = re.sub('\n', ' ', text)
    return text

def removeSGML(k: str) -> str:
    text = re.sub('<.*?>', '', k)
    text = re.sub(' +', ' ', text)
    return text


def tokenizeText(text: str) -> List[str]:
    here_we = Tokenizer(text)
    return here_we.go()


def removeStopwords(k: List[str]) -> List[str]:
    stopwords = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'from', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your']
    i = 0
    while i < len(k):
        if k[i] in stopwords:
            k.pop(i)
        else:
            i += 1
    return k


def main():
    docs = []
    for i in os.listdir(sys.argv[1]):
        text = ""
        with open(sys.argv[1]+"/"+i) as f:
            for line in f:
                text += line
        text = re.sub('\n', ' ', text)
        docs.append(text)
    #docs = [docs[0]]
    for i in range(0, len(docs)):
        docs[i] = removeSGML(docs[i])
    for i in range(0, len(docs)):
        docs[i] = tokenizeText(docs[i])
    for i in range(0, len(docs)):
        docs[i] = removeStopwords(docs[i])

    words = defaultdict(int)
    totalwords = 0
    for doc in docs:
        for word in doc:
            words[word] += 1
            totalwords+=1
    sorted_words = sorted(words.items(), key=lambda x:x[1], reverse=True)
    with open("preprocess.output", "w") as f:
        f.write('Words '+str(totalwords)+"\n")
        f.write('Vocabulary '+str(len(sorted_words))+"\n")
        f.write('Top 50 words\n')
        for i in range(0, 50):
            f.write(sorted_words[i][0]+" "+str(sorted_words[i][1])+"\n")
    #print(sorted_words)

    #print(docs)

if __name__ == "__main__":
    main()
#ajpynnon Alex Pynnonen