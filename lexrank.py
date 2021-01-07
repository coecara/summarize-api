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


texts = [
    "こんにちは、オオハシナオキです。",
    "最近、ブログをNetlifCMSからWordPressに移行しました。",
    "なぜNetlifyCMSからWordPressに移行したのか",
    "移行した理由は一言でいうと、課題を解決するプロダクト・ツールを作ってみたかったからです。",
    "で、どうせ作るなら自分の体験ベースの課題を解決する物を作りたいなと。",
    "あと前々から、「テキストコミュニケーション」をテーマに、何か作りたいと思っていました。",
    "そう考えた時に、WordPressは、",
    "世界中のサイトの1/3で使われている。",
    "唯一のハック可能なコンテンツプラットフォーム",
    "という特徴がありました。",
    "WordPressは唯一のハック可能なコンテンツプラットフォーム",
    "note / Medium / Facebook / Twitter など、文章を書く事のできるコンテンツプラットフォームは多数あります。",
    "ただ、サードパーティーの開発者として、ユーザーの執筆体験を向上させることのできるプラットフォームはWordPressだけです。",
    "やりたいこと",
    "書き手の執筆体験を、向上したい。",
    "自分も、もっと楽に早く記事を書きたいです。",
    "文章書くのツライ問題を解決したいです。",
    "まとめ",
    "今後は、執筆体験の向上のため、もっと楽に記事を書けるように、ツールを作ったりしていこうと思います。",
    "もし、この活動に興味のある方はTwiiterなどで絡んでもらえると嬉しいです!",
]

# texts = [
#     "はい、みなさんこんにちは。いしかわでございます。",
#     "さて、ベクトルは2年くらい前から全員がリモートワークに移行（遠方の人はそれ以前から）したのですが、業務ではzoomを利用しています。",
#     "で、困っていたのが",
#     "Zoomで困っていた事",
#     "メインセッションで一部の人が特定の会話をすると他のメンバーの効率が下がるケースがある",
#     "ブレイクアウトルームはあるがホストが不在の時に割当を自由にできない",
#     "オンラインイベントで懇親会でブレイクアウトルームを作ると参加者はルームを自由に移動できない",
#     "という問題があったのですが…",
#     "Zoomのアップデートでブレイクアウトルームの移動が可能になりました！",
#     "ありがとうZoom！",
#     "まずはアプリケーションのアップデートを",
#     "まずはアプリケーションのアップデートをします。",
#     "ブレイクアウトルームを作ってみる",
#     "ブレイクアウトルームを作成しようとすると「参加者によるルーム選択を許可」が！",
#     "ルームの名前を任意に変更する",
#     "ブレイクアウトルームは従来通り自由に名前を変更できるのでこんな風にしておけば…",
#     "使ってみる",
#     "いしかわさーん、もう少し給料上げて欲しいんですけど何とかなりませんか？",
#     "ここでは話せないので会議室1にお願いします。",
#     "了解でーす。",
#     "Zoomさんありがとうございます！",
#     "自分達もユーザーの皆様に喜んでいただける製品開発を頑張っていきたいと思います！",
# ]

# 参考記事のstem関数で語幹を抽出
from utils import stems  # 参考記事の実装ほぼそのまま
sentences = [stems(text) for text in texts]

lexrank_array = lexrank(sentences, len(sentences), 0.1, "tf-idf")

summary_texts_raw = []

for index in range(len(lexrank_array)):
    summary_texts_raw.append([lexrank_array[index],index])

summary_texts_raw_sorted = sorted(summary_texts_raw, reverse=True)

def generate_summary(summary_texts_raw_sorted):
    for index in range(len(summary_texts_raw_sorted)):
        summary_text = ""
        item = summary_texts_raw_sorted[index]
        
        if 3 > index:
            text_index = item[1]
            print(texts[text_index])
            summary_text+=texts[text_index]
        else:
            return summary_text

print(generate_summary(summary_texts_raw_sorted))