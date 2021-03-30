from functions.dat_worker import read_sales, write_sales
from functions.stock_management import check_exists, get_item, reduce_stock
from random import random
from datetime import datetime as dt

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