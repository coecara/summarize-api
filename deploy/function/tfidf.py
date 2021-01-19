# -*- coding: utf-8 -*-
import numpy as np
import fasttext as ft
from scipy.spatial import distance


def word2id(bow, word_id):

    for w in bow:
        if word_id.__contains__(w) is False:
            word_id[w] = len(word_id)

    return word_id


def compute_tf(sentences, word_id):

    tf = np.zeros([len(sentences), len(word_id)])

    for i in range(len(sentences)):
        for w in sentences[i]:
            tf[i][word_id[w]] += 1

    return tf


def compute_df(sentences, word_id):

    df = np.zeros(len(word_id))

    for i in range(len(sentences)):
        exist = {}
        for w in sentences[i]:
            if exist.__contains__(w) is False:
                df[word_id[w]] += 1
                exist[w] = 1
            else:
                continue

    return df


def compute_idf(sentences, word_id):

    idf = np.zeros(len(word_id))
    df = compute_df(sentences, word_id)

    for i in range(len(df)):
        idf[i] = np.log(len(sentences) / df[i]) + 1

    return idf


def compute_tfidf(sentences):

    word_id = {}

    for sent in sentences:
        word_id = word2id(sent, word_id)

    tf = compute_tf(sentences, word_id)
    idf = compute_idf(sentences, word_id)

    tf_idf = np.zeros([len(sentences), len(word_id)])

    for i in range(len(sentences)):
        tf_idf[i] = tf[i] * idf

    return tf_idf


def compute_cosine(v1, v2):

    return 1 - distance.cosine(v1, v2)


def sent2vec(bow, model_w):

    vector = np.zeros(100)
    N = len(bow)

    for b in bow:
        try:
            vector += model_w[b]
        except:
            continue

    vector = vector / float(N)

    return vector


def compute_word2vec(sentences):

    model_w = ft.load_model("../models/wiki_sg_d100.bin")
    vector = np.zeros([len(sentences), 100])

    for i in range(len(sentences)):
        vector[i] = sent2vec(sentences[i], model_w)

    return vector


if __name__ == "__main__":

    pass
