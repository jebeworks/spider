__author__ = 'DCD'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import string
import time
import numpy as np
import pandas as pd
import csv

#import urllib.request
#http://fund.eastmoney.com/f10/jjjz_000697.html
#http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=000697&page=1&per=20&sdate=&edate=&rt=0.2289961661162161
#http://fund.eastmoney.com/js/fundcode_search.js

#http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code=000697&topline=10&year=&month=&rt=0.8884351801845889
#http://fund.eastmoney.com/f10/F10DataApi.aspx?type=hypz&code=000697&year=2016&rt=0.21980476212178313
#http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=hypzsy&code=000697&rt=0.5281546500642944
#http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=gmbd&mode=0&code=000697&rt=0.09567990767947365
#http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=cwzb&code=000697&showtype=1&year=&rt=0.03965805350296048


class Spider:
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'

    def getPage(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        print url

        #request = urllib.request.Request(url)
        #response = urllib.request.urlopen(request)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        return response.read().decode('gbk')

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(
            '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern, page)
        for item in items:
            print(item[0], item[1], item[2], item[3], item[4])


#spider = Spider()
#spider.getContents(2)

class TtjjSpider:
    def __init__(self):
        self.siteURL = 'http://fund.eastmoney.com/f10/'

    def getPage(self, code, per):
        url = self.siteURL + "F10DataApi.aspx?type=lsjz&code=" + code + "&page=1&per=" + str(per) + "&sdate=&edate=&rt=0.2289961661162161"
        #print url

        #request = urllib.request.Request(url)
        #response = urllib.request.urlopen(request)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        return response.read()

    def getContents(self, code):
        page = self.getPage(code, 1)
        #print page

        pattern = re.compile('var apidata={ content:"<table class=.*?>.*?</table>",records:(.*?),pages:.*?,curpage:.*?};',re.S)
        recordsStr = re.findall(pattern, page)
        records = int(('').join(recordsStr))

        #page = self.getPage(code, 10)
        page = self.getPage(code, records)
        #print page
        pattern = re.compile(
            '<tr><td>(.*?)</td><td class=.*?>(.*?)</td><td class=.*?>(.*?)</td>.*?</tr>',re.S)

        items = re.findall(pattern, page)

        print len(items)

        #for item in items:
            #print(time.strptime(item[0], "%Y-%m-%d"), string.atof(item[1]), string.atof(item[2]))
            #print(item[0], item[1], item[2])

        print items[1]


        with open('stocks.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(items)


        date = list()
        with open('stocks.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                #if reader.line_num == 1:
                #    continue
                date.append(row[0])
        #print date

        daily = list()
        with open('stocks.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                #if reader.line_num == 1:
                #    continue
                daily.append(string.atof(row[1]))
        #print daily


        accu = list()
        with open('stocks.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                #if reader.line_num == 1:
                #    continue
                accu.append(string.atof(row[2]))
        #print accu

        #print daily+accu

        df = pd.DataFrame(accu, index = date, columns=list('A')) #['Daily', 'Accu'])

        print df.describe()


spider = TtjjSpider()
spider.getContents("000697")
