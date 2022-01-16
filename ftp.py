import ftplib
import os
import pandas as pd
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



