import math
import os
import pickle
import random
import re

import numpy as np
import scipy.sparse as sp


# Define global variables
project_to_path = {
    "biblical_trump": "./projects/biblical_trump/model"
}

vocab_to_id = None
id_to_vocab = None
vocab = None
mat_norm = None


def load_resources(project):
    """Given the project name, load global resources."""
    PROJECT_DIR = project_to_path[project]

    # Read back in the matrix and dictionary objects
    global mat_norm
    mat_norm = sp.load_npz(os.path.join(PROJECT_DIR, "norm_matrix.npz"))

    with open(os.path.join(PROJECT_DIR, "vocab_to_id.pkl"), "rb") as f:
        global vocab_to_id
        vocab_to_id = pickle.load(f)
        f.close()
    with open(os.path.join(PROJECT_DIR, "id_to_vocab.pkl"), "rb") as f:
        global id_to_vocab
        id_to_vocab = pickle.load(f)
        f.close()
    with open(os.path.join(PROJECT_DIR, "vocab.pkl"), "rb") as f:
        global vocab
        vocab = pickle.load(f)
        f.close()


def normal_generate(start_word):
    if start_word not in vocab:
        raise KeyError("{} not found in vocabulary.".format(start_word))

    sentence = [start_word]
    while start_word != "!endline!":
        row_ind = vocab_to_id[start_word]
        prob_dist = np.array(mat_norm.getrow(row_ind).todense())[0]
        try:
            next_ind = np.random.choice(range(len(vocab)), p=prob_dist)
        except ValueError:
            pass
            # TODO: Figure out what to do here.
        start_word = id_to_vocab[next_ind]
        sentence.append(start_word)
    return " ".join(sentence[:-1]).capitalize()


def memory_generate(start_words, memory_mechanism="random"):
    # Specify the starting sentence
    start_words = start_words.split(" ")

    # Make sure all words are valid
    for word in start_words:
        if word not in vocab:
            raise KeyError("{} not found in vocabulary.".format(word))

    if memory_mechanism not in ["random", "uniform", "decaying"]:
        raise KeyError("Invalid memory mechanism")

    # Specify the choice of weigts
    weight_choice = "random"
    gamma = 0.5
    if weight_choice == "uniform":
        weights = np.zeros(len(start_words)) + 1
        weights = weights / len(start_words)
    elif weight_choice == "decaying":
        weights = [0] * len(start_words)
        for i in range(len(start_words)):
            weights[i] = math.pow(gamma, i)

        weights.reverse()
        weights = np.array(weights) / sum(weights)
    else:
        weights = np.array(random.sample(range(0, 100), len(start_words)))
        weights = weights / sum(weights)

    current_word = start_words[-1]

    # Number of steps to look back
    lookback = len(start_words)

    while current_word != "!endline!":
        # Get the last "n" words, where "n" is the lookback amount
        lookback_words = start_words[-(lookback):]

        # Start with the furthest back word and use it's distribution as the start
        row_ind = vocab_to_id[start_words[-len(start_words)]]
        prob_dist = weights[0] * np.array(mat_norm.getrow(row_ind).todense())[0]

        # For all the rest of the words, add the weighted probability distribution to the result
        for i, word in enumerate(lookback_words[1:]):
            row_ind = vocab_to_id[word]
            prob_dist += (
                weights[i + 1] * np.array(mat_norm.getrow(row_ind).todense())[0]
            )

        # Make sure we don't have repeats
        current_word = start_words[-1]
        while current_word in lookback_words:
            next_ind = np.random.choice(range(len(vocab)), p=prob_dist)
            current_word = id_to_vocab[next_ind]

        # Append the predicted word the results
        start_words.append(current_word)

    return " ".join(start_words[:-1]).capitalize()


def generate(start_word, project, memory=False, memory_mechanism="uniform"):
    """Generate a word phrase with the given inputs.

    Args:
        start_word (srt): The starting phrase for the generator.
        project (str): The name of the project.
        memory (bool, optional): Whether to use memory. Defaults to False.
        memory_mechanism (str, optional): What memory mechanism to use.
            Defaults to "uniform".

    Returns:
        (str): The generated message.
    """

    if project not in project_to_path:
        raise KeyError("Could not find the given project.")

    load_resources(project)

    if not start_word:
        start_word = random.choice(list(vocab))

    start_word = start_word.lower()
    remove_non_alphabetic = re.compile("[^a-zA-Z ]")
    start_word = re.sub(pattern=remove_non_alphabetic, string=start_word, repl="")

    if not memory:
        if len(start_word.split(" ")) != 1:
            raise ValueError("If not using memory, only a single word can be entered.")
        else:
            return normal_generate(start_word)
    else:
        if len(start_word.split(" ")) <= 1:
            raise ValueError("If using memory, more than one word must be entered.")
        else:
            return memory_generate(start_word, memory_mechanism)


if __name__ == "__main__":
    print(generate("", "biblical_trump"))
    print(generate("I", "biblical_trump"))
    print(generate("I am", "biblical_trump", memory=True))
