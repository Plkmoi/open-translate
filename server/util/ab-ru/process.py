import sentencepiece as spm
from mosestokenizer import *
import ctranslate2
import re

def translate(src_list,sp_path_src,sp_path_tgt,ct_path):
    tokenize = MosesTokenizer('ru')
    sp_src = spm.SentencePieceProcessor()
    sp_src.load(sp_path_src)
    lengths = []
    temp = []
    p_big = re.compile('Ҧ')
    g_big = re.compile('Ҕ')
    p_small = re.compile('ҧ')
    g_small = re.compile('ҕ')
    for text in src_list:
        text = p_big.sub('Ԥ', text)
        text = g_big.sub('Ӷ', text)
        text = p_small.sub('ԥ', text)
        text = g_small.sub('ӷ', text)
        if text != '':
            with MosesSentenceSplitter('ru') as splitsents:
                text = splitsents([text])
        lengths.append(len(text))
        temp.extend(text)
    src_list = temp
    for i, text in enumerate(src_list):
        text = ' '.join(tokenize(text)).lower()
        text = sp_src.encode(text, out_type=str)
        src_list[i] = text
    translator = ctranslate2.Translator(ct_path)
    tgt_list = translator.translate_batch(src_list)
    for i, text in enumerate(tgt_list):
        detokenize = MosesDetokenizer('ru')
        sp_tgt = spm.SentencePieceProcessor()
        sp_tgt.load(sp_path_tgt)
        text = sp_tgt.decode(text[0]['tokens'])
        text = detokenize(text.split(' '))
        tgt_list[i] = text
    temp = []
    i = 0
    for length in lengths:
        text = ''
        for jw in range(length):
            text = text + tgt_list[i+jw] + ' '
        temp.append(text.strip())
        i = i + length
    tgt_list = temp
    return tgt_list
