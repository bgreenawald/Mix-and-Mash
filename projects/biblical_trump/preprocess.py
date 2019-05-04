import math
import os
from os.path import join
import pickle
import random
import re
import sys

import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.preprocessing import normalize

DATA_DIR = "raw_data"
WRITE_DIR = "processed_data"
MODEL_DIR = "model"

with open(join(DATA_DIR, "bible.txt"), "r") as file:
    bible_text = file.read()

# Regular expression to consolidate verses into single lines
single_line = re.compile("\n(?!\n)")
bible_text = re.sub(pattern=single_line, string=bible_text, repl=" ")

# Read in the trump tweets
tweets = pd.read_csv(join(DATA_DIR, "trumpTweets.csv"))
tweets_text = tweets["text"]

# Append tweets to Bible
bible_and_tweets = bible_text + "\n".join(tweets_text)
with open(join(WRITE_DIR, "bible_and_tweets.txt"), "w+", encoding="utf-8") as file:
    file.write(bible_and_tweets)

# Use regular expression to edit data
remove_non_alphabetic = re.compile("[^a-zA-Z \n]")
remove_multiple_newlines = re.compile("\n[\n]+")
remove_multiple_spaces = re.compile(" [ ]+")
remove_http = re.compile("http[^ ]+")
bible_and_tweets = re.sub(
    pattern=remove_non_alphabetic, string=bible_and_tweets, repl=""
)
bible_and_tweets = re.sub(
    pattern=remove_multiple_newlines, string=bible_and_tweets, repl="\n"
)
bible_and_tweets = re.sub(pattern=remove_http, string=bible_and_tweets, repl=" ")
bible_and_tweets = bible_and_tweets.replace("\n", " !ENDLINE!\n")
bible_and_tweets = re.sub(
    pattern=remove_multiple_spaces, string=bible_and_tweets, repl=" "
)

# Make everything lowercase
bible_and_tweets = bible_and_tweets.lower()

# Trim each line, write result file
sentences = []
for line in bible_and_tweets.split("!endline!\n"):
    sentences.append(line.strip())

text_full = " !endline!\n".join(sentences)

with open(join(WRITE_DIR, "text_processed.txt"), "w+") as file:
    file.write(text_full)

print("Text length: " + str(len(text_full)))

# Create the vocabulary
vocab = []
for line in text_full.split("\n"):
    for word in line.split(" "):
        vocab.append(word)

print("Vocabulary length: " + str(len(vocab)))

# Create a set for the vocab
vocab = set(vocab)
print("Unique vocab: " + str(len(vocab)))

# Create a dict mapping vocab to index
vocab_to_id = {}
id_to_vocab = {}
for index, word in enumerate(vocab):
    vocab_to_id[word] = index
    id_to_vocab[index] = word

# Save the objects
with open(join(MODEL_DIR, "vocab_to_id.pkl"), "wb") as f:
    pickle.dump(vocab_to_id, f, pickle.HIGHEST_PROTOCOL)
    f.close()

with open(join(MODEL_DIR, "id_to_vocab.pkl"), "wb") as f:
    pickle.dump(id_to_vocab, f, pickle.HIGHEST_PROTOCOL)
    f.close()

with open(join(MODEL_DIR, "vocab.pkl"), "wb") as f:
    pickle.dump(vocab, f, pickle.HIGHEST_PROTOCOL)
    f.close()


# Create an empty matrix of zeroes
tf = sp.lil_matrix((len(vocab), len(vocab)), dtype=np.float)

# Fill up the tf matrix
for line in text_full.split("\n"):
    words = line.split(" ")
    for i in range(len(words) - 1):
        id1 = vocab_to_id[words[i]]
        id2 = vocab_to_id[words[i + 1]]
        tf[id1, id2] += 1

# Create the spark matrix
mat = tf.tocoo()

# Normalize the matrix
mat_norm = normalize(mat, norm="l1", axis=1)

# Save the normalized matrix
sp.save_npz(join(MODEL_DIR, "norm_matrix.npz"), mat_norm)
