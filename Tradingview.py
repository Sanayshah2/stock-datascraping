import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime 
import time as t
name = input('Enter stock symbol\n')
PATH = 'C:\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get('https://in.tradingview.com/')
search = driver.find_element_by_class_name('tv-header-search__input')
search.send_keys('{}'.format(name))
search.send_keys(Keys.RETURN)
t.sleep(3)
price = []
timeseries = []
while True: 
    now = datetime.now()
    time = now.strftime("%H:%M:%S"    )
    date = now.strftime("%d/%m/%y")
    if time >= '09:15:00' and time < '15:30:00':
        live_price = driver.find_element_by_class_name('tv-symbol-price-quote__value')  
        initial_price = live_price.text
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        price.append(initial_price)
        timeseries.append(time)
        print('Appending initial price at the start')
        while True:
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            if time == '15:30:00':
                break
            live_price = driver.find_element_by_class_name('tv-symbol-price-quote__value') 
            current_price = live_price.text
            if current_price == initial_price:
                print('Same Price '+current_price)
                t.sleep(1)
                continue
            else:
                print('Appending '+current_price)
                t.sleep(1)
                price.append(current_price)
                timeseries.append(time)
                initial_price = current_price
    else :
        break
df = pd.DataFrame({'Time':timeseries, 'Price':price})
df.to_csv('{}_{} {}.csv'.format(name, now.strftime('%b'), now.strftime('%d')), index = False)
driver.quit()
