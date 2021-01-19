import tfidf
import numpy as np


def PowerMethod(CosineMatrix, N, err_tol):

    p_old = np.array([1.0 / N] * N)
    err = 1

    while err > err_tol:
        err = 1
        p = np.dot(CosineMatrix.T, p_old)
        err = np.linalg.norm(p - p_old)
        p_old = p

    return p


def calc_lexrank(sentences, N, threshold, vectorizer):
    """
    LexRankで文章を要約する．
    @param  sentences: list
        文章([[w1,w2,w3],[w1,w3,w4,w5],..]のような文リスト)
    @param  n: int
        文章に含まれる文の数
    @param  t: float
        コサイン類似度の閾値(default 0.1)
    @return : list
        LexRank
    """
    CosineMatrix = np.zeros([N, N])
    degree = np.zeros(N)
    L = np.zeros(N)

    if vectorizer == "tf-idf":
        vector = tfidf.compute_tfidf(sentences)
    elif vectorizer == "word2vec":
        vector = tfidf.compute_word2vec(sentences)

    # 1. 隣接行列の作成
    for i in range(N):
        for j in range(N):
            CosineMatrix[i, j] = tfidf.compute_cosine(vector[i], vector[j])
            if CosineMatrix[i, j] > threshold:
                CosineMatrix[i, j] = 1
                degree[i] += 1
            else:
                CosineMatrix[i, j] = 0

    # 2.LexRank計算
    for i in range(N):
        for j in range(N):
            CosineMatrix[i, j] = CosineMatrix[i, j] / degree[i]

    L = PowerMethod(CosineMatrix, N, err_tol=10e-6)

    return L
