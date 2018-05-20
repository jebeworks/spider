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
import matplotlib.pyplot as plt
import sys
import datetime




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

    def getFirstPage(self, code, per):
        url = 'http://fund.eastmoney.com'
        #print url

        #request = urllib.request.Request(url)
        #response = urllib.request.urlopen(request)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        return response.read()

    def getFirstPageContents(self, code):
        page = self.getFirstPage(code, 1)
        #print page
        #pattern = re.compile('var apidata={ content:"<table class=.*?>.*?</table>",records:(.*?),pages:.*?,curpage:.*?};',re.S)
        #pattern = re.compile('<div class="wrapper fund_margin10">.*?class="fname">(.*?)</a>.*?fc=(.*?)".*?<a .*?class="fname">(.*?)</a>.*?fc=(.*?)".*?class="fname">(.*?)</a>.*?fc=(.*?)".*?<div class="dataShow-item dataShow-border">', re.S)
        #pattern = re.compile('<!--published at (.*?) (.*?)-->.*?<div class="wrapper fund_margin10">.*?class="fname">(.*?)</a>.*?fc=(.*?)".*?<a .*?class="fname">(.*?)</a>.*?fc=(.*?)".*?class="fname">(.*?)</a>.*?fc=(.*?)".*?<div class="dataShow-item dataShow-border">', re.S)

        datetimepattern = '<!--published at (.*?) (.*?)-->'
        highpattern = '.*?<div class="wrapper fund_margin10">.*?class="fname">(.*?)</a>.*?fc=(.*?)".*?<a .*?class="fname">(.*?)</a>.*?fc=(.*?)".*?class="fname">(.*?)</a>.*?fc=(.*?)"'
        goodpattern = '.*?<div class="dataShow-item dataShow-border">.*?class="fname">(.*?)</a>.*?fc=(.*?)".*?<a .*?class="fname">(.*?)</a>.*?fc=(.*?)".*?class="fname">(.*?)</a>.*?fc=(.*?)"'
        #endpattern = '.*?<div class="dataShow-item dataShow-border">'
        hotpattern='.*?<div class="dataShow-item dataShow-border">.*?class="fname">(.*?)</a>.*?class="fname">(.*?)</a>.*?class="fname">(.*?)</a>.*?class="fname">(.*?)</a>.*?class="fname">(.*?)</a>'
        endpattern = '.*?<div class="dataShow-item">'
        pattern = re.compile(datetimepattern+highpattern+goodpattern+hotpattern+endpattern, re.S)


        items = re.findall(pattern, page)
        #print items

        with open('ttjj.csv', 'a+') as f:
            writer = csv.writer(f)
            #write.writerows(['date' 'Adj' 'Adj'])

            #mydate = time.strftime('%Y-%m-%d')
            #writer.writerows(datetime)
            #items.append(''.join(mydate))
            writer.writerows(items)

        #print items
        print 'Done!'
        f.close()

#python -m py_compile test.py
#mv test.pyc test0520a.pyc
#python test0520a.pyc


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
        #pattern=re.compile(
        #    '<tr><td>(.*?)</td><td class=.*?>(.*?)</td><td class=.*?>.*?</td><td class=.*?>.*?%</td>.*?</tr>',re.S)

        items = re.findall(pattern, page)

        items.reverse()

        print len(items)

        #for item in items:
            #print(time.strptime(item[0], "%Y-%m-%d"), string.atof(item[1]), string.atof(item[2]))
            #print(item[0], item[1], item[2])

        print items[0]


        with open('stocks.csv', 'w') as f:
            writer = csv.writer(f)
            #write.writerows(['date' 'Adj' 'Adj'])
            writer.writerows(items)

        date = list()
        with open('stocks.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                #if reader.line_num == 1:
                #    continue
                date.append(row[0])
        #print date

        price = list()
        with open('stocks.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                #if reader.line_num == 1:
                #    continue
                price.append(string.atof(row[1]))
        #print daily

        rtn = list()
        with open('stocks.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                #if reader.line_num == 1:
                #    continue
                rtn.append(string.atof(row[2]))
        #print accu

        df = pd.DataFrame(price , index = date, columns=list('A')) #['price', 'rtn'])



        print df.describe()

        plt.show(df.plot())

#df=pd.read_csv("stocks.csv")
#print df.describe()
#plt.show(df.plot())

spider = TtjjSpider()
#spider.getContents("001878")  #001878
spider.getFirstPageContents("001878")  #001878


#>>> import test
#>>> spider=test.TtjjSpider()
#>>> spider.getContents("001878")


#sys.exit()

#f = pd.read_csv("./stocks.csv")
#f.values
#f.ix[:,1]
#f.ix[:,1].valuesc
#p=f.ix[:,1]
#q=p.shift(-1)
#(q-p)/p
#t=f.ix[:,0]
#r=(q-p)/p
#df = pd.DataFrame(r , index = t, columns=list('return'))




