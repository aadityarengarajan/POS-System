from pickle import dump,load
from random import random
from datetime import datetime as dt
from os import listdir


if "items.dat" not in listdir():
    with open("items.dat","wb"):
        pass

if "sales.dat" not in listdir():
    with open("sales.dat","wb"):
        pass


def read_items():
    objects = []
    with (open("items.dat", "rb")) as openfile:
        while True:
            try:
                objects.append(load(openfile))
            except EOFError:
                break
    try:
        return objects[0]
    except IndexError:
        return {"items":[]}

def write_items(data):
    with open("items.dat","wb") as f:
        dump(data,f)
    return True

def read_sales():
    objects = []
    with (open("sales.dat", "rb")) as openfile:
        while True:
            try:
                objects.append(load(openfile))
            except EOFError:
                break
    try:
        return objects[0]
    except IndexError:
        return {"sales":[]}

def write_sales(data):
    with open("sales.dat","wb") as f:
        dump(data,f)
    return True


def add_item():
    particular = input("PARTICULAR : ")
    rate = float(input("RATE (in Rupees) : "))
    qt = 0
    while qt<=0:
            qt = float(input("QUANTITY (PCS/UNITS) : "))
            if qt<=0:
                print("QUANTITY MUST BE MORE THAN 0")
    items = read_items()
    codes = []
    for i in items["items"]:
        codes.append(int(i["code"]))
    try:
        code = (max(codes)+1)
    except ValueError:
        code = 1
    items["items"].append({"code":code,
                           "particular":particular,
                           "rate":rate,
                           "quantity":qt})
    write_items(items)
    i = {"code":code,
         "particular":particular,
         "rate":rate,
         "quantity":qt}
    print(f'''

ITEM CODE {i["code"]}
PARTICULAR : {i["particular"]}
RATE : {i["rate"]}
CURRENT QUANTITY : {i["quantity"]}
''')
    print("\n\nNEW ITEM ADDED.")

def add_stock():
    code = int(input("ITEM CODE : "))
    items = read_items()
    for i in items["items"]:
        if int(i["code"])==int(code):
            print(f'''ITEM CODE {i["code"]}
PARTICULAR : {i["particular"]}
RATE : {i["rate"]}
CURRENT QUANTITY : {i["quantity"]}
''')
            qty = -1
            while qty<0:
                qty = float(input("ENTER ADDITIONAL QUANTITY (PCS/UNITS) : "))
                if qty<0:
                    print("QUANTITY MUST BE MORE THAN OR EQUAL TO 0")
            print("\n"*2)
            print(f'''ITEM CODE {i["code"]}
PARTICULAR : {i["particular"]}
RATE : {i["rate"]}
CURRENT QUANTITY : {i["quantity"]}
NEW QUANTITY : {qty}

TOTAL QUANTITY : {i["quantity"]+qty}
''')
            if input("ARE YOU SURE YOU WOULD LIKE TO AMEND CHANGES? (Y/N [Default : Y]) : ") in "Yy":
                new_item = ({"code":i["code"],
                             "particular":i["particular"],
                             "rate":i["rate"],
                             "quantity":i["quantity"]+qty})
                items["items"].remove(i)
                items["items"].append(new_item)
                write_items(items)
                print("\n\nSTOCK INCREASED.")
                
                return True
            else:
                print("\n\nSTOCK UNCHANGED.")
                return True
    print("\n\nITEM NOT FOUND.")
    return False

def reduce_stock(code,qt):
    items = read_items()
    for i in items["items"]:
        if int(i["code"])==int(code):
            new_item = ({"code":i["code"],
                         "particular":i["particular"],
                         "rate":i["rate"],
                         "quantity":i["quantity"]-qt})
            items["items"].remove(i)
            items["items"].append(new_item)
            write_items(items)
            return True
    return False

def check_exists(code):
    items = read_items()
    code_exists = False
    stock_exists = False
    stock_pcs = 0
    for i in items["items"]:
        if int(i["code"])==int(code):
            code_exists = True
            if int(i["quantity"])>=1:
                stock_exists = True
            stock_pcs = int(i["quantity"])
    return {"code_exists":code_exists,"stock_exists":stock_exists,"stock_pcs":stock_pcs}

def get_item(code):
    items = read_items()
    code_exists = False
    stock_exists = False
    for i in items["items"]:
        if int(i["code"])==int(code):
            return i
    return False


def code_gen():
    exists = True
    while exists == True:
        code = int(random()*(10**8))
        exists = check_exists(code)["code_exists"]
    return code

