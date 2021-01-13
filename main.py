
# 参考記事のstem関数で語幹を抽出
import lexrank
from utils import stems
def get_lexrank(texts):
    sentences = [stems(text) for text in texts]
    lexrank_list = lexrank.lexrank(sentences, len(sentences), 0.1, "tf-idf")
    lexrank_list_with_index = [[lexrank_list[index],index] for index in range(len(lexrank_list))]
    return sorted(lexrank_list_with_index, reverse=True)

from operator import itemgetter
def sort_lexrank_by_index(splited_text, summary_text):
    summary_text_data = sorted(summary_text,  key=itemgetter(1))
    summary_text=''
    for item in summary_text_data:
        index = item[1]
        summary_text+=splited_text[index]
    return summary_text

def generate_summary(splited_text, lexrank_list_data, paragraph_count):
    summary_text = []
    for index in range(len(lexrank_list_data)):
        item = lexrank_list_data[index]
        if paragraph_count > index:
            summary_text.append(item)
    return sort_lexrank_by_index(splited_text, summary_text)

import segmenter
texts = 'こんにちは、オオハシナオキです。最近、ブログをNetlifCMSからWordPressに移行しました。なぜNetlifyCMSからWordPressに移行したのか移行した理由は一言でいうと、課題を解決するプロダクト・ツールを作ってみたかったからです。で、どうせ作るなら自分の体験ベースの課題を解決する物を作りたいなと。あと前々から、「テキストコミュニケーション」をテーマに、何か作りたいと思っていました。そう考えた時に、WordPressは、世界中のサイトの1/3で使われている。唯一のハック可能なコンテンツプラットフォームという特徴がありました。note / Medium / Facebook / Twitter など、文章を書く事のできるコンテンツプラットフォームは多数あります。ただ、サードパーティーの開発者として、ユーザーの執筆体験を向上させることのできるプラットフォームはWordPressだけです。書き手の執筆体験を、向上したい。自分も、もっと楽に早く記事を書きたいです。文章書くのツライ問題を解決したいです。今後は、執筆体験の向上のため、もっと楽に記事を書けるように、ツールを作ったりしていこうと思います。もし、この活動に興味のある方はTwiiterなどで絡んでもらえると嬉しいです!'
splited_text = segmenter.segment(texts)
lexrank_list = get_lexrank(splited_text)
result = generate_summary(splited_text, lexrank_list, 3)