from functions.dat_worker import read_sales, read_items
from datetime import datetime as dt

def cash_memo():
    billno = int(input("Enter Cash Memo Number : "))
    all_sales = read_sales()
    for i in all_sales["sales"]:
        if i["number"] == billno:
            cash_memo = i
            print(f'''
================================================================================
Date : {cash_memo["date"]}                Cash Memo Number : {cash_memo["number"]}
================================================================================

S. No.     Item Code                 Particular           Rate    Quantity  Amt
''')
            for j in cash_memo["items"]:
                print(f"{j['sno']}        {j['code']}         {j['particular']}         Rs. {j['rate']}  {j['quantity']}  Rs. {j['amount']}")
            print(f'''
================================================================================
Grand Total                                                 Rs. {cash_memo["total"]}
================================================================================''')
            print("\n"*3)
            return True
    print("Cash Memo Not Found. Invalid Number :(")

def daily_sales_report():
    while 1:
        try:
            date = dt.strptime(input("ENTER DATE AS 'DD/MM/YYYY' (WITHOUT QUOTES) : "),"%d/%m/%Y")
            break
        except:
            print("INVALID.")
            continue
    all_sales = read_sales()
    items_list = []
    amount = 0
    for i in all_sales["sales"]:
        if dt.strptime(i["date"], "%d/%m/%y %H:%M:%S").strftime("%d/%m/%Y") == date.strftime("%d/%m/%Y"):
            for x in i["items"]:
                item_added = False
                for z in items_list:
                    if z["name"] == x["particular"]:
                        z["amount"] += x["amount"]
                        item_added = True
                if item_added == False:
                    items_list.append({"name":x["particular"],"amount":x["amount"]})
            amount += i["total"]
    print(f"""
==========================================================
DAILY SALES REPORT FOR DAY : {date.strftime("%d/%m/%Y")}
==========================================================

LIST OF ITEMS SOLD
==================""")
    for i in items_list:
        print(f"{i['name']}  -  Rs. {i['amount']}")
    print(f"""

==================

TOTAL AMOUNT EARNT : Rs. {amount}""")

def monthly_sales_report():
    while 1:
        try:
            date = dt.strptime(input("ENTER MONTH AS 'MM/YYYY' (WITHOUT QUOTES) : "),"%m/%Y")
            break
        except:
            print("INVALID.")
            continue
    all_sales = read_sales()
    items_list = []
    amount = 0
    for i in all_sales["sales"]:
        if dt.strptime(i["date"], "%d/%m/%y %H:%M:%S").strftime("%m/%Y") == date.strftime("%m/%Y"):
            for x in i["items"]:
                item_added = False
                for z in items_list:
                    if z["name"] == x["particular"]:
                        z["amount"] += x["amount"]
                        item_added = True
                if item_added == False:
                    items_list.append({"name":x["particular"],"amount":x["amount"]})
            amount += i["total"]
    print(f"""
==========================================================
MONTHLY SALES REPORT FOR MONTH : {date.strftime("%B, %Y")}
==========================================================

LIST OF ITEMS SOLD
==================""")
    for i in items_list:
        print(f"{i['name']}  :  Rs. {i['amount']}")
    print(f"""

==================

TOTAL AMOUNT EARNT : Rs. {amount}""")

def yearly_sales_report():
    while 1:
        try:
            date = dt.strptime(input("ENTER YEAR AS 'YYYY' (WITHOUT QUOTES) : "),"%Y")
            break
        except:
            print("INVALID.")
            continue
    all_sales = read_sales()
    items_list = []
    amount = 0
    for i in all_sales["sales"]:
        if dt.strptime(i["date"], "%d/%m/%y %H:%M:%S").strftime("%Y") == date.strftime("%Y"):
            for x in i["items"]:
                item_added = False
                for z in items_list:
                    if z["name"] == x["particular"]:
                        z["amount"] += x["amount"]
                        item_added = True
                if item_added == False:
                    items_list.append({"name":x["particular"],"amount":x["amount"]})
            amount += i["total"]
    print(f"""
==========================================================
MONTHLY SALES REPORT FOR YEAR : {date.strftime("%Y")}
==========================================================

LIST OF ITEMS SOLD
==================""")
    for i in items_list:
        print(f"{i['name']}  :  Rs. {i['amount']}")
    print(f"""

==================

TOTAL AMOUNT EARNT : Rs. {amount}""")

def item_wise_report():
    all_sales = read_sales()
    items_list = []
    amount = 0
    for i in all_sales["sales"]:
        for x in i["items"]:
            item_added = False
            for z in items_list:
                if z["name"] == x["particular"]:
                    z["amount"] += x["amount"]
                    item_added = True
            if item_added == False:
                items_list.append({"name":x["particular"],"amount":x["amount"]})
        amount += i["total"]
    print("""
==========================================================
ITEM-WISE SALES REPORT
==========================================================

LIST OF ITEMS SOLD
==================""")
    for i in items_list:
        print(f"{i['name']}  :  Rs. {i['amount']}")
    print(f"""

==================

TOTAL AMOUNT EARNT : Rs. {amount}""")

def items_available():
    items = read_items()
    print("""
==========================================================
LIST OF ITEMS AVAILABLE / STOCK REPORT
==========================================================

CODE      PARTICULAR              QUANTITY    AVAILABILITY
""")
    for i in items["items"]:
        print(i["code"],i["particular"],i["quantity"],end=" ")
        if int(i["quantity"])>=1:
            print("  AVAILABLE")
        else:
            print("  UNAVAILABLE")
        print("\n")

def order_stock_list():
    items = read_items()
    order_list = []
    print("""
==========================================================
LIST OF ITEMS<20 / TO ORDER
==========================================================

CODE      PARTICULAR              QUANTITY
""")
    for i in items["items"]:
        if int(i["quantity"])<20:
            print(i["code"],i["particular"],i["quantity"])