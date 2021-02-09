# coding: utf-8
import re
import lexrank
import utils
import operator
import json

def add_end_syntax(texts):
    """文末に句読点（。、）を追加する関数

    Args:
        texts (string): テキスト

    Returns:
        string: 句読点が追加されたテキスト
    """
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
    """。や文末記号で文を分割する関数

    Args:
        text (string): テキスト

    Returns:
        list of string: 分割されたテキストの配列
    """
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
    """Lexrankの高い順に、lexrankと文章のindexをリストに追加して返す関数

    Args:
        splited_texts (list of string): 句読点で分割されたテキスト

    Returns:
        list of list of float, int: [[lexrankスコア, 文章のindex]...]
    """
    words = [utils.stems(text) for text in splited_texts]
    lexranks = lexrank.calc_lexrank(words, len(words), 0.1, "tf-idf")
    return_data = [[lexranks[index], index] for index in range(len(lexranks))]
    return sorted(return_data, reverse=True)


def generate_summary(splited_texts, lexranks, line_count):
    """文章とLexrankから要約を作成する関数

    Args:
        splited_texts (list of string): 句読点で分割されたテキスト
        lexranks （list of list of float, int): lexrankスコアと文章のindexを含むリストのリスト
        line_count (int): 要約文章の行数

    Returns:
        string: 要約文章
    """
    line_count = int(line_count)
    lexranks = lexranks[0:line_count]
    # 文章のindex順にソート
    lexranks_sorted = sorted(lexranks, key=operator.itemgetter(1))

    summary = ""
    for item in lexranks_sorted:
        text_index = item[1]
        summary += splited_texts[text_index]

    return summary


def generate_summary_wrapper(texts, line_count):
    texts = add_end_syntax(texts)
    splited_texts = segment(texts)
    lexranks = get_lexrank(splited_texts)
    return generate_summary(splited_texts, lexranks, line_count)


def lambda_handler(event, context):
    req_body = json.loads(event["body"])
    summary = generate_summary_wrapper(req_body["text"], req_body["line_count"])
    res_body = {"summary": summary}
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'https://coecara.com',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,'
        },
        "body": json.dumps(res_body),
    }
