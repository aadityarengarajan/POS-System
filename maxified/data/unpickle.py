from pickle import dump,load
import json

def read_items():
    with open("items.dat","rb") as f:
        items_file = load(f)
    return items_file

def read_sales():
    with open("sales.dat","rb") as f:
        sales_file = load(f)
    return sales_file

with open("items.json","w") as f:
    json.dump(read_items(),f)

with open("sales.json","w") as f:
    json.dump(read_sales(),f)