def bill():
    datetime = dt.now().strftime("%d/%m/%y %H:%M:%S")
    cash_memo = {"date":datetime, "number":code_gen()}
    purchased_items = []
    c = 0
    total_amt = 0
    while 1:
        if input("ADD ANOTHER ITEM? (Y/N [Default : Y]) : ") in "Yy":
            print('''
ADD ITEM
========

    ''')
            item = int(input("CODE : "))
            if check_exists(item)["code_exists"] == False:
                print("Code doesn't exist :(")
                continue
            elif check_exists(item)["stock_exists"] == False:
                print("Item is out of stock :(")
                continue
            else:
                qt = 0
                while qt<=0 or int(qt)>int(check_exists(item)["stock_pcs"]):
                    qt = float(input("QUANTITY (PCS/UNITS) : "))
                    if qt<=0:
                        print("QUANTITY MUST BE MORE THAN 0")
                    if int(qt)>int(check_exists(item)["stock_pcs"]):
                        print(f'THERE ARE ONLY {check_exists(item)["stock_pcs"]} PCS/UNITS IN STOCK. PLEASE ENTER A NUMBER LESSER THAN THE SAME.')
                c += 1
                item = get_item(item)
                code = item["code"]
                particular = item["particular"]
                rate = item["rate"]
                quantity = qt
                amount = rate*qt
                purchased_items.append({"sno":c,
                                        "code":code,
                                        "particular":particular,
                                        "rate":rate,
                                        "quantity":quantity,
                                        "amount":amount})
                total_amt += amount             
        else:
            break
    cash_memo.update({"items":purchased_items,"total":total_amt})
    print(f'''
================================================================================
Date : {cash_memo["date"]}                Cash Memo Number : {cash_memo["number"]}
================================================================================

S. No.     Item Code                 Particular           Rate    Quantity  Amt
''')
    for i in cash_memo["items"]:
        print(f"{i['sno']}        {i['code']}         {i['particular']}         Rs. {i['rate']}  {i['quantity']}  Rs. {i['amount']}")
    print(f'''
================================================================================
Grand Total                                                 Rs. {cash_memo["total"]}
================================================================================''')
    print("\n"*3)

    if input("ARE YOU SURE YOU WOULD LIKE TO COMPLETE BILLING? (Y/N [N to Cancel Bill, Default : Y]) : ") in "Yy":
        for i in cash_memo["items"]:
            reduce_stock(i["code"],i["quantity"])
        current_sales = read_sales()
        current_sales["sales"].append(cash_memo)
        write_sales(current_sales)
        print("\n\nBILLING COMPLETE.")

    else:
        print("\n\nBILLING CANCELED.")


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



menu = """
==========================================
SALES MANAGEMENT SYSTEM FOR STORES
==========================================

WHAT WOULD YOU LIKE TO DO?

(1) ADD NEW ITEM TO INVENTORY
(2) ADD NEW STOCK TO INVENTORY
(3) PERFORM BILLING FOR CUSTOMER
(4) VIEW CASH MEMO GIVEN CODE
(5) VIEW SALES REPORT(S)
(6) VIEW LIST OF AVAILABLE ITEMS
(7) GENERATE ORDER LIST FOR ITEMS WHERE STOCK < 20
(0) EXIT

YOUR CHOICE : """

report_menu = """
==========================================
VIEW SALES REPORT(S)
==========================================

WHAT TYPE OF SALES REPORT WOULD YOU LIKE TO VIEW?

(1) DAILY SALES REPORT
(2) MONTHLY SALES REPORT
(3) YEARLY SALES REPORT
(4) ITEM-WISE SALES REPORT
(0) BACK TO MAIN MENU

YOUR CHOICE : """

while True:
	while 1:
		try:
			ch = int(input(menu))
			break
		except:
			print("PLEASE ENTER A VALID INTEGER")
			continue
	if ch==1:
		add_item()
		print("\n"*2)
	elif ch==2:
		add_stock()
		print("\n"*2)
	elif ch==3:
		bill()
		print("\n"*2)
	elif ch==4:
		cash_memo()
		print("\n"*2)
	elif ch==5:
		while 1:
			try:
				ch = int(input(report_menu))
				break
			except:
				print("PLEASE ENTER A VALID INTEGER")
				continue
		if ch==1:
			daily_sales_report()
		elif ch==2:
			monthly_sales_report()
		elif ch==3:
			yearly_sales_report()
		elif ch==4:
			item_wise_report()
		print("\n"*2)
	elif ch==6:
		items_available()
		print("\n"*2)
	elif ch==7:
		order_stock_list()
		print("\n"*2)
	elif ch==0:
		break