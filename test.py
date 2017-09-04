#-*-coding:utf-8-*-
from __future__ import division
from flask import Flask, url_for, render_template, request, redirect
from bs4 import BeautifulSoup
import time
import urllib
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

date = {}
date['year'] = time.strftime("%Y-%m", time.localtime())
date['day'] = time.strftime("%d", time.localtime())

app = Flask(__name__)

def index_get(name): #用于获取当日的报纸
    img_list = []
    baozhi_h = {}
    page = urllib.urlopen("http://www.zgfznews.com/paper/")
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    for i in soup.section.div.ul.find_all('a'): #找到所有的链接
        img_list.append(i)
    baozhi_h = {'fzrb':img_list[1]['href'],'xindushi':img_list[-1]['href']}  #在之中分离出2个报纸的各种封面
    return baozhi_h

def get_url(link, bz_name): #改变报纸图片中链接指向的文章
    page = urllib.urlopen(link)
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    #soup.section.img['class']= 'img-responsive' #修改下图片的样式
    #soup.section.img['width']= '100%'
    html = soup.section.img
    for i in range(0, len(html.find_all('a'))):
        tmp = html.find_all('a')[i]['href']
        html.find_all('a')[i]['href'] = '/'+bz_name+'/text/' + tmp[-24:-6]
    return html

def banmian(url, name):
    if name == 'fzrb' : zhi = 53
    if name == 'xindushi' : zhi = 57
    il = []
    page = urllib.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    ban = soup.find_all("div", class_="all-pages")
    for i in ban[0].find_all('a'):
        il.append(i['href'])
    for i in range(0, 4):
        il[i] = il[i][29:zhi]
    strs = '''<li><a href="{0}">A1</a></li>
            <li><a href="{1}">A2</a></li>
            <li><a href="{2}">A3</a></li>
            <li><a href="{3}">A4</a></li>'''.format(il[0], il[1], il[2], il[3])
    return strs

@app.route('/', defaults={'name': 'fzrb'})
@app.route('/<name>/', methods=['POST', 'GET']) #主页显示各个报纸的封面，并处理post跳转页面
def index(name):
    baozhi = ''
    if request.method == 'GET':
        if name == 'fzrb' : baozhi = 'A报'
        if name == 'xindushi' : baozhi = 'B报'
        baozhi_h = index_get(name)
        img = get_url(baozhi_h[name], name)
        ban = banmian(baozhi_h[name], name)
        name = '/' + name + '/'
        return render_template('index.html',name='action={0}'.format(name), img=img, baozhi=baozhi, ban=ban)
    elif request.method == 'POST':
        data = request.form['fname']
        data = data.replace('/','-')
        if name == "fzrb":
            return redirect(url_for("fzrb", year=data[:7], day=data[8:]))
        elif name == "xindushi":
            return redirect(url_for("xindushi", year=data[:7], day=data[8:]))
    
@app.route('/fzrb/<year>/<day>')
def fzrb(year, day):
    link = ""
    ban = ""
    with open('fzrb.txt', 'r+') as f: #从index里获取对应的报纸进行跳转
        tmp = f.read()
        a = tmp.find(year+'-'+day)
        if a == -1:
            html_date = "所访问的 " + year+'-'+day + "号的报纸并不存在"
            return render_template('miss.html', date=html_date) #如果页面不存在就显示404
        link = tmp[a+12:a+71]
    img = get_url(link, "fzrb")
    ban = banmian(link, 'fzrb')
    return render_template('index.html', name='action="/fzrb/"', img=img,  baozhi='A报', ban=ban) #修改页面对不同报纸的跳转地址

@app.route('/xindushi/<year>/<day>')
def xindushi(year, day):
    link = ""
    ban = ""
    with open('xindushi.txt', 'r+') as f:
        tmp = f.read()
        a = tmp.find(year+'-'+day)
        if a == -1:
            html_date = "所访问的 " + year+'-'+day + "号的报纸并不存在"
            return render_template('miss.html', date=html_date)
        link = tmp[a+12:a+75]
    img = get_url(link, "xindushi")
    ban = banmian(link, 'xindushi')
    return render_template('index.html', name='action="/xindushi/"', img=img,  baozhi='B报', ban=ban)

@app.route('/<name>/text/<a>/<b>/<c>')
def text(name, a, b, c): #文章显示页面
    link = "http://www.zgfznews.com/paper/"+ name + "/" + a + '/' + b + '/' + c + ".shtml"
    page = urllib.urlopen(link)
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    title1 = soup.body.section.h1
    title2 = soup.body.section.h3
    context = soup.body.section.article
    return render_template('text1.html', title1=title1, title2=title2, context=context)

@app.route('/<name>/<a>/<b>/<c>')
def banmian_chuli(name, a, b, c):
    baozhi = ''
    if name == 'fzrb' : baozhi = 'A报'
    if name == 'xindushi' : baozhi = 'B报'
    url = "http://www.zgfznews.com/paper/" + name + "/" + a + '/' + b + '/' + c + ".shtml"
    img = get_url(url, name)
    ban = banmian(url, name)
    return render_template('index.html', name='action="/fzrb/"', img=img,  baozhi=baozhi, ban=ban)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
@app.errorhandler(500)
def web_error(error):
    return render_template('500.html'), 500


with app.test_request_context():
    url_for('static', filename='style.css')
    url_for('static', filename='laydate.css')

app.run(debug=True)