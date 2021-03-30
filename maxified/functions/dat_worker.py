from pickle import dump,load
from os import listdir

if "items.dat" not in listdir("./data"):
    with open("items.dat","wb"):
        pass

if "sales.dat" not in listdir("./data"):
    with open("sales.dat","wb"):
        pass

def read_items():
    objects = []
    with (open("./data/items.dat", "rb")) as openfile:
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
    with open("./data/items.dat","wb") as f:
        dump(data,f)
    return True

def read_sales():
    objects = []
    with (open("./data/sales.dat", "rb")) as openfile:
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
    with open("./data/sales.dat","wb") as f:
        dump(data,f)
    return True


'''
SAMPLE CONTENT OF BINARY FILES

'sales.dat'
-----------

{"sales":[{"date":"17/03/2007 18:07:23","number":"23145","items":[
            {"sno":"1","code":"001","particular":"PEN","rate":"40.00","quantity":"75","amount":"3000"},
            {"sno":"2","code":"002","particular":"PENCIL","rate":"5.00","quantity":"100","amount":"500"},
            {"sno":"3","code":"003","particular":"CARBON PAPER","rate":"50.00","quantity":"20","amount":"1000"}
            ],
            "total":"4500"},
        {"date":"17/03/2007","number":"14552","items":[
            {"sno":"1","code":"001","particular":"PEN","rate":"40.00","quantity":"75","amount":"3000"},
            {"sno":"2","code":"002","particular":"PENCIL","rate":"5.00","quantity":"100","amount":"500"},
            {"sno":"3","code":"003","particular":"CARBON PAPER","rate":"50.00","quantity":"20","amount":"1000"}
            ],
            "total":"4500"},]}


'items.dat'
-----------

{"items":[{"code":001,"particular":"PEN","rate":40.00,"quantity":250},
          {"code":002,"particular":"PENCIL","rate":5.00,"quantity":400},
          {"code":003,"particular":"CARBON PAPER","rate":50.00,"quantity":1000}]}

'''