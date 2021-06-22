import numpy as np
import os
import pandas as pd
import requests
import sqlite3

from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib import pyplot as plt

dt = datetime.now().strftime("%d %B %Y")
url = 'https://proline.pl/?g=Karty+graficzne&stan=dostepne&sort=cena&wektor=0'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

source = requests.get(url, headers=header).text

soup = BeautifulSoup(source, 'lxml')

results = []
i = 0

for x in soup.find_all("a", class_="produkt"):
    x = str(x)
    x = x[x.find('title')+7 : x.find(' - opis produktu')]
    if "(" in x:
        x = x.split(" (")[0]
    results.append([x])
    
for p in soup.find_all("td", class_="c"):
    p = str(p)
    p = p[14 : p.find(",00</td>")]
    results[i].append(int(p))
    i += 1

results = list(map(tuple, results))

# One big DB for all GPUs
if f'GPU {dt}.db' not in os.listdir():
    con = sqlite3.connect(f'GPU {dt}.db')
    c = con.cursor()

    c.execute("""CREATE TABLE GPUs (GPU, price)""")

    c.executemany("INSERT INTO GPUs VALUES (?,?)", results)

    con.commit()
    con.close()

# And for each model separately
models = ["710","730","1030","1050 Ti","1660","1660 Ti","1660 SUPER","2060","3060","6700 XT","3070","3070 Ti","3080","3080 Ti","6800 XT","6900 XT","3090"]

obj = {}
for i in models:
    obj['results'+i] = [x for x in results if i in x[0]]

for key, value in obj.items():
    con = sqlite3.connect(f"{key}.db")
    c = con.cursor()
    if " " in key:
        key = key.replace(" ", "_")
    c.execute(f"CREATE TABLE {key} (GPU, price)")

    c.executemany(f"INSERT INTO {key} VALUES (?,?)", value)

    con.commit()
    con.close()

# Deleting Ti & SUPER models from databases of regular models
dbs = {
    "1660": "results1660",
    "3070": "results3070",
    "3080": "results3080"
}

for i, j in dbs.items():
    con = sqlite3.connect(f"{j}.db")
    c = con.cursor()

    c.execute(f"DELETE FROM {j} WHERE GPU LIKE '%{i} SUPER%' OR GPU LIKE '%{i} Ti%'")

    con.commit()
    con.close()










# print(obj)
# print(type(obj))

# for key, lis in obj.items():
#     while n < 13:
#         if models[n] in key:
#             print(key)
#             n += 1
            # for item in results:
            #     if key in item[0]:
            #         print(key)
                    # lis.append(item)

# print(obj)


#     while n < 13:
#         for key, value in pair:
#             if models[n] in key:
#                 for item in results:
#                     if key in item[0]:
#                         value.append(item)

# print(obj)
    

# for x in models:
#     x = []
#     for item in results:
#         if x in item[0]:
#             x.append(item)
#     print(x)


# results710 = [] 
# for item in results:
#     if "710" in item[0]:
#         results710.append(item)
# print(results710)