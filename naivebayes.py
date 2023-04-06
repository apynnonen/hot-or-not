import sys
import os
from typing import List
import time
import preprocess
import math

def testNaiveBayes(bayesValues, file: str):
    probabilities, base_probabilities, vocab_size, total_word_counts = bayesValues
    pos = base_probabilities["pos"]
    neg = base_probabilities["neg"]
    modified_probs = {"pos": pos, "neg": neg}

    for word in preprocess.tokenizeFromString(file):
        for type in probabilities:
            if word in probabilities[type]:
                modified_probs[type] += probabilities[type][word]
            else:
                modified_probs[type] += math.log2(1/(vocab_size + total_word_counts[type]))
    if modified_probs["neg"] > modified_probs["pos"]:
        return "neg", modified_probs["neg"], modified_probs["pos"]
    else:
        return "pos", modified_probs["pos"], modified_probs["neg"]


def trainNaiveBayes(folder):
    filepaths = sorted(os.listdir(folder))
    files = {}
    for file in filepaths:
        with open(folder + "/" + file) as f:
            files[file] = preprocess.tokenizeFromFile(f)
    n = len(filepaths)
    file_count = {}
    file_count["neg"] = 0
    file_count["pos"] = 0
    word_count = {}
    word_count["neg"] = {}
    word_count["pos"] = {}
    probabilities = {}
    probabilities["neg"] = {}
    probabilities["pos"] = {}
    base_probabilities = {}
    vocab = set()
    for file in filepaths:
        type = file[0:3]
        file_count[type] += 1
        for word in files[file]:
            vocab.add(word)
            if word in word_count[type]:
                word_count[type][word] += 1
            else:
                word_count[type][word] = 1
    total_word_counts = {}
    total_word_counts["neg"] = sum(word_count["neg"].values())
    total_word_counts["pos"] = sum(word_count["pos"].values())
    for type in word_count:
        base_probabilities[type] = file_count[type] / n
        for word, count in word_count[type].items():
            probabilities[type][word] = math.log2((count+1) / (len(vocab) + total_word_counts[type]))
    return [probabilities, base_probabilities, len(vocab), total_word_counts]

def main():
    start_time = time.time()
    folder = sys.argv[1].strip()
    files = sorted(os.listdir(folder))
    output = ""
    correct = 0
    # Read in all the files to begin with so this program isn't slow as heck
    for file in files:
        with open(folder + "/" + file) as f:
            words = preprocess.tokenizeFromFile(f)
        global_files[file] = words
    for i in range(0, len(files)):
        filepaths = files[0:i] + files[(i+1):]
        probabilities, base_probabilities, vocab_size, total_word_counts = trainNaiveBayes(filepaths)
        decision = testNaiveBayes(probabilities, base_probabilities, vocab_size, total_word_counts, files[i])
        output += files[i] + " " + decision + "\n"
        if decision[0] == files[i][0]:
            correct+=1
    with open("naivebayes.output."+folder, "w") as f:
        f.write(output)
    print(f"We got {correct} files correct out of {len(files)} making for {round(correct/len(files), 2)} accuracy.")
    print(f"Took {round(time.time() - start_time, 1)} seconds")


if __name__ == "__main__":
    main()
# Alex Pynnonen (ajpynnon@umich.edu)