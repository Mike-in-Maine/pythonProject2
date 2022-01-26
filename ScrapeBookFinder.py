import pandas as pd



while True:
    for test in range(1,100,1):
        url = 'https://www.bookfinder.com/search/?author=&title=&lang=en&isbn=1406364835&new_used=*&destination=it&currency=EUR&mode=basic&st=sr&ac=qr'
        df = pd.read_html(url)
        #pd.set_option('display.max_rows', None)
        #pd.set_option('display.max_columns', None)
        #pd.set_option('display.width', None)
        used = df[3]
        #print(used['Notes'])
        #print([used])


        print (used)

