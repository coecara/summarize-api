# -*- coding: utf-8 -*-
import re

def segment(text):
    #改行削除
    text = text.replace( '\n' , '' )
    #。！？の後に改行追加
    pattern = re.compile(r'(。|！|？|\?|\!)')
    text = pattern.sub(r'\1\n', text)
    #改行で分割
    splited = text.splitlines()
    # リストの末尾を削除
    if '' == splited[-1]: 
        del splited[-1]
    return splited