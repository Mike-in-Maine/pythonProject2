import sqlite3 as sqlite
import os
import pandas as pd
#conn = sqlite.connect('orders.db')
cursor = conn.cursor()
download_path = "C:/Users/gratt/Desktop/IDS2"
files = os.listdir(download_path)
df = pd.DataFrame()
for filename in files:
    local_filename = os.path.join(download_path, filename)
    dd = pd.read_csv(local_filename, index_col=False)
    df = pd.concat([df, dd], ignore_index=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format='%m/%d/%y')
#df.sort_values(by='ORDERDATE', key=pd.to_datetime, inplace=True)
df.sort_values(by=['ORDERDATE'], inplace=True, ignore_index=True)
#df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
print(df.head())


df.to_csv("C:/Users/gratt/Desktop/all.csv")
df.to_sql(con=conn, name= 'Orders.sql', if_exists= 'replace')
total = df['PRICE'].sum()
count_usa = df.SHIPTOCOUNTRY.str.count("Australia").sum()


print(total, count_usa)