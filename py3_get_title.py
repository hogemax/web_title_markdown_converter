from urllib.request import urlopen
from bs4 import BeautifulSoup as bs4
import sys
import re
import os
import subprocess
import requests as req

args = sys.argv
flag = 0
url =''

# 取得先URL 初期化
if len(args) > 1 and args[1]:
    #引数があれば定義
    single_arg_url = "http(.+)"
    list_file_txt = "(.*)_url_list.txt"
    SingleURL = re.search(single_arg_url, args[1])
    ListFile = re.search(list_file_txt, args[1])
    if SingleURL:
        url = args[1]
        flag = 1
    if ListFile:
        read_list_file = args[1]
        flag = 2
else:
    # 固定設定しているURLを読み込むように設定
    url = "https://qiita.com/ntkgcj"

def titleGetter(url):
    html = req.get(url, timeout=2000)
    if html.status_code == 200:
        soup = bs4(html.content, 'html.parser')
        return soup.title
    else:
        return ''
    #return soup.title

# ファイルを読み込んで出力
def outputUrlListFile():
    f = open(read_list_file, mode='r', encoding='utf-8')
    data = f.read()
    lines = data.strip().split("\n")
    apd_url_arg = []
    for line in lines:
        plus_url = outputArgURL(line)
        apd_url_arg.append(plus_url)

    result_url = ":::*(.u.)*:::".join(apd_url_arg).replace(":::*(.u.)*:::", "\n")
    clipboardCopyUrl(result_url)
    return result_url

    f.close()

# 単体用
# 整形された文字列を返す
def outputArgURL(url):
    r_ssl_pattern = "https://(.+)"
    r_url_pattern = "http://(.+)"
    SslCertainlyUrl = re.match(r_ssl_pattern, url)
    CertainlyUrl = re.match(r_url_pattern, url)
    # URLの形式が正しいか確認
    if (CertainlyUrl or SslCertainlyUrl):
        # URL取得を行う
        url_tag_title = titleGetter(url)
        shaped_sentence = "[" + url_tag_title.string + "](" + str(url) + ")"
        return shaped_sentence
    else:
        # そのまま文字列を返す
        return url

# クリップボードに保存する処理
def clipboardCopyUrl(cp_url_words):
    if sys.platform == "darwin" :
        text = cp_url_words.encode('utf-8','ignore') if isinstance(cp_url_words,str) else ''
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(text)
        p.stdin.close()
        retcode = p.wait()


## --- 引数があれば処理実行 --- ##
if len(args) > 1 and args[1]:
    if flag == 1:
        # 引数の単体URLからタイトルを取得して整形＆出力
        p_text = outputArgURL(url)
        clipboardCopyUrl(p_text)
        print('_'*30 + "\n" + p_text + "\n" + '_'*30 )
    elif flag == 2:
        # URL一覧をファイルで読み込んで一括出力処理
        p_text =[]
        p_text = outputUrlListFile()
        print('_'*30 + "\n" + p_text + "\n" + '_'*30 )
    else:
        print("（・⊆・）？") # 引数が無効判定
else:
    print (outputArgURL(url)) #初期値
    print("（・〆・）") # 引数なしで実行した場合
