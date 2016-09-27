#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import os
import sys
import time
import webbrowser


class LZU():

    def __init__(self, opt):
        # Internation Office
        if opt == 'i':
            self.id = 0
            self.baseurl = 'http://faoffice.lzu.edu.cn'
            url = 'http://faoffice.lzu.edu.cn/lzupage/B20151224105231.html'
            pattern = r'<li><span>\((.*?)\)</span><a href="(.*?)">(.*?)</a></li>'
        # Academic Lecture
        if opt == 'a':
            self.id = 1
            self.baseurl = 'http://news.lzu.edu.cn'
            url = 'http://news.lzu.edu.cn/l/xueshujiangzuo/'
            date = time.localtime()
            year = date[0]
            month = date[1]
            pattern = '<li><a href="(.*?)" target="_blank" title=".*?">(.*?)</a> <span class="listDate">(%d-%02d.*?)</span>.*?<p>.*?</p></li>'\
                      % (year, month)
        if __name__ == '__main__':
            page = self.getPage(url)
            self.items = self.getItems(pattern, page)
            self.printItems(self.items)
            self.html_path = '%s/output.html' % os.path.dirname(os.path.realpath(__file__))

    def getPage(self, url):
        page = urllib2.urlopen(url)
        page_src = page.read()
        return page_src

    def getItems(self, pattern, page):
        pattern = re.compile(pattern, re.S)
        items = re.findall(pattern, page)
        return items

    def printItems(self, items):
        if self.id == 0:
            print '\n# 学期制交流项目：\n'
            count = 0
            for item in items:
                count += 1
                print '[%02d] %s %s' % (count, item[0], item[2].decode('gbk'))
        if self.id == 1:
            print '\n# 近期学术讲座：\n'
            count = 0
            for item in items:
                count += 1
                print '[%02d] %s %s' % (count, item[2], item[1])

    def saveHTML(self):
        html = '<!DOCTYPE html>\n'
        html += '<html lang="zh-CN">\n'
        html += '<head>\n'
        html += '<meta charset="UTF-8">\n'
        html += '<meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
        html += '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        html += '<title>兰大资讯</title>\n'
        html += '<link href="http://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">\n'
        html += '</head>\n'
        html += '<body>\n'
        html += '<div class="container">\n'
        if self.id == 0:
            html += '<div class="page-header">'
            html += '<h1>学期制交流项目</h1>\n'
            html += '</div>'
            html += '<div class="list-group">\n'
            for item in self.items:
                url = self.baseurl + item[1]
                html += '<a href="%s" class="list-group-item"><span class="glyphicon glyphicon-list-alt"></span> %s<span class="badge">%s</span></a>\n'\
                        % (url, item[2].decode('gbk').encode('utf-8'), item[0])
        if self.id == 1:
            html += '<div class="page-header">'
            html += '<h1>近期学术讲座</h1>\n'
            html += '</div>'
            html += '<div class="list-group">\n'
            for item in self.items:
                url = self.baseurl + item[0]
                html += '<a href="%s" class="list-group-item"><span class="glyphicon glyphicon-book"></span> %s<span class="badge">%s</span></a>\n'\
                        % (url, item[1], item[2])
        html += '</div>\n'
        html += '</div>\n'
        html += '<script src="http://cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>\n'
        html += '<script src="http://cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>\n'
        html += '</body>\n'
        html += '</html>\n'
        file = open('output.html', 'w')
        file.write(html)
        file.close()

    def openHTML(self):
        webbrowser.open(self.html_path)


if __name__ == '__main__':
    opt_list = ['i', 'a', 'c', 'o', 'h']
    if len(sys.argv) > 1:
        for argv in sys.argv[1:]:
            opt = argv[1]
            if opt in opt_list[:len(opt_list)-3]:
                spider = LZU(opt)
            elif opt == 'c':
                spider.saveHTML()
                if '-o' in sys.argv[1:]:
                    spider.openHTML()
            elif opt == 'o':
                pass
            elif opt == 'h':
                print 'Usage: lzuspider [OPTIONS]'
                print 'Available options:'
                print '  -i          internation office'
                print '  -a          academic lecture'
                print '  -c          create an html'
                print '  -o          open the html by default browser'
                print '  -h          print this message'
            else:
                print '\n[warning] An unavailable option was found: %s\n' % argv
                break
    else:
        print '\n[warning] Please add options.'
        print '  -h  is to print help message.\n'

