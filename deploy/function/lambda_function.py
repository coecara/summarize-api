# coding: utf-8
import re


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


texts = "はい！どうも、こんにちは今日はですねここから調理しますやっぱり調理しませんえーっと文章要約 API についてお話ししていきたいと思いますはいえーとですね今回作ったのは文章をその API に投げるとですねあの作業に予約して変換してくれるというとても便利なあのあれですねいいものですねあ最近ですね雨の情報はすごくレベルには多くてこれをですねなんとかこうま短くして知りたいというニーズがあると思うのでそれにすごくお勧めですね他にも使いどころとしてはですねあのー例えばこうメールの APN Chrome 拡張機能と組み合わせてメールの予約をしたりだとか後は2と WordPress のプラグインと組み合わせていい記事のあの文頭にですね産業予約を追加したりできるとても便利な API ですこれを OSS として公開したので是非皆さん使ってみてくださいはいありがとうございます"

# splited_text = segment(texts)
# lexrank_list = get_lexrank(splited_text)
# result = generate_summary(splited_text, lexrank_list, 5)
