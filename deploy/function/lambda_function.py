# coding: utf-8
import re
import lexrank
import utils

# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def add_end_syntax(texts):
    # 「ですから　ですと　ですし　ますと　ますから　ませんと　ませんから　ませんし」　にマッチ
    pattern1 = re.compile(r"(です|ます|ません)(と|から|し)")
    texts = pattern1.sub(r"\1\2、", texts)
    # 「ですよ　ですね　ますよ　ますね」にマッチ
    pattern2 = re.compile(r"(です|ます)(よ??ね)")
    texts = pattern2.sub(r"\1\2。", texts)

    pattern3 = re.compile(r"((です|ます)(?!(。|と|から|し|よ|ね)))")
    texts = pattern3.sub(r"\1。", texts)

    pattern4 = re.compile(r"(ください(?!(。|よ|ね|な)))")
    texts = pattern4.sub(r"\1。", texts)

    return texts


def segment(text):
    # 改行削除
    text = text.replace("\n", "")
    # 。！？の後に改行追加
    pattern = re.compile(r"(。|！|？|\?|\!)")
    text = pattern.sub(r"\1\n", text)
    # 改行で分割
    splited = text.splitlines()
    # リストの末尾を削除
    if "" == splited[-1]:
        del splited[-1]
    return splited


def get_lexrank(splited_texts):
    """Lexrankの高い順に文を配列に挿入して返す

    Args:
        splited_texts ([type]): 分割されたテキスト

    Returns:
        [type]: [lexrankスコア, 文章のindex]
    """
    words = [utils.stems(text) for text in splited_texts]
    lexranks = lexrank.calc_lexrank(words, len(words), 0.1, "tf-idf")
    return_data = [[lexranks[index], index] for index in range(len(lexranks))]
    return sorted(return_data, reverse=True)


texts = "はい！どうも、こんにちは今日はですねここから調理しますやっぱり調理しませんえーっと文章要約 API についてお話ししていきたいと思いますはいえーとですね今回作ったのは文章をその API に投げるとですねあの作業に予約して変換してくれるというとても便利なあのあれですねいいものですねあ最近ですね雨の情報はすごくレベルには多くてこれをですねなんとかこうま短くして知りたいというニーズがあると思うのでそれにすごくお勧めですね他にも使いどころとしてはですねあのー例えばこうメールの APN Chrome 拡張機能と組み合わせてメールの予約をしたりだとか後は2と WordPress のプラグインと組み合わせていい記事のあの文頭にですね産業予約を追加したりできるとても便利な API ですこれを OSS として公開したので是非皆さん使ってみてくださいはいありがとうございます"
texts = add_end_syntax(texts)
splited_texts = segment(texts)
lexranks = get_lexrank(splited_texts)

print(lexranks)

# result = generate_summary(splited_text, lexrank_list, 5)
