# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from pattern.en import singularize
import os
from gtts import gTTS
import pyttsx
import sys
sys.path.insert(0,"I:\Projects\finderbuddy")
from msgbox import threshold
from .logic_adapter import LogicAdapter

names=[]
prices=[]
item=''
class LanguageAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(LanguageAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'order' and 'buy' and 'temperature'.
        """
        words = ['go','NIL','reorder','check','checking','checked','ordering','update','last','first','how','available','decrease','increment','reduce',
        'increase','expect','expected','total','want','need','require','buy','best',
        'change','modify','cancel','help','previous','review','last','old','needing','updating'
        ,'updated','decreased','decreasing','incremented','incrementing','reducing','reduced',
        'increasing','increased','expecting','totalling','totalled','wanting','wanted','required'
        'requiring','buying','bought','changing','changed','modifying','modified','cancelling'
        ,'cancelled','helping','helped','reviewing','reviewed','find','finding','found']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, statement):
        from chatterbot.conversation import Statement

        import sqlite3
        con1 = sqlite3.connect('item_list.db')
        con2 = sqlite3.connect('order_list.db')

        from nltk import word_tokenize,pos_tag
        import nltk

        engine=pyttsx.init()

        noise_list=['availability','product','stock','place','us','delivery','date','value','bill','amount',"is","are","the","a","an","I","we","will","please","my","our",'sheets',
                    'of','from','We','to','order','what','for','was','quantity','number','request','on']
        def remove_noise(input_string):
            words=input_string.split()
            noise_free_words = [word for word in words if word not in noise_list] 
            noise_free_text = " ".join(noise_free_words) 
            return noise_free_text

        def pre_process(res):
            from nltk.stem.wordnet import WordNetLemmatizer
            from nltk.stem.porter import PorterStemmer 
            from pattern.en import pluralize,singularize
            lem=WordNetLemmatizer()
            stemmer=PorterStemmer()
            i=0
            for k in res:
                k.lower()
                k=str(k)
                print type(k)
                ml=[]
                ml.append(k)
                tagg=pos_tag(ml)
                if(tagg[0][1]=='VBG' or tagg[0][1]=='VBD' or tagg[0][1]=='VBN' or tagg[0][1]=='VBP'):
                    k=lem.lemmatize(k,pos='v')
                if(tagg[0][1]=='NNS'):
                    res[i]=singularize(k)    
                    #k=stemmer.stem(k)
                print k
                i=i+1
            return res    

        res1=remove_noise(str(statement.text)).split()
        res=pre_process(res1)

        if any(x in res for x in ['need','require','want']) and not any(x in res for x in ['how','cancel','change','modify','review','available','help','assist','increase','decrease','reduce','increment','buy','price','cost','value']):
            print "Need query"
            if(len(res)>2):
                ml=[]
                ml.append(res[2])
                tagg=pos_tag(ml)
            else:
                ml=[]
                ml.append(res[1])
                tagg=pos_tag(ml)    
            if not (len(res)>1 and (res[1].isdigit() or res[1] is not "") and (tagg[0][1]=='NNS' or tagg[0][1]=='NN' )):
                response=Statement("FinderBuddy understands that you're trying to order something\nBut FinderBuddy can't process this\nTry entering statements like-\n=>I want/need/require <quantity> <product>\n=>#place_order /product_name/quantity/color(if any)")
            print "Token 1 is "+res[1]
            if(res[1].isdigit()):
                qty=int(res[1])
                print "Quantity is "+str(qty)
                del(res[0])
                del(res[0])
                prod=clr=""
                print pos_tag(res)

                if(len(res)>1):
                    clr+=res[0]
                    prod+=res[1]
                else:
                    prod+=res[0]        
 
                print "Product is "+prod
                print "Color is "+clr
            else:
                qty=1
                print "Quantity is "+str(qty)
                del(res[0])
                prod=clr=""
                print pos_tag(res)
                for k in res:
                    ml=[]
                    ml.append(k)
                    tagg=pos_tag(ml)
                if(len(res)>1):
                    clr+=res[0]
                    prod+=res[1]
                else:
                    prod+=res[0]        
 
                print "Product is "+prod
                print "Color is "+clr
            if(clr==""):
                print "Here"
                cur1 = con1.execute("SELECT * FROM ITEMS where NAME=?", (prod,));
            else:
                print "There"
                cur1 = con1.execute("SELECT * FROM ITEMS where NAME=? and COLOR=?", (prod,clr));
            pid=nm=qt_av=rt=cl=0
            for row in cur1:
                pid = row[0]
                nm = row[1]
                qt_av = row[2]
                rt = row[3]
                cl = row[4]
            pr = rt * qty;
            qty_lft = qt_av-qty;
            if qt_av>=qty and qty_lft>=0:
                q2 = """INSERT INTO USER_ORDER (PROD,PROD_ID,QTY,RATE,COLOR,PRICE,PLACED_AT,DELIVER_AT)
                         VALUES ( ?, ?,?, ? ,? ,?,date('now','localtime'),date('now','localtime','+4 day'));"""
                q1= """UPDATE ITEMS SET QTY_AVAIL=? where NAME = ?;"""
                con2.execute(q2,(nm,pid,qty,rt,cl,pr))
                con1.execute(q1,(qty_lft,nm))
                con1.commit()
                con2.commit()

                q3 = "select seq from sqlite_sequence where name='USER_ORDER' "
                c = con2.execute(q3);
                odno = c.fetchone()[0]
                response=Statement("Order Successfully Placed with Order ID: "+str(odno)+". Use me Again :)")
                response.remove_response("Order Successfully Placed with Order ID: "+str(odno)+". Use me Again :)")
            else:
                response=Statement("Not Enough Quantity available.You can command FinderBuddy to find the best deals of "+clr+" "+prod+" for you")
                response.remove_response("Not Enough Quantity available.You can command FinderBuddy to find the best deals of "+clr+" "+prod+" for you")
            response.confidence=1
            return response        

    #CHANGE ORDER TAGS
        elif any(x in res for x in ['modify','change','update']) and not any(x in res for x in ['how']):
            print "Change query"
            if(res[0]=='want' or res[0]=='need'):
                del(res[0])    
            if not(len(res)==3 and (res[1].isdigit() or res[1]=='previous' or res[1]=='last' or res[1]=='first') and res[2].isdigit()):
                  response=Statement("FinderBuddy understands that you may be trying to change your order\nBut FinderBuddy can't really process this\nTry entering statements like-\n=>Change order <order id> to <new quantity>\n=>I want to change my previous/last/first order to <new quantity>")
                  response.confidence=1
                  return response
            if(res[1].isdigit()):
                ord_id=int(res[1])
            elif(res[1]=='previous' or res[1]=='last'):
                q="select ORDER_ID FROM  USER_ORDER LIMIT 1 OFFSET (select COUNT(*) FROM  USER_ORDER)-1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]
            elif(res[1]=='first'):
                q="select ORDER_ID FROM  USER_ORDER ORDER BY ORDER_ID ASC LIMIT 1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]  
            print "Order id is "+str(ord_id)
            q = "select * FROM  USER_ORDER WHERE ORDER_ID = ? "
            cur = con2.execute(q,(ord_id,))
            ck=1
            qty_chn=int(res[2])
            for row in cur:
                oid = row[0]
                print "Row is "+str(row[0])+" "+str(row[2])
                if oid==ord_id:
                    ck=0
                    pid = row[2]
                    qty = int(row[3])
                    rt = row[4]
                    abs = qty_chn-qty
                    print "Quantity to be changed is "+str(qty_chn)+" "+str(qty)
                    print "abs is "+str(abs)
                    pr = abs*rt
                    print "pr is "+str(pr)
                    q = "select * FROM  ITEMS WHERE PROD_ID = ? "
                    curr = con1.execute(q,(pid,))
                    for x in curr:
                        qt_av = x[2]
                        if qt_av>=abs:
                            q= "UPDATE ITEMS SET QTY_AVAIL = QTY_AVAIL - ? WHERE PROD_ID = ?"
                            con1.execute(q,(abs,pid))
                            con1.commit()
                            #print ord_id
                            #con2.execute(qx,(oid,prd,pid,qty,rt,cl,pr,pld,dld))
                            con2.execute("update USER_ORDER  SET QTY = QTY + ?, PRICE = PRICE + ? WHERE ORDER_ID = ?",(abs,pr,oid,))
                            con2.commit()
                            response=Statement("Order with Order Id: "+str(oid)+" succesfully changed with quantity: "+str(qty_chn))
                            response.remove_response("Order with Order Id: "+str(oid)+" succesfully changed with quantity: "+str(qty_chn))
                        else:
                            response = Statement("Sorry!! Not enough Quantity available to fulfil your need.")
                            response.remove_response("Sorry!! Not enough Quantity available to fulfil your need.")
            if ck==1:
                response=Statement("No order present with this order id.")
                response.remove_response("No order present with this order id.")
            response.confidence=1
            return response    


        #CANCEL ORDER TAGS---
        elif any(x in res for x in ['cancel']) and not any(x in res for x in ['how']):
            print "Cancel query"
            if(res[0]=='want' or res[0]=='need'):
                del(res[0])
            if not(len(res)==2 and (res[1].isdigit() or res[1]=='previous' or res[1]=='last' or res[1]=='first')):
                  response=Statement("FinderBuddy understands that you may be trying to cancel your order\nBut FinderBuddy can't really process this\nTry entering statements like-\n=>Cancel order <order id>\n=>I want to cancel my previous/last/first order")
                  response.confidence=1
                  return response
            if(res[1].isdigit()):
                ord_id=int(res[1])
            elif(res[1]=='previous' or res[1]=='last'):
                q="select ORDER_ID FROM  USER_ORDER LIMIT 1 OFFSET (select COUNT(*) FROM  USER_ORDER)-1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]
            elif(res[1]=='first'):
                q="select ORDER_ID FROM  USER_ORDER ORDER BY ORDER_ID ASC LIMIT 1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]    
            print "Order id is "+str(ord_id)
            q = "select * FROM  USER_ORDER WHERE ORDER_ID = ? "
            cur = con2.execute(q,(ord_id,))
            ck=1
            for row in cur:
                oid = row[0]
                if oid==ord_id:
                    ck=0
                    pid = row[2]
                    qty = row[3]
                    q = "DELETE FROM USER_ORDER WHERE ORDER_ID = ?"
                    con2.execute(q,(ord_id,))
                    con2.commit()
                    q= "UPDATE ITEMS SET QTY_AVAIL = QTY_AVAIL + ? WHERE PROD_ID = ?"
                    con1.execute(q,(qty,pid))
                    con1.commit()

            if ck==0:
                response=Statement("Order with Order Id:"+str(oid)+" succesfully cancelled")
                #engine.say("Order with Order Id:"+str(oid)+" succesfully cancelled")
                #engine.runAndWait()
                response.remove_response("Order with Order Id:"+str(oid)+" succesfully cancelled")
            else:
                response=Statement("No order present with this order id.")
                response.remove_response("No order present with this order id.")
            response.confidence=1
            return response    

        elif any(x in res for x in ['review','go']) and not any(x in res for x in ['how']):
            print "Review query" 
            if(res[0]=='want' or res[0]=='need'):
                del(res[0])
            if not(len(res)==2 and (res[1].isdigit() or res[1]=='previous' or res[1]=='last' or res[1]=='first')):
                response=Statement("FinderBuddy understands that you may be trying to review your order\nBut FinderBuddy can't really process this\nTry entering statements like-\n=>Review order <order id>\n=>I want to review my previous/last/first order")
                response.confidence=1
                return response
            if(res[1].isdigit()):
                ord_id=int(res[1])
            elif(res[1]=='previous' or res[1]=='last'):
                q="select ORDER_ID FROM  USER_ORDER LIMIT 1 OFFSET (select COUNT(*) FROM  USER_ORDER)-1" 
                cur= con2.execute(q)
                for row in cur:
                    ord_id=row[0]
            elif(res[1]=='first'):
                q="select ORDER_ID FROM  USER_ORDER ORDER BY ORDER_ID ASC LIMIT 1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]    
            print "Order id is "+str(ord_id)
            q = "select * FROM  USER_ORDER WHERE ORDER_ID = ? "
            cur = con2.execute(q,(ord_id,))
            ck=1
            for row in cur:
                oid = row[0]
                if oid:
                    ck=0
                    prd = row[1]
                    qt = row[3]
                    cl = row[5]
                    pr = row[6]
                    pld = row[7]
                    dld = row[8]
            if ck==0:
                response=Statement("Order Details:\n"+"Order Id:"+str(oid)+"\nProduct:"+str(prd)+"\nQuantity:"+str(qt)+"\nColor:"+str(cl)+"\nPrice:Rs."+str(pr)+"\nOrder Date:"+str(pld)+"\nExpected Delivery:"+str(dld)  \
                                        +"\nHope to see you again :)")
                response.remove_response("Order Details:\n"+"Order Id:"+str(oid)+"\nProduct:"+str(prd)+"\nQuantity:"+str(qt)+"\nColor:"+str(cl)+"\nPrice:Rs."+str(pr)+"\nOrder Date:"+str(pld)+"\nExpected Delivery:"+str(dld)  \
                                        +"\nHope to see you again :)")
            else:
                response=Statement("No order present with this order id.")
                response.remove_response("No order present with this order id.")
            response.confidence=1
            return response    


        elif any(x in res for x in ['buy','best','find']) and not any(x in res for x in ['price','how','available','total','expect','expected']):
            print "Find Deal query"  
            global item
            global names,prices
            if(res[0]=='want' or res[0]=='need'):
                del(res[0])    
            ml=[]
            ml.append(res[1])
            tagg=pos_tag(ml)    
            if not(len(res)>1 and (res[1].isdigit() or tagg[0][1]=='NN' or tagg[0][1]=='NNS' or tagg[0][1]=='JJ')):
                response=Statement("FinderBuddy understands that you're trying to order something from suppliers\nBut FinderBuddy can't really process this\nTry statements like-\n=>buy/best/find <quantity> <product>\n=>#find_deal /<product>")
                response.confidence=1
                return response
            if(res[1].isdigit()):
                qty=int(res[1])
                del(res[1])
            else:
                qty=1
            from bs4 import BeautifulSoup
            import urllib2
            item=""
            for i in range(1,len(res)-1):
                item=item+res[i]+" "            
            item+=res[len(res)-1]
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


        elif any(x in res for x in ['reorder']) and not any(x in res for x in ['how']):
            print "Need reorder based query" 
            if not (len(res)>1 and (res[1]=='previous' or res[1]=='last' or res[1]=='first' or res[1].isdigit())):
                response=Statement("FinderBuddy understands that you're trying to repeat an order\nBut FinderBuddy can't really process this\nTry statements like-\nreorder my previous/first/last order\n=>reorder order <order id>")
                response.confidence=1
                return response
            if(res[1].isdigit()):
                ord_id=int(res[1])
            elif(res[1]=='previous' or res[1]=='last'):
                q="select ORDER_ID FROM  USER_ORDER LIMIT 1 OFFSET (select COUNT(*) FROM  USER_ORDER)-1" 
                cur= con2.execute(q)
                for row in cur:
                    ord_id=row[0]
            elif(res[1]=='first'):
                q="select ORDER_ID FROM  USER_ORDER ORDER BY ORDER_ID ASC LIMIT 1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]    
            print "Order id is "+str(ord_id)
            q="select * FROM USER_ORDER WHERE ORDER_ID=?"
            cur = con2.execute(q,(ord_id,))
            ck=1
            for row in cur:
                oid = row[0]
                if oid:
                    ck=0
                    prod = row[1]
                    prod_id=row[3]
                    qty = row[3]
                    rate=row[4]
                    clr = row[5]
                    pr = row[6]

            if ck==0:
                if(clr==""):
                    print "Here"
                    cur1 = con1.execute("SELECT * FROM ITEMS where NAME=?", (prod,));
                else:
                    print "There"
                    cur1 = con1.execute("SELECT * FROM ITEMS where NAME=? and COLOR=?", (prod,clr));
                pid=nm=qt_av=rt=cl=0
                for row in cur1:
                    pid = row[0]
                    nm = row[1]
                    qt_av = row[2]
                    rt = row[3]
                    cl = row[4]
                pr = rt * qty;
                qty_lft = qt_av-qty;
                if qt_av>=qty and qty_lft>=0:
                    q2 = """INSERT INTO USER_ORDER (PROD,PROD_ID,QTY,RATE,COLOR,PRICE,PLACED_AT,DELIVER_AT)
                         VALUES ( ?, ?,?, ? ,? ,?,date('now','localtime'),date('now','localtime','+4 day'));"""
                    q1= """UPDATE ITEMS SET QTY_AVAIL=? where NAME = ?;"""
                    con2.execute(q2,(nm,pid,qty,rt,cl,pr))
                    con1.execute(q1,(qty_lft,nm))
                    con1.commit()
                    con2.commit()
                    q3 = "select seq from sqlite_sequence where name='USER_ORDER' "
                    c = con2.execute(q3);
                    odno = c.fetchone()[0]
                    response=Statement("Order Successfully Placed with Order ID: "+str(odno)+". Use me Again :)")
                    response.remove_response("Order Successfully Placed with Order ID: "+str(odno)+". Use me Again :)")
                else:
                    response=Statement("Not Enough Quantity available.You can command FinderBuddy to find the best deals of "+clr+" "+prod+" for you")
                    response.remove_response("Not Enough Quantity available.You can command FinderBuddy to find the best deals of "+clr+" "+prod+" for you")
                response.confidence=1
                return response            
            else:
                response=Statement("No order present with this order id.")
                response.remove_response("No order present with this order id.")
            response.confidence=1
            return response    


        elif any(x in res for x in ['total']):
            print "Total based query"
            if not (len(res)==2 and (res[1]=='previous' or res[1]=='last' or res[1]=='first' or res[1].isdigit())):
                response=Statement("FinderBuddy understands that you're trying to find the total value of an order\nBut FinderBuddy can't really process this\nTry statements like-\nfind total of my previous/first/last order\n=>total order <order id>")
                response.confidence=1
                return response
            if(res[1].isdigit()):
                ord_id=int(res[1])
            elif(res[1]=='previous' or res[1]=='last'):
                q="select ORDER_ID FROM  USER_ORDER LIMIT 1 OFFSET (select COUNT(*) FROM  USER_ORDER)-1" 
                cur= con2.execute(q)
                for row in cur:
                    ord_id=row[0]
            elif(res[1]=='first'):
                q="select ORDER_ID FROM  USER_ORDER ORDER BY ORDER_ID ASC LIMIT 1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]    
            print "Order id is "+str(ord_id)
            q="select * FROM USER_ORDER WHERE ORDER_ID=?"
            cur = con2.execute(q,(ord_id,))
            ck=1
            for row in cur:
                oid = row[0]
                if oid:
                    ck=0
                    qty = row[3]
                    rate=row[4]

            if ck==0:
                total=qty*rate
                response=Statement("Total value of order with order id "+str(ord_id)+" is "+unichr(163)+str(total))
                response.remove_response("Total value of order with order id "+str(ord_id)+" is "+unichr(163)+str(total))
                response.confidence=1
                return response            
            else:
                response=Statement("No order present with this order id.")
                response.remove_response("No order present with this order id.")
            response.confidence=1
            return response    


        elif any(x in res for x in ['expect','expected']) and not any(x in res for x in ['how']):
            print "Delivery date based query"
            if(res[0]=='find'):
                del(res[0])
            print res
            if not (len(res)>1 and (res[1]=='previous' or res[1]=='last' or res[1]=='first' or res[1].isdigit())):
                response=Statement("FinderBuddy understands that you're trying to find the delivery date of an order\nBut FinderBuddy can't really process this\nTry statements like-\nfind expected delivery date of my previous/first/last order/<order id>\n")
                response.confidence=1
                return response
            if(res[1].isdigit()):
                ord_id=int(res[1])
            elif(res[1]=='previous' or res[1]=='last'):
                q="select ORDER_ID FROM  USER_ORDER LIMIT 1 OFFSET (select COUNT(*) FROM  USER_ORDER)-1" 
                cur= con2.execute(q)
                for row in cur:
                    ord_id=row[0]
            elif(res[1]=='first'):
                q="select ORDER_ID FROM  USER_ORDER ORDER BY ORDER_ID ASC LIMIT 1" 
                cur = con2.execute(q)
                for row in cur:
                    ord_id=row[0]    
            print "Order id is "+str(ord_id)
            q="select * FROM USER_ORDER WHERE ORDER_ID=?"
            cur = con2.execute(q,(ord_id,))
            ck=1
            for row in cur:
                oid = row[0]
                if oid:
                    ck=0
                    dld=row[8]

            if ck==0:
                response=Statement("Delivery date of order with order id "+str(ord_id)+" is "+str(dld))
                response.remove_response("Delivery date of order with order id "+str(ord_id)+" is "+str(dld))
                response.confidence=1
                return response            
            else:
                response=Statement("No order present with this order id.")
                response.remove_response("No order present with this order id.")
            response.confidence=1
            return response   

        elif any(x in res for x in ['price','cost','value']) and not any(x in res for x in ['what']):
            print "Price based query"
            if(res[0]=='find'):
                del(res[0])
            print res
            if not (len(res)>1):
                response=Statement("FinderBuddy understands that you're trying to find the price of an item\nBut FinderBuddy can't really process this\nTry statements like-\nfind price of <item>")
                response.confidence=1
                return response
            if(len(res)>2):
                ml=[]
                ml.append(res[1])
                tagg=pos_tag(ml)
                clr=res[1]
                nl=[]
                nl.append(res[2])
                tagg1=pos_tag(nl)
                prd=res[2]
                q="select * FROM ITEMS WHERE COLOR=? AND NAME=?"
                cur = con1.execute(q,(res[1],res[2]))
            else:        
                ml=[]
                ml.append(res[1])
                tagg=pos_tag(ml)
                clr=""
                prd=res[1]
                q="select * FROM ITEMS WHERE NAME=?"
                cur = con1.execute(q,(res[1]))
            ck=1
            for row in cur:
                proid = row[0]
                if proid:
                    ck=0
                    rate=row[3]

            if ck==0:
                response=Statement("Price of "+str(clr)+" "+str(prd)+" is "+str(rate))
                response.confidence=1
                return response            
            else:
                response=Statement("Sorry-No item present with this name.You can command FinderBuddy to order it")
                response.remove_response("Sorry-No item present with this name.You can command FinderBuddy to order it")
            response.confidence=1
            return response   

        elif any(x in res for x in ['reduce','increase','decrease','increment']) and not any(x in res for x in ['how']):
            print "Update based query"
            print res 
            ml=[]
            ml.append(res[1])
            tagg=pos_tag(ml)
            nl=[]
            nl.append(res[2])
            tagg1=pos_tag(nl)
            if not(len(res)>1 and (tagg[0][1]=='NN' or tagg[0][1]=='NNS' or tagg[0][1]=='JJ') and (tagg1[0][1]=='NN' or tagg1[0][1]=='NNS' or res[2].isdigit())):
                response=Statement("FinderBuddy understands that you're trying to update the quantity of a product\nBut FinderBuddy can't really process this\nTry using statements like-\n=>reduce/increase/decrease/decrement/increment quantity of <color(if any)> <product> <new quantity>")
                response.confidence=1
                return response
            prod=""
            clr=""
            if ((tagg[0][1]=='NN' or tagg[0][1]=='NNS' or tagg[0][1]=='JJ') and (tagg1[0][1]=='NN' or tagg1[0][1]=='NNP')):
                clr=res[1]
                prod=res[2]
                qty_chn=int(res[3])
            else:
                prod=res[1]
                qty_chn=int(res[2])
            print "Color is "+clr
            print "Product is "+prod
            print "Quantity is "+str(qty_chn)
            q= "update ITEMS SET QTY_AVAIL=? where NAME = ? and COLOR=?;"
            con1.execute(q,(qty_chn,prod,clr))
            con1.commit()
            response=Statement("Updated item "+str(clr)+" "+str(prod)+" succesfully to "+str(qty_chn))
            response.confidence=1
            return response

        elif any(x in res for x in ['available']) and not any(x in res for x in ['how','check']):
            print "Retrieval based query" 
            if(res[0]=='find'):
                del(res[0])
            ml=[]
            ml.append(res[1])
            tagg=pos_tag(res[1]) 
            if not(len(res)>1 and (tagg[0][1]=='NN' or tagg[0][1]=='NNS' or tagg[0][1]=='JJ')):
                response=Statement("FinderBuddy understands that you're trying to find the available quantity of an item\nBut FinderBuddy can't really process this\nTry using statements like-\n=>find available quantity of <color(if any)> <product>")
                response.confidence=1
                return response
            clr=prod=""    
            if(len(res)>2):
                nl=[]
                nl.append(res[2])
                tagg1=pos_tag(nl)
                clr=res[1]
                prod=res[2]
            else:
                prod=res[1]
            print "Color is "+clr 
            print "Product is "+prod 
            qty=""
            if(clr==""):
                q= "select * FROM ITEMS WHERE NAME=?" 
                cur1=con1.execute(q,(prod,))
                for row in cur1:
                    qty=row[2]
                if(qty==""):
                    response=Statement("No such product exists")
                else:        
                    response=Statement("Available quantity of "+str(clr)+" "+str(prod)+" is "+str(qty))
                response.confidence=1
                return response
            else:
                q="select * FROM ITEMS WHERE NAME=? and COLOR=?"
                cur1=con1.execute(q,(prod,clr,))
                for row in cur1:
                    qty=row[2]
                if(qty==""):
                    response=Statement("No such product exists")
                else:      
                    response=Statement("Available quantity of "+str(clr)+" "+str(prod)+" is "+str(qty))
                response.confidence=1
                return response


        elif any(x in res for x in ['check']) and not any(x in res for x in ['how']):
            print "Threshold based query"
            print "Threshold is "+str(threshold)
            q="select NAME,COLOR FROM ITEMS WHERE QTY_AVAIL<=? "
            cur1=con1.execute(q,(threshold,))
            a="Items which are short are\n"
            i=0
            for row in cur1:
                a=a+row[1]+" "
                a+=row[0]+"\n"
                i=i+1
            if(i==0):
                response=Statement("Relax-no items are short!! :)")
            else:        
                response=Statement(a)
            response.confidence=1
            return response             

        elif any(x in res for x in ['help','how']):
            print "Help needed" 
            a = "To place an Order, please type:  #place_order /product_name/quantity/color(if any)"
            b = "To change an Order, please type:  #change_order /order_id/quantity(to change)"
            c = "To review an Order, please type:  #review_order /order_id"
            d = "To cancel an Order, please type:  #cancel_order /order_id"
            g = "To know your previous Order, please type:  #previous_order"
            k = "To check what all items are about to finish, please type: #check"
            e = "For help, please type:  #help"
            g = "Other than this,you can also just type in the keywords of your query "
            h = "like want/need/find/reorder along with the order id and product name"
            f = "pattern is sensitive and use of small case letters is recommended\n"
            i = "Hope this helped\nIn case of further queries,please feel free to contact the developers "
            j = "\n\tAnushka Chawla->anushkachawla@zhcet.ac.in\n\tAman Varshney->amanvars@zhcet.ac.in"
            response = Statement(a+"\n"+b+"\n"+c+"\n"+d+"\n"+g+"\n"+k+"\n"+e+"\n"+"\n"+g+h+f+"\n\n"+i+j)
            response.confidence=1
            response.remove_response(a+"\n"+b+"\n"+c+"\n"+d+"\n"+g+"\n"+k+"\n"+e+"\n"+"\n"+g+h+f+"\n\n"+i+j)
            return response

        elif any(x in res for x in ['NIL']):
            print 'Empty input'
            response=Statement("Sorry-I couldn't understand what you just said.You can try repeating your order or just type it in") 
            response.confidence=1
            return response   


        response=Statement("Processing your request")
        response.confidence = 1
        return response