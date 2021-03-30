from functions.dat_worker import read_items, write_items

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