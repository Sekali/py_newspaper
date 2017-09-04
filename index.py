from __future__ import division
import sys
import time
import os
reload(sys)  
sys.setdefaultencoding('utf8')

import urllib
from bs4 import BeautifulSoup
data_div = ""
link_lists = []
date = {}
tmp = ''

def get_data(url):
    page = urllib.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    tmp = soup.select("div#eBack")
    with open('data.txt', 'w+') as f:
        f.write(str(tmp))
def main(path, url):
    get_data(url)
    with open(r'data.txt', 'rb+') as f:
        data_div = f.read()
    soup = BeautifulSoup(data_div, "html.parser")
    for link in soup.find_all('a'):
        link_lists.append(link.get('href'))
    a = len(link_lists)+1

    url = link_lists[-1]
    page = urllib.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    day = soup.body.span.string[8:10]
    mouth = soup.body.span.string[5:7]
    year = soup.body.span.string[0:4]
    context = str(year) + '-' + str(mouth) + '-' +str(day) + " :" + str(url)+'\n'
    with open(path, 'r') as f:
        tmp = f.read()
        if context in tmp:
            return 
    with open(path, 'a+') as f:
        f.write(context)
    time.sleep(0.3)

main('xindushi.txt', r"http://www.zgfznews.com/paper/xindushi/4790/21352/1494406.shtml")
main('fzrb.txt', r"http://www.zgfznews.com/paper/fzrb/4789/21347/1494375.shtml")