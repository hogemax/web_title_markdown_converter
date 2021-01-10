'''This is a test program.'''
# -*- coding: utf-8 -*-

import sys
import re
import os
import subprocess
from bs4 import BeautifulSoup as bs4
import requests as req
import pyperclip as pc

# グローバル変数
args = sys.argv
FLAG = 0
BDOURL = ''

# 取得先URL 初期化
if len(args) > 1 and args[1]:
    #引数があれば定義
    SINGLE_ARG_URL = "http(.+)"
    SingleURL = re.search(SINGLE_ARG_URL, args[1])
    if SingleURL:
        BDOURL = args[1]
        FLAG = 1

elif len(args) == 1:
    FLAG = 2

else:
    # 固定設定しているURLを読み込むように設定
    BDOURL = "https://qiita.com/ntkgcj"

def title_getter(BDOURL):
    html = req.get(BDOURL, timeout=2000)
    if html.status_code == 200:
        soup = bs4(html.content, 'html.parser')
        return soup.title
    else:
        return ''
    #return soup.title


def output_url_list_file():
    """
   クリップボードから読み込んだ内容を1行ずつ処理して結果をクリップボードに保存
    """
    lines = pc.paste().split("\n")
    #print(lines)
    apd_url_arg = []
    for line in lines:
        plus_url = output_arg_url(line)
        apd_url_arg.append(plus_url)

    result_url = ":::*(.u.)*:::".join(apd_url_arg).replace(":::*(.u.)*:::", "\n")
    store_url_to_clipboard(result_url)
    return result_url


def output_arg_url(BDOURL):
    """
   単体用
   整形された文字列を返す
    """
    r_ssl_pattern = "https://(.+)"
    r_url_pattern = "http://(.+)"
    ssl_certainly_url = re.match(r_ssl_pattern, BDOURL)
    certainly_url = re.match(r_url_pattern, BDOURL)
    # URLの形式が正しいか確認
    if (certainly_url or ssl_certainly_url):
        # URL取得を行う
        url_tag_title = title_getter(BDOURL)
        shaped_sentence = "[" + url_tag_title.string + "](" + str(BDOURL) + ")"
        return shaped_sentence
    else:
        # そのまま文字列を返す
        return BDOURL



def store_url_to_clipboard(cp_url_words):
    """
   MarkDown形式に書き換えたURL文字列内容をクリップボードに保存
    """
    text = cp_url_words.encode('utf-8', 'ignore') if isinstance(cp_url_words, str) else ''
    wsl2_path_pattern = "^\/mnt\/"

    if sys.platform == "darwin": # MacOS X
        #text = cp_url_words.encode('utf-8', 'ignore') if isinstance(cp_url_words, str) else ''
        p_b = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)

    if(sys.platform == "linux" or sys.platform == "linux2"):
        if(re.match(wsl2_path_pattern, os.environ['HOME'])):
            # WSL2 Windows
            p_b = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE)

    p_b.stdin.write(text)
    p_b.stdin.close()

#print(FLAG)



def decoration_lines():
    """
   表示を装飾
    """
    if FLAG == 1 or FLAG == 2:
        print("\n----------------->>")
        print(pc.paste()) if FLAG == 2 else print(BDOURL)
        print("----------------->>")
    else:
        print("（・〆・）")


## メイン処理 ##
decoration_lines()
## --- 引数があれば処理実行 --- ##
if len(args) > 1 and args[1]:
    if FLAG == 1:
        # 引数の単体URLからタイトルを取得して整形＆出力
        P_TEXT = output_arg_url(BDOURL)
        store_url_to_clipboard(P_TEXT)
        print('_'*30 + "\n" + P_TEXT + "\n" + '_'*30)
    else:
        print("（・⊆・）？") # 引数が無効判定

elif FLAG == 2:
    # URL一覧をクリップボードから読み込んで一括出力処理
    P_TEXT = []
    P_TEXT = output_url_list_file()
    print('_'*30 + "\n" + P_TEXT + "\n" + '_'*30)
else:
    print(output_arg_url(BDOURL)) #初期値
    print("（・〆・）") # 引数なしで実行した場合
