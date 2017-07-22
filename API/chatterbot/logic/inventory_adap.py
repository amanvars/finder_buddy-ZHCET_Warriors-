from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter


class InventoryAdapter(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.
    """

    def __init__(self, **kwargs):
        super(InventoryAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'order' and 'buy' and 'temperature'.
        """
        words = ['#place_order', '#review_order', '#change_order','#cancel_order','#help','#previous_order']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, statement):
        from chatterbot.conversation import Statement


        import sqlite3
        con1 = sqlite3.connect('item_list.db')
        con2 = sqlite3.connect('order_list.db')

       # name = str(statement.text)
       # n = name.split("/")
        if statement.text.startswith('#place_order'):
            name = str(statement.text)
            n = name.split("/")

            x = Statement(statement.text)
            x.remove_response(statement.text)
            if len(n)>2:
                prod = str(n[1]).lower()
                qty = int(n[2])
                clr=""
                cur1 = con1.execute("SELECT * FROM ITEMS where NAME=?", (prod,));
                if len(n)==4:
                    clr = str(n[3])
                    cur1 = con1.execute("SELECT * FROM ITEMS where NAME=? and COLOR=?", (prod,clr));

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
                    response=Statement("Not Enough Quantity available.Try Again!!")
                    response.remove_response("Not Enough Quantity available.Try Again!!")
                #print (prod)
                #print (qty)
                #print (clr)
            else:
                response = Statement("Something is wrong in your query!!")
                response.remove_response("Something is wrong in your query!!")

#            print(name)
        elif statement.text.startswith('#review_order'):
            name = str(statement.text)
            n = name.split("/")
            x = Statement(statement.text)
            x.remove_response(statement.text)
            if len(n)>1:
                ord_id = int(n[1])
                #print ord_id
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
            else:
                response = Statement("Something is wrong in your query!!")
                response.remove_response("Something is wrong in your query!!")

        elif statement.text.startswith('#cancel_order'):
            name = str(statement.text)
            n = name.split("/")

            x = Statement(statement.text)
            x.remove_response(statement.text)

            if len(n)>1 and n[1]!=" ":
                ord_id  = int(n[1])
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
                     response.remove_response("Order with Order Id:"+str(oid)+" succesfully cancelled")
                else:
                     response=Statement("No order present with this order id.")
                     response.remove_response("No order present with this order id.")
            else:
                response = Statement("Something is wrong in your query!!")
                response.remove_response("Something is wrong in your query!!")


        elif statement.text.startswith('#change_order'):
            name = str(statement.text)
            n = name.split("/")

            x = Statement(statement.text)
            x.remove_response(statement.text)
            if len(n)>2:
                ord_id  = int(n[1])
                qty_chn = int(n[2])
                q = "select * FROM  USER_ORDER WHERE ORDER_ID = ? "
                cur = con2.execute(q,(ord_id,))
                ck=1
                for row in cur:
                    oid = row[0]
                    if oid==ord_id:
                        ck=0
                        pid = row[2]
                        qty = row[3]
                        rt = row[4]

                        abs = qty_chn-qty
                        #print abs
                        pr = abs*rt
                       # print pr

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
            else:
                response = Statement("Something is wrong in your query!!")
                response.remove_response("Something is wrong in your query!!")

        elif statement.text.startswith('#previous_order'):
           #name = str(statement.text)
           # n = name.split("/")
            x = Statement(statement.text)
            x.remove_response(statement.text)

            q = "select COUNT(*) FROM  USER_ORDER "
            cur = con2.execute(q)
            num = cur.fetchone()[0]
            ck=0
            if num<1:
                ck=1
            else:
                q = "select ORDER_ID, PROD FROM  USER_ORDER LIMIT 1 OFFSET (select COUNT(*) FROM  USER_ORDER)-1"
                cur = con2.execute(q)
                s = "Your last order details is as follows:"
                s2 = "\nOrder Id \t\tProduct\n"


                for row in cur:
                    ck=2
                    oid = row[0]
                    prd = row[1]
                    response=Statement(s+s2+str(oid)+"\t\t\t"+prd)
                    response.remove_response(s+s2+str(oid)+"\t\t\t"+prd)

            if ck==1:
                response=Statement("Seems, you did not place any order")
                response.remove_response("Seems, you did not place any order")


        elif statement.text.startswith('#help'):

            x = Statement(statement.text)
            x.remove_response(statement.text)

            a = "To place an Order, please type:  #place_order /product_name/quantity/color(if any)"
            b = "To change an Order, please type:  #change_order /order_id/quantity(to change)"
            c = "To review an Order, please type:  #review_order /order_id"
            d = "To cancel an Order, please type:  #cancel_order /order_id"
            g = "To know your previous Order, please type:  #previous_order"
            e = "For help, please type:  #help"
            f = "pattern is sensitive"


            response = Statement(a+"\n"+b+"\n"+c+"\n"+d+"\n"+g+"\n"+e+"\n"+f)
            response.remove_response(a+"\n"+b+"\n"+c+"\n"+d+"\n"+g+"\n"+e+"\n"+f)

        response.confidence = 1

        return response
