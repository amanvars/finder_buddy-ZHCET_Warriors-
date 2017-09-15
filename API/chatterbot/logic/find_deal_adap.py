# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

names = []
prices = []


class FindDealAdapter(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.
    """

    def __init__(self, **kwargs):
        super(FindDealAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'order' and 'buy' and 'temperature'.
        """
        words = ['#find_deal']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, statement):
        from chatterbot.conversation import Statement
        global names,prices

        if statement.text.startswith('#find_deal'):
            name = str(statement.text)
            n = name.split("/")
            global item
            item = n[1]
            print item
            search1 = item.replace(" ","-")
            search2 = item.replace(" ","+")
            url1='http://www.kelkoo.co.uk/kss-'+search1+'.html'
            url2='https://www.mintprice.com/c/search?show=16&sortby=price_low_to_high&page=1&search='+search2
            query1=urllib2.urlopen(url1)
            query2=urllib2.urlopen(url2)
            soup1=BeautifulSoup(query1)
            soup2=BeautifulSoup(query2)
            names=[]
            prices=[]
            for row in soup1.find_all('h3', attrs={'class': 'result-title'}):
                names.append(row.span.text)
            for row in soup1.find_all('p',attrs={'class':'price'}):
                prices.append(row.strong.text)    
            print names
            print prices

            for row in soup2.find_all('div',attrs={'class':'caption'}):
                names.append(row.h3.text)
            for row in soup2.find_all('p',attrs={'class':'price'}):
                prices.append(row.strong.text)
            print names
            print prices        
            d1 =  names[0].decode().encode('utf-8')
            p1 =  prices[0].strip().decode().encode('utf-8')
            d2 =  names[1].decode().encode('utf-8')
            p2 =  prices[1].strip().decode().encode('utf-8')
            d3 =  names[2].decode().encode('utf-8')
            p3 =  prices[2].strip().decode().encode('utf-8')
            od1 =  names[len(names)-3].decode().encode('utf-8')
            op1 =  prices[len(prices)-3].strip().decode().encode('utf-8')
            od2 =  names[len(names)-2].decode().encode('utf-8')
            op2 =  prices[len(prices)-2].strip().decode().encode('utf-8')
            od3 =  names[len(names)-1].decode().encode('utf-8')
            op3 =  prices[len(prices)-1].strip().decode().encode('utf-8')
            response = Statement(u"Below are some suggestions\n\t"+d1+" || "+p1+"\n\t"+d2+" || "+p2+"\n\t"+d3+" || "+p3+"\n\t"+od1+" || "+op1+"\n\t"+od2+" || "+op2+"\n\t"+od3+" || "+op3)
            response.confidence = 1
            return response



