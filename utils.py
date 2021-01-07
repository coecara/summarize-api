# Original file is https://github.com/katryo/tfidf_with_sklearn/blob/master/utils.py

import MeCab
import os
import pdb

# 標準出力（ターミナル）をut-f8に指定する。デバッグ用。
# https://hodalog.com/about-unicodeencodeerror-using-japanese-in-python-code/
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Mecabの解析結果から語幹を抽出する関数
# 通常は「すべて自分のほうへ」の入力に対して、次のような結果を返す。
# ['すべて\t名詞,副詞可能,*,*,*,*,すべて,スベテ,スベテ', '自分\t名詞,一般,*,*,*,*,自分,ジブン,ジブン', 'の\t助詞,連体化,*,*,*,*,の,ノ,ノ', 'ほう\t名詞,非自立,一般,*,*,*,ほう,ホウ,ホー', 'へ\t助詞,格助詞,一般,*,*,*,へ,ヘ,エ', 'EOS', '']
# そこから、
# ['すべて', '自分', 'の', 'ほう', 'へ']を抽出する。
def _split_to_words(text, to_stem=False):
    """
    入力: 'すべて自分のほうへ'
    出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
    """
    tagger = MeCab.Tagger('-r /etc/mecabrc')  # 別のTaggerを使ってもいい
    mecab_result = tagger.parse(text)
    info_of_words = mecab_result.split('\n')
    words = []
    for info in info_of_words:
        # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
        if info == 'EOS' or info == '':
            break
            # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
        info_elems = info.split(',')
        # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
        if info_elems[6] == '*':
            # info_elems[0] => 'ヴァンロッサム\t名詞'
            words.append(info_elems[0][:-3])
            continue
        if to_stem:
            # 語幹に変換
            words.append(info_elems[6])
            continue
        # 語をそのまま
        words.append(info_elems[0][:-3])
    return words


def words(text):
    words = _split_to_words(text, to_stem=False)
    return words


def stems(text):
    stems = _split_to_words(text, to_stem=True)
    return stems

# stemsのデバッグ用
# print(stems('すべて自分のほうへ'))