#!/usr/bin/python
# coding: utf-8
# author: Andrey Kutuzov; html2fb library by Chris Clark (https://code.google.com/p/html2fb/) is used
# license: GNU GPL v3
# Extracting TrV articles into one HTML and one FB2

import re
import codecs
import os
import subprocess


def trving(x):
    # Finding directory with articles...
    x = x.replace('https:', 'http:')
    catalogue = x[21:]

    os.chdir('.')

    # Actually downloading pages...
    subprocess.call(['wget', '-r', '-l 1', '--restrict-file-names=nocontrol',
                     '--include-directories=%s,uploads,trv-science.ru/uploads' % catalogue, '-nd', '-E',
                     '--random-wait', '-np', '-p', '-k', '-H', x])

    # Cleaning up a bit...
    os.remove('index.html')
    try:
        os.remove('index.html.1.html')
    except:
        pass
    os.remove('robots.txt')
    os.rename("index.html.1.1.html", "index.html.1.01.html")
    os.rename("index.html.1.2.html", "index.html.1.02.html")
    os.rename("index.html.1.3.html", "index.html.1.03.html")
    os.rename("index.html.1.4.html", "index.html.1.04.html")
    os.rename("index.html.1.5.html", "index.html.1.05.html")
    os.rename("index.html.1.6.html", "index.html.1.06.html")
    os.rename("index.html.1.7.html", "index.html.1.07.html")
    try:
        os.rename("index.html.1.8.html", "index.html.1.08.html")
    except:
        pass
    try:
        os.rename("index.html.1.9.html", "index.html.1.09.html")
    except:
        pass

    listing = os.listdir('.')
    listing_pics = [i for i in listing if '.jpg' in i or '.gif' in i or 'png' in i]
    for pic in listing_pics:
        newname = pic.replace('%2C', ',')
        os.rename(pic, newname)
    listing = os.listdir('.')

    # Creating list of pages to process...
    listing_html = [i for i in listing if i.endswith('.html')]
    listing_html = sorted(listing_html)

    # Extracting articles themselves...
    titles = set()
    text = ""
    for i in listing_html:
        page = codecs.open(i, 'r', 'utf-8').read()
        title = re.search(ur'<h1.*?>(.*?)</h1>', page, re.S)
        if title:
            title = title.group(1).strip()
            if title in titles:
                continue
            else:
                results = re.search(ur'(<header.*?)<div class="mistape_', page, re.S)
                if results:
                    article = results.group(1)
                    article = article.replace('</div></p>', '</div>')
                    article = article.replace(']</p></div>', ']</p></div><p>') + '</div>'
                    titles.add(title)
                else:
                    article = ''
                text += article
        os.remove(i)

    # Compiling the whole content...
    text = text.replace('%3F', '?')
    text = text.replace('%252C', ',')
    trv = u"<!DOCTYPE html PUBLIC \"-//W3C//DTD " \
          u"XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">" \
          + u"<html xmlns=\"http://www.w3.org/1999/xhtml\" dir=\"ltr\" lang=\"ru-RU\">" \
          + u"<head profile=\"http://gmpg.org/xfn/11\">" \
          + u"<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>" \
          + u"</head>" + u"<body>" + u"Троицкий вариант №" + catalogue + '\n' + text + u"</body>" + u"</html>"

    # Writing HTML to file...
    catalogue = catalogue.replace('/', '-')[:-1]
    htmlname = 'trv' + catalogue + '.html'
    o = codecs.open(htmlname, 'w', 'utf-8')
    o.write(trv)
    o.close()
    fb2name = htmlname.replace('.html', '.fb2')

    # Converting to FB2...
    subprocess.call(['ebook-convert', htmlname, fb2name])
    # print "Преобразование в fb2 завершено. Забирайте файл trv(дата выпуска).fb2 и наслаждайтесь."

    # Deleting images...
    listing_pics = [i for i in listing if '.jpg' in i or '.gif' in i or 'png' in i]
    for i in listing_pics:
        os.remove(i)

    # Deleting html...
    listing = os.listdir('.')
    listing_html = [i for i in listing if '.html' in i]
    for i in listing_html:
        os.remove(i)

    subprocess.call(['gzip', fb2name])
