# 標準出力（ターミナル）をut-f8に指定する。デバッグ用。
# https://hodalog.com/about-unicodeencodeerror-using-japanese-in-python-code/
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import tfidf
import numpy as np

def PowerMethod(CosineMatrix, N, err_tol):

    p_old = np.array([1.0/N]*N)
    err = 1

    while err > err_tol:
        err = 1
        p = np.dot(CosineMatrix.T, p_old)
        err = np.linalg.norm(p - p_old)
        p_old = p

    return p

def lexrank(sentences, N, threshold, vectorizer):
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
            CosineMatrix[i,j] = tfidf.compute_cosine(vector[i], vector[j])
            if CosineMatrix[i,j] > threshold:
                CosineMatrix[i,j] = 1
                degree[i] += 1
            else:
                CosineMatrix[i,j] = 0

    # 2.LexRank計算                                                                                                                                            
    for i in range(N):
        for j in range(N):
            CosineMatrix[i,j] = CosineMatrix[i,j] / degree[i]

    L = PowerMethod(CosineMatrix, N, err_tol=10e-6)

    return L

import segmenter
texts = 'こんにちは、オオハシナオキです。最近、ブログをNetlifCMSからWordPressに移行しました。なぜNetlifyCMSからWordPressに移行したのか移行した理由は一言でいうと、課題を解決するプロダクト・ツールを作ってみたかったからです。で、どうせ作るなら自分の体験ベースの課題を解決する物を作りたいなと。あと前々から、「テキストコミュニケーション」をテーマに、何か作りたいと思っていました。そう考えた時に、WordPressは、世界中のサイトの1/3で使われている。唯一のハック可能なコンテンツプラットフォームという特徴がありました。note / Medium / Facebook / Twitter など、文章を書く事のできるコンテンツプラットフォームは多数あります。ただ、サードパーティーの開発者として、ユーザーの執筆体験を向上させることのできるプラットフォームはWordPressだけです。書き手の執筆体験を、向上したい。自分も、もっと楽に早く記事を書きたいです。文章書くのツライ問題を解決したいです。今後は、執筆体験の向上のため、もっと楽に記事を書けるように、ツールを作ったりしていこうと思います。もし、この活動に興味のある方はTwiiterなどで絡んでもらえると嬉しいです!'
texts = segmenter.segment(texts)

# 参考記事のstem関数で語幹を抽出
from utils import stems  # 参考記事の実装ほぼそのまま
sentences = [stems(text) for text in texts]

lexrank_array = lexrank(sentences, len(sentences), 0.1, "tf-idf")

summary_texts_raw = []

for index in range(len(lexrank_array)):
    summary_texts_raw.append([lexrank_array[index],index])

summary_texts_raw_sorted = sorted(summary_texts_raw, reverse=True)

def generate_summary(texts, summary_texts_raw_sorted):
    summary_text = ""
    for index in range(len(summary_texts_raw_sorted)):
        item = summary_texts_raw_sorted[index]

        if 3 > index:
            text_index = item[1]
            summary_text+=texts[text_index]

    return summary_text

print(generate_summary(texts, summary_texts_raw_sorted))