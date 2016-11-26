__author__ = 'DCD'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
# import urllib.request

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
        print
        url

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


spider = Spider()
spider.getContents(2)