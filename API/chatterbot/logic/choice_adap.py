# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter
import urllib2
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ChoiceAdapter(LogicAdapter):
    """
    The ChoiceAdapter evalutae the choice of deals.
    """

    def __init__(self, **kwargs):
        super(ChoiceAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'order' and 'buy' and 'temperature'.
        """
        words = ['#ch','choice']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, statement):
        from chatterbot.conversation import Statement

        if statement.text.startswith('#ch'):
            name = str(statement.text)
            n = name.split("/")

            choice = n[1]
            choice = int(choice)
            print choice
            from find_deal_adap import names, prices,item
            print item

            #list of item names and prices
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

            d_name =''
            d_price =''

            if(choice==1):
                d_name = d1
                d_price = p1
            elif(choice==2):
                d_name = d2
                d_price = p2
            elif(choice==3):
                d_name = d3
                d_price = p3
            elif(choice==4):
                d_name = od1
                d_price = op1
            elif(choice==5):
                d_name = od2
                d_price = op2
            else:
                d_name = od3
                d_price = op3

            d_price = d_price.encode('ascii','ignore')



            import sqlite3
            con1 = sqlite3.connect('item_list.db')
            con2 = sqlite3.connect('order_list.db')

            item_name=''
           # con1.text_factory = str
            cur = con1.execute("SELECT * FROM ITEMS WHERE NAME=?",(item,))



            for row in cur:
                item_name = row[1]
                print item_name+"aaaaaa"

                #q1= "UPDATE ITEMS SET NAME=?, RATE=? where NAME = ?;"
                con1.execute("update ITEMS set QTY_AVAIL=QTY_AVAIL+100 ,RATE=? where NAME = ?",(d_price,item_name,))
                con1.commit()
                print item_name +"  "+d_price

            if item_name=='':
                print "not found"
                qty = 50
                color =''
                #d_price = float(d_price)
                #con1.execute("SELECT  *")

                con1.execute("INSERT INTO ITEMS (PROD_ID,NAME,QTY_AVAIL,RATE,COLOR) VALUES (NULL,?,?,?,?)",(item,qty,d_price,color,))
                con1.commit()


            names=[]
            prices=[]
            item=[]

            response = Statement("You chose " + d_name+" "+d_price)
            response.confidence=1

        if statement.text.startswith('choice'):
            name = str(statement.text)
            n = name.split(" ")

            choice = n[1]
            print choice
            k = choice

            if (k=='one'):
                k=1
            elif (k=='two'):
                k=2
            elif (k=='three'):
                k=3
            elif (k=='four'):
                k=4
            elif (k=='five'):
                k=5
            elif (k=='six'):
                k=6



            from lang_adap import names, prices,item
            print item

            #list of item names and prices
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

            d_name =''
            d_price =''

            if(k==1):
                d_name = d1
                d_price = p1
            elif(k==2):
                d_name = d2
                d_price = p2
            elif(k==3):
                d_name = d3
                d_price = p3
            elif(k==4):
                d_name = od1
                d_price = op1
            elif(k==5):
                d_name = od2
                d_price = op2
            else:
                d_name = od3
                d_price = op3

            d_price = d_price.encode('ascii','ignore')



            import sqlite3
            con1 = sqlite3.connect('item_list.db')
            con2 = sqlite3.connect('order_list.db')

            item_name=''
           # con1.text_factory = str
            cur = con1.execute("SELECT * FROM ITEMS WHERE NAME=?",(item,))



            for row in cur:
                item_name = row[1]
                print item_name

                #q1= "UPDATE ITEMS SET NAME=?, RATE=? where NAME = ?;"
                con1.execute("update ITEMS set QTY_AVAIL=QTY_AVAIL+100 ,RATE=? where NAME = ?",(d_price,item_name,))
                con1.commit()
                print item_name +"  "+d_price

            if item_name=='':
                print "not found"
                qty = 50
                color =''
                #d_price = float(d_price)
                #con1.execute("SELECT  *")

                con1.execute("INSERT INTO ITEMS (PROD_ID,NAME,QTY_AVAIL,RATE,COLOR) VALUES (NULL,?,?,?,?)",(item,qty,d_price,color,))
                con1.commit()



            response = Statement("You chose " + d_name+" "+d_price)

            response.confidence = 1

        return response



