import MeCab
import os

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

    # Mecabの設定
    # IPA辞書を利用
    # ipadic_tagger = MeCab.Tagger('-O wakati -r /dev/null -d /mnt/lambda/lib/mecab/dic/ipadic')
    ipadic_tagger = MeCab.Tagger('-r /dev/null -d /mnt/lambda/lib/mecab/dic/ipadic')

    # NEologdを利用
    # neologd_tagger = MeCab.Tagger('-O wakati -r /dev/null -d /mnt/lambda/lib/mecab/dic/mecab-ipadic-neologd')
    
    # mecabdir = os.path.join(os.getcwd(), "/var/task/.mecab")
    # output_format_type = "chasen"
    # dicdir = os.path.join(mecabdir, "lib/mecab/dic/ipadic")
    # rcfile = os.path.join(mecabdir, "etc/mecabrc")

    # tagger = MeCab.Tagger("-O{} -d{} -r{}".format(output_format_type, dicdir, rcfile))

    mecab_result = ipadic_tagger.parse(text)
    info_of_words = mecab_result.split("\n")
    words = []
    for info in info_of_words:
        # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
        if info == "EOS" or info == "":
            break
            # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
        info_elems = info.split(",")
        # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
        if info_elems[6] == "*":
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
