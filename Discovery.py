import pandas as pd
import ftplib
import os
import smtplib
from tkinter import *
import sqlalchemy
from sqlalchemy import create_engine
import sqlite3
import datetime
import matplotlib
import chardet
#from kivy.app import App
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.label import Label
#from kivy.uix.image import Image
#from kivy.uix.button import Button
#from kivy.uix.textinput import TextInput

#sql connection to dreamhost
engine = sqlalchemy.create_engine('mysql+pymysql://miky1973:itff2020@mysql.irish-booksellers.com:3306/irishbooksellers')
def send_email(subject, msg):

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(user='retiredtotuscany@gmail.com', password='itff2021')
    message = 'Subject: {}\n\n{}'.format(subject, msg)
    server.sendmail(from_addr='books@irish-booksellers.com', to_addrs='retiredtotuscany@gmail.com',msg=message)
    server.quit()
def GUI_interface_tkinter():
    app = Tk()
    part_text = StringVar()
    part_label = Label(app, text = 'Part Name', font=('bold', 14))
    part_label.grid(row=0, column=0)

    part_text = Button(app, text = 'Hello', width=16)
    part_label = Label(app, text = 'Part Name', font=('bold', 14))
    part_label.grid(row=0, column=0)

    app.title('Selector')
    app.geometry('700x350')
    app.mainloop()




    if __name__ == "__main__":
        SayHello().run()
def get_abe_ftp_files():
    session = ftplib.FTP_TLS('orders.abebooks.com', 'irishbooksellers', 'ef624a8bd5a843cda651')
    session.prot_p()
    session.cwd('orders')
    files = session.nlst()

    print(files)

    download_path = "C:/Users/gratt/Desktop/IDS2"

    for filename in files:
        local_filename = os.path.join(download_path, filename)
        print(f"Downloading: {local_filename}...", end="")
        if os.path.isfile(local_filename):
            print(" Exists!")
            continue

        file = open(local_filename, 'wb')
        session.retrbinary('RETR %s' % filename, file.write)

        file.close()
        print(" Done!")

    session.close()
def merge_ftp_files():
    download_path = "C:/Users/gratt/Desktop/IDS2"
    files = os.listdir(download_path)
    df = pd.DataFrame()
    for filename in files:
        local_filename = os.path.join(download_path, filename)
        #with open(local_filename, 'rb') as rawdata:
            #result = chardet.detect(rawdata.read(100000))
        #print(result)
        dd = pd.read_csv(local_filename, index_col=False)
        #if you get a UTF error: encoding = "ISO-8859-1" but data might lose special characters
        df = pd.concat([df, dd], ignore_index=True)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    #convert date into pandas date
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format='%m/%d/%y')
    # orders the df by date
    df.sort_values(by=['ORDERDATE'], inplace=True, ignore_index=True)
    # df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    #print(df)
    df_sql = pd.read_sql(sql = 'orders', con = engine)
    df_sql.append(df)
    df.to_csv("C:/Users/gratt/Desktop/all.csv")

    df.drop_duplicates(subset='ABEPOITEMID', keep='first', inplace=True)

    print('Existing df1 HEAD:', (pd.read_sql(sql = 'orders', con = engine).head()))
    print('Existing df1 TAIL:', (pd.read_sql(sql='orders', con=engine).tail()))

    df.to_sql(name = 'orders', con = engine, index = False, if_exists='replace')
    #df.to_sql('orders', con=engine)
    total = df['PRICE'].sum()
    print("Total 98934.68: ", total)
    count_usa = df.SHIPTOCOUNTRY.str.count("U.S.A.").sum()
    print("Number of orders to USA: ", count_usa)

    # SHOW LAST month
    today_date = pd.to_datetime('today')
    print("_____________\nToday is the:", today_date)
    month_ago = datetime.datetime.today()-datetime.timedelta(days=30)
    print(month_ago)
    monthly_range_df = df[(df['ORDERDATE'] > month_ago) & (df['ORDERDATE'] <= today_date)]
    #print(monthly_range_df)
    total = monthly_range_df['PRICE'].sum()
    num_transactions = len(monthly_range_df)
    print(f"Number of transactions since ",month_ago,": ", num_transactions )
    average_sale = total/ num_transactions
    print("Total sales month: ", total)
    print("Total profit month at 16%: ", (total*0.16))
    print("Average sale price (excludes shipping): ", average_sale)
    dec_range_df = df[(df['ORDERDATE'] > '2021-12-01') & (df['ORDERDATE'] <= '2021-12-31')]
    totalshipping = dec_range_df['SHIPPING'].sum()
    print("December shipping: 28396", totalshipping)
    #print(nov_range_df)
    monthly_range_df.to_csv("C:/Users/gratt/Desktop/LastMonth.csv")
    df = pd.read_sql(sql = 'orders', con = engine)
    #weekly_range_df.set_index('ORDERDATE')
#def delete_dusplicate():

#GUI_interface_tkinter()
get_abe_ftp_files()
merge_ftp_files()
#end_email('Hello', 'Its miky!!!!')