#!/usr/bin/python
#coding:UTF-8
#author: Andrey Kutuzov; html2fb library by Chris Clark (https://code.google.com/p/html2fb/) is used
#license: GNU GPL v3
#Extracting TrV articles into one HTML and one FB2

import re
import codecs
import os
import subprocess
import h2fb

x = raw_input('Введите адрес страницы с номером ТрВ:')

#Finding directory with articles...
catalogue = x[21:]

#Actually downloading pages...
subprocess.call(['wget', '-r', '-l 1', '--include-directories=%s,uploads' % catalogue, '-nd', '-E', '--random-wait', '-np', '-p', '-k', x])

#Cleaning up a bit...
os.remove('index.html')
os.remove('index.html.1.html')
os.remove('robots.txt')
os.rename("index.html.1.1.html","index.html.1.01.html")
os.rename("index.html.1.2.html","index.html.1.02.html")
os.rename("index.html.1.3.html","index.html.1.03.html")
os.rename("index.html.1.4.html","index.html.1.04.html")
os.rename("index.html.1.5.html","index.html.1.05.html")
os.rename("index.html.1.6.html","index.html.1.06.html")
os.rename("index.html.1.7.html","index.html.1.07.html")
os.rename("index.html.1.8.html","index.html.1.08.html")
os.rename("index.html.1.9.html","index.html.1.09.html")

#Creating list of pages to process...
listing = os.listdir('.')
listing_html = [i for i in listing if i.endswith('.html')]
listing_html = sorted(listing_html)

#Extracting articles themselves...
text = ""
for i in listing_html:
    page = codecs.open(i,'r','utf-8').read()
    results = ()
    results = re.search(ur'(<h1>.*?)addthis_',page,re.S)
    article = results.group(1)[:-12]
    text = text+article
    os.remove(i)

#Compiling the whole content...
trv = u"<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">"+u"<html xmlns=\"http://www.w3.org/1999/xhtml\" dir=\"ltr\" lang=\"ru-RU\">"+u"<head profile=\"http://gmpg.org/xfn/11\">"+u"<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>"+u"</head>"+u"<body>"+u"Троицкий вариант №"+catalogue+'\n'+text+u"</body>"+u"</html>"

#Writing HTML to file...
catalogue = catalogue.replace('/','-')[:-1]
htmlname='trv'+catalogue+'.html'
o = codecs.open(htmlname,'w','utf-8')
o.write(trv)
o.close()
# print "Преобразование в HTML завершено. Забирайте файл trv(дата выпуска).html и все картинки из этого каталога и наслаждайтесь."

#Converting to FB2...
fb2name='trv'+catalogue+'.fb2'
params = h2fb.default_params.copy()
params['data'] = trv.encode('utf-8')
data=h2fb.MyHTMLParser().process(params)
text = data.decode('utf-8')
fb2 = codecs.open(fb2name,'w','utf-8')
fb2.write(text)
fb2.close()
print "Преобразование в fb2 завершено. Забирайте файл trv(дата выпуска).fb2 и наслаждайтесь."

#Deleting images...
listing = os.listdir('.')
listing_pics = [i for i in listing if i.endswith('.jpg') or i.endswith('.gif')]
for i in listing_pics:
    os.remove(i)

#Deleting html...
listing = os.listdir('.')
listing_html = [i for i in listing if i.endswith('.html')]
for i in listing_html:
    os.remove(i)
